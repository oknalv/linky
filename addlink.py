import webapp2
from base import BaseHandler
from link import Link, Container
from google.appengine.api import users
import time

class AddLinkHandler(BaseHandler):
    def __init__(self, request = None, response = None):
        self.initialize( request, response )

    def post(self):
        user = users.get_current_user()
        if user:
            containers = Container.query(Container.user == user)
            cont = None
            if not containers.iter().has_next():
                cont = Container(user = user)
                cont.put()
            else:
                cont = containers.iter().next()
            check = True
            for link in cont.links:
                if link.name == self.request.get("name"):
                    check = False
                    break

            if check:
                url = self.request.get("url")
                url = url if url.startswith("http://") or url.startswith("https://") else "http://" + url
                cont.links.append(Link(name = self.request.get("name"), url = url, tags = self.request.get("tags")))
                cont.put()
                time.sleep(1)
            else:
                self.set_flash("danger", "duplicated-name")

            self.redirect("/")

        else:
            self.set_flash("danger", "not-logged-in")
            self.redirect("/")

    def get(self):
        self.set_flash("danger", "forbidden-access")
        self.redirect("/")

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'merely remarkable came line',
}

app = webapp2.WSGIApplication([
    ('/addlink', AddLinkHandler)
], debug = True, config = config)