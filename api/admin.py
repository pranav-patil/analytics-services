from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from records.models import BlogPost
from .models import VideoGameSales, SuicideStatistics


class VideoGameSalesResource(resources.ModelResource):
    set_unique = set()

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        # Clear out anything that may be there from a dry_run, such as the admin mixin preview
        self.set_unique = set()

    def skip_row(self, instance, original):
        name = instance.name  # Could also use composer_key_id
        platform = instance.platform
        tuple_unique = (name, platform)

        if (tuple_unique in self.set_unique) and (not name) and (not platform):
            print(
                f"tuple_unique = {tuple_unique}, set_unique = {self.set_unique}, name = {name}, platform = {platform}")
            return True
        else:
            self.set_unique.add(tuple_unique)

        return super(VideoGameSalesResource, self).skip_row(instance, original)

    class Meta:
        model = VideoGameSales


class VideoGameSalesAdmin(ImportExportModelAdmin):
    resource_class = VideoGameSalesResource


class SuicideStatisticsResource(resources.ModelResource):
    set_unique = set()

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        # Clear out anything that may be there from a dry_run, such as the admin mixin preview
        self.set_unique = set()

    def skip_row(self, instance, original):
        country = instance.country  # Could also use composer_key_id
        year = instance.year
        sex = instance.sex
        age = instance.age
        tuple_unique = (country, year, sex, age)

        if (tuple_unique in self.set_unique) and (not country) and (not year) and (not sex) and (not age):
            print(
                f"tuple_unique = {tuple_unique}, set_unique = {self.set_unique}, country = {country}, year = {year}, "
                f"sex = {sex}, age = {age},")
            return True
        else:
            self.set_unique.add(tuple_unique)

        return super(SuicideStatisticsResource, self).skip_row(instance, original)

    class Meta:
        model = SuicideStatistics


class SuicideStatisticsAdmin(ImportExportModelAdmin):
    resource_class = SuicideStatisticsResource


admin.site.register(BlogPost)
admin.site.register(VideoGameSales, VideoGameSalesAdmin)
admin.site.register(SuicideStatistics, SuicideStatisticsAdmin)
