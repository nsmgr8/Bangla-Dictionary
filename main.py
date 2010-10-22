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

from forms import WordForm

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')

def render(template_name, template_values={}):
    """ render a django template """
    user = users.get_current_user()
    if user:
        auth = {'admin': users.is_current_user_admin(), 'auth_url':
                users.create_logout_url('/')}
    else:
        auth = {'auth_url': users.create_login_url('/input')}

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
    def get(self):
        form = WordForm(initial={'contributor': users.get_current_user()})
        html = render('input.html', {'form': form})
        self.response.out.write(html)

    def post(self):
        form = WordForm(data=self.request.POST)
        if form.is_valid():
            entity = form.save(commit=False)

            synonyms = self.request.POST.get('synonyms', None)
            if synonyms:
                entity.synonyms = [w.strip() for w in synonyms.split(',')]

            antonyms = self.request.POST.get('antonyms', None)
            if antonyms:
                entity.antonyms = [w.strip() for w in antonyms.split(',')]

            entity.put()
            form = WordForm(initial={'contributor': users.get_current_user()})
        else:
            pass
        html = render('input.html', {'form': form})
        self.response.out.write(html)


class AdminHandler(webapp.RequestHandler):
    """ admin page """
    def get(self):
        self.response.out.write('Hello admin!')

def main():
    routes = [('/', MainHandler),
              ('/input', InputHandler),
              ('/admin', AdminHandler),
             ]
    debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
    application = webapp.WSGIApplication(routes, debug=debug)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()

