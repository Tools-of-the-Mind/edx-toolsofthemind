from django.contrib.auth import get_user_model
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save

from .models import TOMStudentCourseGroups

User = get_user_model()  # returns common.djangoapps.student.models


@receiver(post_save, sender=User)
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
