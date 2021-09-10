"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Sep-2021

toolsofthemind App models.
Custom models for categorizing the presentation of the course library to students based
on customized groupings.

Example:
------------------------------------------
PREK WORKSHOP 1
 - Opening Group Activities
 - Classroom Practices and Self-Reg
    - Course 1 (an actual course in Open edX)
    - Course 2 (an actual course in Open edX)
 - Make Believe Play Block
 - Large Group Literacy
 - Small Group Literacy
 - Math & Science

"""
from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview


User = get_user_model()  # returns common.djangoapps.student.models


class TOMCourseGroups(TimeStampedModel):
    """
    Tools of the Mind course directory Main Menu Labels
    Example: WORKSHOP 1
    """

    course_group = models.CharField(
        primary_key=True,
        max_length=50,
        default="new course group",
        help_text=_("Tools of the Mind course group description. Example: PreK Workshop 1"),
    )

    class Meta:
        ordering = "created"

    def __str__(self):
        return self.course_group


class TOMCourseSubgroups(TimeStampedModel):
    """
    Tools of the Mind course directory Main Menu sub-labels
    Example: OPENING GROUP ACTIVITIES
    """

    course_group = models.ForeignKey(
        TOMCourseGroups,
        db_constraint=True,
        on_delete=models.CASCADE,
    )
    ordinal_position = models.IntegerField(
        default=0,
        help_text="The ordinal position of this record in relation to all other"
        "Sub Group items for this Tools of the Mind Course Group.",
    )
    course_subgroup = models.CharField(max_length=50, blank=False, default="new subgroup")

    class Meta:
        unique_together = (
            ("course_group", "course_subgroup"),
            ("ordinal_position", "course_subgroup"),
        )
        ordering = ("course_group", "ordinal_position")

    def __str__(self):
        return self.course_group + ":" + self.course_subgroup


class TOMCourseMenu(TimeStampedModel):
    """
    The set of Open edX courses associated with one TOM Course Group / Sub-group combination.
    """

    course_subgroup = models.ForeignKey(
        TOMCourseSubgroups,
        db_constraint=True,
        on_delete=models.CASCADE,
    )

    course = models.ForeignKey(
        CourseOverview,
        db_constraint=True,
        on_delete=models.CASCADE,
    )

    required = models.BooleanField(default=False)

    class Meta:
        unique_together = (("course_subgroup", "course"),)
        ordering = ("course_subgroup", "course")

    def __str__(self):
        return self.course_group + ":" + self.course_group


class TOMStudentCourseGroups(TimeStampedModel):
    """
    The set of TOM Course Groups associated with one learner.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    course_group = models.ForeignKey(
        TOMCourseGroups,
        blank=True,
        db_constraint=True,
        on_delete=models.CASCADE,
    )


@receiver(models.signals.post_save, sender=User)
def _add_tom_student_course_groups(
    sender, instance, created, raw, using, update_fields, **kwargs
):  # pylint: disable=unused-argument
    """
    Create one TOMStudentCourseGroups record for each new Django user record created.
    https://docs.djangoproject.com/en/3.2/ref/signals/

    sender: The model class.
    instance: The actual instance being saved.
    created: A boolean; True if a new record was created.
    raw: A boolean; True if the model is saved exactly as presented (i.e. when loading a fixture). One should not query/modify other records in the database as the database might not be in a consistent state yet.
    using: The database alias being used.
    update_fields:The set of fields to update as passed to Model.save(), or None if update_fields wasn’t passed to save().

    """
    if created:
        student_course_groups = TOMStudentCourseGroups(user=instance)
        student_course_groups.save()
