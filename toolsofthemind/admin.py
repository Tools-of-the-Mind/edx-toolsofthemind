from django.contrib import admin

from .models import TOMCourseGroups, TOMCourseSubgroups, TOMCourseMenu, TOMStudentCourseGroups


class TOMCourseGroupsAdmin(admin.ModelAdmin):
    """
    Django admin customizations for TOMCourseGroups model
    """

    inlines = [
        TOMCourseSubgroups,
    ]


class TOMCourseSubgroupsAdmin(admin.TabularInline):
    """
    Django admin customizations for TOMCourseSubgroups model
    """

    inlines = [
        TOMCourseMenu,
    ]


class TOMCourseMenuAdmin(admin.ModelAdmin):
    """
    Django admin customizations for TOMCourseSubgroups model
    """

    search_fields = (
        "course_subgroup",
        "course",
    )


class TOMStudentCourseGroupsAdmin(admin.ModelAdmin):
    """
    Django admin customizations for TOMStudentCourseGroups model
    """

    search_fields = (
        "user",
        "course_group",
    )


admin.site.register(TOMCourseGroups, TOMCourseGroupsAdmin)
admin.site.register(TOMCourseSubgroups, TOMCourseSubgroupsAdmin)
admin.site.register(TOMCourseMenu, TOMCourseMenuAdmin)
admin.site.register(TOMStudentCourseGroups, TOMStudentCourseGroupsAdmin)
