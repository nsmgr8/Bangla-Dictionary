#!/usr/bin/env python
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
import os
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template
from google.appengine.api import users

from models import Word, WordComment
from forms import WordForm

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')

def render(template_name, template_values={}):
    """ render a django template """
    user = users.get_current_user()
    if user:
        auth = {'admin': users.is_current_user_admin(), 'auth_url':
                users.create_logout_url('/')}
    else:
        auth = {'auth_url': users.create_login_url('/')}

    template_values.update({'user': users.get_current_user()})
    template_values.update(auth)

    template_path = os.path.join(TEMPLATE_DIR, template_name)
    return template.render(template_path, template_values)


class MainHandler(webapp.RequestHandler):
    """ main page """
    def get(self):
        html = render('index.html')
        self.response.out.write(html)


class InputHandler(webapp.RequestHandler):
    """ input page """
    def _get_instance(self):
        _id = self.request.GET.get('id', None)
        if _id:
            self.instance = Word.get_by_id(long(_id))
        else:
            self.instance = None

    def get(self):
        self._get_instance()
        form = WordForm(instance=self.instance)
        html = render('input.html', {'form': form})
        self.response.out.write(html)

    def post(self):
        self._get_instance()
        form = WordForm(data=self.request.POST, instance=self.instance)
        if form.is_valid():
            entity = form.save(commit=False)
            entity.contributor = users.get_current_user()

            synonyms = self.request.POST.get('synonyms', None)
            if synonyms:
                entity.synonyms = [w.strip() for w in synonyms.split(',')]

            antonyms = self.request.POST.get('antonyms', None)
            if antonyms:
                entity.antonyms = [w.strip() for w in antonyms.split(',')]

            entity.put()
            self.redirect('/input')
        else:
            pass
        html = render('input.html', {'form': form})
        self.response.out.write(html)

class ListHandler(webapp.RequestHandler):
    """ list words """
    def get(self):
        dictionary = int(self.request.GET.get('dict', 0))
        words = Word.all_by_dictionary(dictionary).order('bangla').fetch(100)
        html = render('list.html', {'words': words})
        self.response.out.write(html)

class CommentHandler(webapp.RequestHandler):
    """ comment list """
    def get_word(self):
        word_id = self.request.GET.get('id', None)
        if not word_id:
            return None

        return Word.get_by_id(long(word_id))

    def get(self):
        word = self.get_word()
        if not word:
            self.error(404)
            return

        comments = WordComment.all().filter('word =', word).fetch(20)
        html = render('comments.html', {'comments': comments, 'word': word})
        self.response.out.write(html)

    def post(self):
        word = self.get_word()
        if not word:
            self.error(404)
            return

        comment = self.request.POST.get('comment', None)
        if comment:
            WordComment(word=word, comment=comment,
                        user=users.get_current_user()).put()

        self.redirect('/comments?id=%d' % word.key().id())


class AdminHandler(webapp.RequestHandler):
    """ admin page """
    def get(self):
        self.response.out.write('Hello admin!')

def main():
    routes = [('/', MainHandler),
              ('/list', ListHandler),
              ('/comments', CommentHandler),
              ('/input', InputHandler),
              ('/admin', AdminHandler),
             ]
    debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
    application = webapp.WSGIApplication(routes, debug=debug)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()

