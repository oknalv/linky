#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
import webapp2
import os
import jinja2
from google.appengine.api import users
from link import Container
from base import BaseHandler

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader( os.path.dirname( __file__ ) ),
    extensions=[ "jinja2.ext.autoescape" ],
    autoescape=True )

class MainHandler(BaseHandler):
    def __init__(self, request = None, response = None):
        self.initialize( request, response )
        self.template = "templates/main.html"

    def get(self):

        user = users.get_current_user()
        vars = {}
        vars["page"] = "main"
        if not self.session.get("lang"):
            self.session["lang"] = "en"

        vars["lang"] = self.session.get("lang")
        vars["logged"] = False
        vars["links"] = []
        vars["flash"] = self.get_flash()
        if user:
            vars["logged"] = True
            containers = Container.query(Container.user == user)
            cont = None
            if not containers.iter().has_next():
                cont = Container(user = user)
                cont.put()
            else:
                cont = containers.iter().next()

            if self.request.get("search"):
                vars["is_search"] = True

            else:
                vars["is_search"] = False

            if self.request.get("tag"):
                vars["is_tag"] = True

            else:
                vars["is_tag"] = False

            for link in cont.links:
                if vars["is_search"]:
                    search = self.request.get("search")
                    tags = link.tags.split(" ")
                    if search in link.name or search in link.url or search in tags:
                        vars["links"].append([link.name, link.url, link.tags])

                elif vars["is_tag"]:
                    tags = link.tags.split(" ")
                    if self.request.get("tag") in tags:
                        vars["links"].append([link.name, link.url, link.tags])

                else:
                    vars["links"].append([link.name, link.url, link.tags])

        vars["login_link"] = users.create_login_url("/")
        vars["logout_link"] = users.create_logout_url("/")

        template = JINJA_ENVIRONMENT.get_template(self.template)
        self.response.write(template.render(vars))

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'merely remarkable came line',
}

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug = True, config = config)
