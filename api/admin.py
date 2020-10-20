from django.contrib import admin
from records.models import BlogPost
from import_export import resources
from records.models import BlogPost
from .models import VideoGameSales
from import_export.admin import ImportExportModelAdmin


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


admin.site.register(BlogPost)
admin.site.register(VideoGameSales, VideoGameSalesAdmin)
