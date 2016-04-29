import webapp2
from base import BaseHandler
from link import Link, Container
from google.appengine.api import users
import time

class MoveDownHandler(BaseHandler):
    def __init__(self, request = None, response = None):
        self.initialize( request, response )

    def get(self):
        if not self.request.get("id"):
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

                actual = None
                for ind, link in enumerate(cont.links):
                    if link.name == self.request.get("id"):
                        actual = ind
                        break

                if actual is not None and actual < len(cont.links):
                    cont.links[actual], cont.links[actual + 1] = cont.links[actual + 1], cont.links[actual]
                    cont.put()
                    time.sleep(1)

                self.redirect("/")

            else:
                self.set_flash("danger", "not-logged-in")
                self.redirect("/")

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'merely remarkable came line',
}

app = webapp2.WSGIApplication([
    ('/movedown', MoveDownHandler)
], debug = True, config = config)