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

from django.utils.translation import ugettext_lazy as _


class Dictionary(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    source_language = models.CharField(max_length=200,
                                       verbose_name=_("Source Language"))
    target_language = models.CharField(max_length=200,
                                      verbose_name=_("Target Language"))
    abbrev = models.CharField(max_length=10, verbose_name=_("Abbreviation"))
    pos = models.TextField(verbose_name=_('Parts of Speech'))
    alphabets = models.TextField(verbose_name=_('Alphabets'))

    class Meta:
        verbose_name = _('Dictionary')
        verbose_name_plural = _('Dictionaries')

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.abbrev)

    @property
    def reverse_dict(self):
        d = self.abbrev.split('2')
        return "%s2%s" % (d[-1], d[0])

NEW, ACCEPTED, REJECTED, CLOSED = 0, 1, 2, 3
EDIT_STATES = [(NEW, _('New')), (ACCEPTED, _('Accepted')),
               (REJECTED, _('Rejected')), (CLOSED, _('Closed'))]

class Word(models.Model):
    dictionary = models.ForeignKey(Dictionary, verbose_name=_('Dictionary'))
    alpha = models.CharField(max_length=5, verbose_name=_('alpha'))
    original = models.CharField(max_length=50, verbose_name=_('Original'))
    translation = models.CharField(max_length=50,
                                   verbose_name=_('Translation'))
    phoneme = models.CharField(max_length=70, blank=True,
                               verbose_name=_('Phoneme'))
    pos = models.CharField(max_length=50, verbose_name=_('Parts of Speech'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    synonyms = models.CharField(max_length=500, blank=True,
                                verbose_name=_('Synonyms'))
    antonyms = models.CharField(max_length=500, blank=True,
                                verbose_name=_('Antonyms'))
    contributor = models.ForeignKey(User, verbose_name=_('Contributor'))
    status = models.IntegerField(default=NEW, choices=EDIT_STATES,
                                 verbose_name=_('Status'))
    added_at = models.DateTimeField(auto_now_add=True,
                                    verbose_name=_('Added at'))

    def __unicode__(self):
        return '%s -> %s' % (self.original, self.translation)

    def save(self, *args, **kwargs):
        self.alpha = self.original[0].lower()
        super(Word, self).save(*args, **kwargs)

class WordLoad(models.Model):
    contributor = models.ForeignKey(User, verbose_name=_('Contributor'))
    uploaded_at = models.DateTimeField(auto_now_add=True,
                                       verbose_name=_('Uploaded at'))
    hash = models.CharField(max_length=256, verbose_name=_('Hash'))
    file = models.TextField(verbose_name=_('File'))

    def __unicode__(self):
        return self.file[:20]

