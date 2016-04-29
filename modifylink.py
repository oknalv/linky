import webapp2
from base import BaseHandler
from link import Link, Container
from google.appengine.api import users
import time

class ModifyLinkHandler(BaseHandler):
    def __init__(self, request = None, response = None):
        self.initialize( request, response )

    def post(self):
        if not self.request.get("name") or not self.request.get("newName") or not self.request.get("url"):
            self.set_flash("danger", "forbidden-access")
            self.redirect("/")
        else:
            user = users.get_current_user()
            if user:
                containers = Container.query(Container.user == user)
                cont = None
                if not containers.iter().has_next():
                    cont = Container(user = user)
                    cont.put()
                else:
                    cont = containers.iter().next()

                check = False
                if self.request.get("name") != self.request.get("newName"):
                    for ind, link in enumerate(cont.links):
                        if link.name == self.request.get("newName"):
                            check = True
                            self.set_flash("danger", "duplicated-name")
                            self.redirect("/")

                if not check:
                    url = self.request.get("url")
                    url = url if url.startswith("http://") or url.startswith("https://") else "http://" + url
                    for ind, link in enumerate(cont.links):
                        if link.name == self.request.get("name"):
                            cont.links[ind] = Link(name = self.request.get("newName"), url = url, tags = self.request.get("tags"))
                            break

                    cont.put()
                    time.sleep(1)
                    self.set_flash("success", "link-modified")
                    self.redirect("/")

            else:
                self.set_flash("danger", "not-logged-in")
                self.redirect("/")

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'merely remarkable came line',
}

app = webapp2.WSGIApplication([
    ('/modifylink', ModifyLinkHandler)
], debug = True, config = config)