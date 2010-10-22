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

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util


class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')


class InputHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello input!')

class AdminHandler(webapp.RequestHandler):
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

