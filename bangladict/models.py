#
# Copyright 2010 BengDict Project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from django.db import models
from django.contrib.auth.models import User


class Dictionary(models.Model):
    name = models.CharField(max_length=200)
    source_language = models.CharField(max_length=200)
    target_language = models.CharField(max_length=200)
    abbrev = models.CharField(max_length=10)
    pos = models.TextField(verbose_name='Parts of Speech')
    alphabets = models.TextField()

    class Meta:
        verbose_name = 'Dictionary'
        verbose_name_plural = 'Dictionaries'

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.abbrev)

    @property
    def reverse_dict(self):
        d = self.abbrev.split('2')
        return "%s2%s" % (d[-1], d[0])

NEW, ACCEPTED, REJECTED, CLOSED = 0, 1, 2, 3
EDIT_STATES = [(NEW, 'New'), (ACCEPTED, 'Accepted'), (REJECTED, 'Rejected'),
               (CLOSED, 'Closed')]

class Word(models.Model):
    dictionary = models.ForeignKey(Dictionary)
    alpha = models.CharField(max_length=5)
    original = models.CharField(max_length=50)
    translation = models.CharField(max_length=50)
    phoneme = models.CharField(max_length=70, blank=True)
    pos = models.CharField(max_length=50, verbose_name='Parts of Speech')
    description = models.TextField(blank=True)
    synonyms = models.CharField(max_length=500, blank=True)
    antonyms = models.CharField(max_length=500, blank=True)
    contributor = models.ForeignKey(User)
    status = models.IntegerField(default=NEW, choices=EDIT_STATES)
    added_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s -> %s' % (self.original, self.translation)

class WordLoad(models.Model):
    contributor = models.ForeignKey(User)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    hash = models.CharField(max_length=256)
    file = models.TextField()

    def __unicode__(self):
        return self.file[:20]

