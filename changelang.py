import webapp2
from base import BaseHandler

class ChangeLangHandler(BaseHandler):
    def __init__(self, request = None, response = None):
        self.initialize( request, response )

    def get(self):
        self.session["lang"] = self.request.get("id","en")
        self.redirect(self.request.referer)

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'merely remarkable came line',
}

app = webapp2.WSGIApplication([
    ('/changelang', ChangeLangHandler)
], debug = True, config = config)