"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Sep-2021

toolsofthemind Django admin views.
"""
from django.contrib import admin

from .models import TOMCourseGroups, TOMCourseSubgroups, TOMCourseMenu, TOMStudentCourseGroups


class TOMCourseSubgroupsInline(admin.TabularInline):
    """
    Django admin customizations for TOMCourseSubgroups model
    """

    model = TOMCourseSubgroups


class TOMCourseGroupsAdmin(admin.ModelAdmin):
    """
    Django admin customizations for TOMCourseGroups model
    """

    list_display = [
        "course_group",
        "created",
        "modified",
    ]

    inlines = [
        TOMCourseSubgroupsInline,
    ]


class TOMCourseMenuAdmin(admin.ModelAdmin):
    """
    Django admin customizations for TOMCourseSubgroups model
    """

    search_fields = (
        "course_subgroup__course_group",
        "course_subgroup__course_subgroup",
        "course__id",
    )
    list_display = [
        "course_subgroup",
        "course",
        "required",
        "created",
        "modified",
    ]


class TOMStudentCourseGroupsAdmin(admin.ModelAdmin):
    """
    Django admin customizations for TOMStudentCourseGroups model
    """

    search_fields = ["course_group__course_group", "user__username", "user__email"]
    list_display = [
        "user",
        "course_group",
        "created",
        "modified",
    ]


admin.site.register(TOMCourseGroups, TOMCourseGroupsAdmin)
admin.site.register(TOMCourseMenu, TOMCourseMenuAdmin)
admin.site.register(TOMStudentCourseGroups, TOMStudentCourseGroupsAdmin)
