from django.contrib.comments.models import BaseCommentAbstractModel

FIELD_INDEXES = {
    BaseCommentAbstractModel: {'indexed': ['object_pk',]},
}
