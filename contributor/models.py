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

class Contributor(models.Model):
    website = models.CharField(max_length=200, blank=True)
    ims = models.CharField(max_length=200, blank=True)
    number_words = models.IntegerField(default=0)
    number_accepted = models.IntegerField(default=0)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.user.username

def get_or_create_profile(self):
    try:
        return Contributor.objects.filter(user=self).get()
    except Contributor.DoesNotExist:
        profile = Contributor(user=self)
        profile.save()
        return profile
User.get_or_create_profile = get_or_create_profile

def display_name(self):
    return self.first_name or self.username
User.display_name = display_name

