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

class TagsHandler(BaseHandler):
    def __init__(self, request = None, response = None):
        self.initialize( request, response )
        self.template = "templates/tags.html"

    def get(self):

        user = users.get_current_user()
        vars = {}
        vars["page"] = "tags"
        if not self.session.get("lang"):
            self.session["lang"] = "en"

        vars["lang"] = self.session.get("lang")
        vars["logged"] = False
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
            vars["tags"] = {}
            for link in cont.links:
                for tag in link.tags.split(" "):
                    if tag not in vars["tags"].keys():
                        vars["tags"][tag] = 1
                    else:
                        vars["tags"][tag] += 1

            min, max = 0, 0
            for key, val in vars["tags"].iteritems():
                if min == 0 or min > val:
                    min = val
                if max < val:
                    max = val

            div = (max - min) / 3
            for key, val in vars["tags"].iteritems():
                if val == max:
                    vars["tags"][key] = "xx-large"

                elif val > min + div * 2:
                    vars["tags"][key] = "large"

                else:
                    vars["tags"][key] = "small"

        else:
            self.set_flash("danger", "not-logged-in")
            self.redirect("/")

        vars["login_link"] = users.create_login_url("/")

        template = JINJA_ENVIRONMENT.get_template(self.template)
        self.response.write(template.render(vars))

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'merely remarkable came line',
}

app = webapp2.WSGIApplication([
    ('/tags', TagsHandler)
], debug = True, config = config)
