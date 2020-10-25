import re
from io import BytesIO

import matplotlib
import pandas as pd
from django.http import HttpResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_pandas import PandasSimpleView, PandasView, PandasJSONRenderer, PandasSVGRenderer

from records.models import BlogPost
from .models import VideoGameSales
from .permissions import UserIsOwnerBlogPost
from .serializers import BlogPostSerializer
from .serializers import VideoGameSalesSerializer

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns


class BlogPostListCreateAPIView(ListCreateAPIView):
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        return BlogPost.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BlogPostDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()
    permission_classes = (IsAuthenticated, UserIsOwnerBlogPost)


# class BlogPostRudView(RetrieveUpdateDestroyAPIView):
#     lookup_field = 'pk'  # slug, id
#     queryset = BlogPost.objects.all()
#
#     def get_queryset(self):
#         return BlogPost.objects.all()
#
#     def get_object(self):
#         pk = self.kwargs.get("pk")
#         return BlogPost.objects.get(pk=pk)


class SuicideStatisticsView(PandasSimpleView):
    renderer_classes = [PandasJSONRenderer]

    def get_data(self, request, *args, **kwargs):
        return pd.read_csv('data/who_suicide_statistics.csv')


def set_style(style):
    if style:
        if style in plt.style.available:
            plt.style.use(style)
        else:
            raise ValueError(
                f'Invalid value style parameter {style}, valid values are: {plt.style.available}')
    else:
        plt.style.use('default')


def transform_filter_by(dataframe, filter_col, filter_val):

    valid_filter_cols = dataframe.columns.values.tolist()

    if filter_col and filter_val:
        if filter_col in valid_filter_cols:
            dataframe = dataframe.loc[dataframe[filter_col].str.contains(filter_val, flags=re.I, regex=True)]
        else:
            raise ValueError('Valid values for filter by columns are: {}'.format(valid_filter_cols))

    return dataframe


def transform_group_by(dataframe, group_by):

    valid_group_cols = ['platform', 'year', 'genre', 'publisher']

    if group_by:
        if group_by in valid_group_cols:
            dataframe = dataframe.groupby([group_by])['usa_sales', 'europe_sales',
                                                      'japan_sales', 'other_sales',
                                                      'global_sales'].apply(lambda x: x.astype(float).sum())
        else:
            raise ValueError('Valid values for group by argument are: {}'.format(valid_group_cols))

    return dataframe


def transform_sort_by(dataframe, sort_column):

    valid_sort_cols = dataframe.columns.values.tolist()

    if sort_column:
        if sort_column in valid_sort_cols:
            dataframe = dataframe.sort_values(sort_column)
        else:
            raise ValueError('Valid values for sort columns are: {}'.format(valid_sort_cols))

    return dataframe


class VideoGameSalesView(PandasView):
    renderer_classes = [PandasJSONRenderer, PandasSVGRenderer]
    queryset = VideoGameSales.objects.all()
    serializer_class = VideoGameSalesSerializer

    def filter_queryset(self, qs):
        return qs

    def transform_dataframe(self, dataframe):
        filter_col = self.request.query_params.get('filter_column')
        filter_val = self.request.query_params.get('filter_value')
        dataframe = transform_filter_by(dataframe, filter_col, filter_val)

        group_by = self.request.query_params.get('group')
        dataframe = transform_group_by(dataframe, group_by)

        sort_column = self.request.query_params.get('sort')
        dataframe = transform_sort_by(dataframe, sort_column)

        return dataframe

    def list(self, request, *args, **kwargs):

        is_chart = kwargs.get('chart', False)

        chart_type = self.request.query_params.get('chart')
        valid_chart_types = ['scatter', 'box', 'swarm', 'joint', 'histogram', 'bar', 'pie', 'line', 'category']

        if is_chart:

            if chart_type not in valid_chart_types:
                raise ValueError(
                    f'In valid value of parameter chart (type) = {chart_type}, valid values are: {valid_chart_types}')

            response = super().list(request, *args, **kwargs)
            dataframe = response.data

            sns.set_context("paper", font_scale=1.0, rc={"lines.linewidth": 2.5})
            set_style(self.request.query_params.get('style'))

            if chart_type == 'scatter':

                fig = plt.figure(figsize=(10, 7))
                x_column, y_column = self.get_columns(dataframe)
                sns.lmplot(x=x_column, y=y_column, data=dataframe, fit_reg=False)
                plt.ylim(0, None)
                plt.xlim(0, None)

            elif chart_type == 'box':

                fig = plt.figure(figsize=(14, 5))
                x_column, y_column = self.get_columns(dataframe)
                sns.boxplot(x=x_column, y=y_column, data=dataframe)
                plt.xticks(rotation=-45)

            elif chart_type == 'swarm':

                fig = plt.figure(figsize=(10, 6))
                x_column, y_column = self.get_columns(dataframe)
                sns.swarmplot(x=x_column, y=y_column, data=dataframe)

                # adjust the y-axis
                plt.ylim(0, 260)
                # place legend to the right
                plt.legend(bbox_to_anchor=(1, 1), loc=2)
                plt.xticks(rotation=-45)

            elif chart_type == 'category':

                fig = plt.figure(figsize=(10, 6))
                x_column, y_column = self.get_columns(dataframe)
                sns.catplot(x=x_column, y=y_column, data=dataframe)
                plt.xticks(rotation=-45)

            elif chart_type == 'joint':

                fig = plt.figure(figsize=(10, 6))
                x_column, y_column = self.get_columns(dataframe)
                sns.jointplot(x=x_column, y=y_column, data=dataframe)

            elif chart_type == 'histogram':

                fig = plt.figure(figsize=(14, 5))
                x_column = self.get_column(dataframe, 'x')

                # ,hist=False
                sns.distplot(dataframe[x_column])

            elif chart_type == 'bar':

                fig = plt.figure(figsize=(10, 7))
                x_column, y_column = self.get_columns(dataframe)

                if self.request.query_params.get('hue'):
                    hue_column = self.get_column(dataframe, 'hue')
                    sns.barplot(x=x_column, y=y_column, hue=hue_column, data=dataframe)
                else:
                    sns.barplot(x=x_column, y=y_column, data=dataframe)

                plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
                plt.xticks(rotation=45)

            elif chart_type == 'pie':

                fig = plt.figure(figsize=(8, 8))
                y_column = self.get_column(dataframe, 'y')
                dataframe.plot.pie(y=y_column, autopct='%1.1f%%', startangle=90, shadow=True, legend=False)
                plt.tight_layout()
                plt.axis('equal')
                # plt.legend(loc=5)

            elif chart_type == 'line':

                fig = plt.figure(figsize=(10, 7))
                x_column, y_column = self.get_columns(dataframe)
                dataframe.plot(x=x_column, y=y_column, kind='line')

            else:
                raise NotImplementedError(f'Chart type {chart_type} currently not supported.')

            # save the figure as a bytes string in the svg format.
            bytes_io = BytesIO()
            plt.savefig(bytes_io, format="svg")
            self.renderer_classes = [PandasSVGRenderer]
            response = HttpResponse(bytes_io.getvalue(), content_type='image/svg+xml')
            fig.clf()
            plt.close(fig)
            plt.close('all')
            return self.update_pandas_headers(response)
        else:
            self.renderer_classes = [PandasJSONRenderer]
            return super().list(request, *args, **kwargs)

    def get_column(self, dataframe, name):

        column = self.request.query_params.get(name)
        column_names = dataframe.columns.values.tolist()

        if column not in column_names:
            raise ValueError(f'In valid value of parameter {name} = {column}, valid values are: {column_names}')

        return column

    def get_columns(self, dataframe):

        x_column = self.request.query_params.get('x')
        y_column = self.request.query_params.get('y')
        column_names = dataframe.columns.values.tolist()

        if x_column not in column_names:
            raise ValueError(f'In valid value of parameter x = {x_column}, valid values are: {column_names}')
        if y_column not in column_names:
            raise ValueError(f'In valid value of parameter y = {y_column}, valid values are: {column_names}')

        return x_column, y_column

