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

from google.appengine.ext import db

class Word(db.Model):
    """
    The main model to store the word definitions.
        dictionary: a string defining the dictionary. i.e., Bangla to English or
            English to Bangla.
        bangla: the word in Bangla
        english: the word in English
        pos: parts of speech of the word
        description: Optional description, example of the word
        contributor: user who first entried it first
    """
    dictionary = db.StringProperty(required=True)
    bangla = db.StringProperty(required=True)
    english = db.StringProperty(required=True)
    phoneme = db.StringProperty(required=False, indexed=False)
    pos = db.StringProperty(required=True, indexed=False)
    description = db.TextProperty(required=False, indexed=False)
    synonyms = db.ListProperty(required=False)
    antonyms = db.ListProperty(required=False)
    contributor = db.UserProperty(required=True)

    @classmethod
    def all_by_dictionary(cls, dict):
        """ filter by dictionary """
        return cls.all().filter('dictionary =', dict)

class WordEdit(db.Model):
    """
    """
    word = db.ReferenceProperty(Word, required=True)
    description = db.TextProperty(required=True, indexed=False)

class Profile(db.Model):
    """
    The user profile. This will store the contributors profile.
    """
    user = db.UserProperty(required=True)
    username = db.StringProperty(required=True)
    fullname = db.StringProperty(required=True, indexed=False)
    email = db.StringProperty(required=True, indexed=False)
    website = db.StringProperty(required=False, indexed=False)

