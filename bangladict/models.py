from django.db import models
from django.contrib.auth.models import User


class Dictionary(models.Model):
    name = models.CharField(max_length=200)
    source_language = models.CharField(max_length=200)
    target_language = models.CharField(max_length=200)
    abbrev = models.CharField(max_length=10)
    pos = models.TextField(verbose_name='Parts of Speech')

    class Meta:
        verbose_name = 'Dictionary'
        verbose_name_plural = 'Dictionaries'

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.abbrev)

NEW, ACCEPTED, REJECTED, CLOSED = 0, 1, 2, 3
EDIT_STATES = [(NEW, 'New'), (ACCEPTED, 'Accepted'), (REJECTED, 'Rejected'),
               (CLOSED, 'Closed')]

class Word(models.Model):
    dictionary = models.ForeignKey(Dictionary)
    original = models.CharField(max_length=50)
    translation = models.CharField(max_length=50)
    phoneme = models.CharField(max_length=70)
    pos = models.CharField(max_length=50, verbose_name='Parts of Speech')
    description = models.TextField()
    synonyms = models.CharField(max_length=500)
    antonyms = models.CharField(max_length=500)
    contributor = models.ForeignKey(User)
    status = models.IntegerField(default=NEW, choices=EDIT_STATES)
    added_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s :: %s' % (self.original, self.translation)

