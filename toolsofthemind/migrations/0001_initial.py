# Generated by Django 2.2.24 on 2021-09-10 21:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("course_overviews", "0024_overview_adds_has_highlights"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TOMCourseGroups",
            fields=[
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="modified"
                    ),
                ),
                (
                    "course_group",
                    models.CharField(
                        default="new course group",
                        help_text="Tools of the Mind course group description. Example: PreK Workshop 1",
                        max_length=50,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
            ],
            options={
                "ordering": ["created"],
            },
        ),
        migrations.CreateModel(
            name="TOMStudentCourseGroups",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="modified"
                    ),
                ),
                (
                    "course_group",
                    models.ForeignKey(
                        blank=True, on_delete=django.db.models.deletion.CASCADE, to="toolsofthemind.TOMCourseGroups"
                    ),
                ),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TOMCourseSubgroups",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="modified"
                    ),
                ),
                (
                    "ordinal_position",
                    models.IntegerField(
                        default=0,
                        help_text="The ordinal position of this record in relation to all otherSub Group items for this Tools of the Mind Course Group.",
                    ),
                ),
                ("course_subgroup", models.CharField(default="new subgroup", max_length=50)),
                (
                    "course_group",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="toolsofthemind.TOMCourseGroups"),
                ),
            ],
            options={
                "ordering": ("course_group", "ordinal_position"),
                "unique_together": {("ordinal_position", "course_subgroup"), ("course_group", "course_subgroup")},
            },
        ),
        migrations.CreateModel(
            name="TOMCourseMenu",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="modified"
                    ),
                ),
                ("required", models.BooleanField(default=False)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="course_overviews.CourseOverview"
                    ),
                ),
                (
                    "course_subgroup",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="toolsofthemind.TOMCourseSubgroups"
                    ),
                ),
            ],
            options={
                "ordering": ("course_subgroup", "course"),
                "unique_together": {("course_subgroup", "course")},
            },
        ),
    ]