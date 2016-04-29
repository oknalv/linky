import webapp2
from webapp2_extras import sessions

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()

    def set_flash(self, type, message_tag):
        if not self.session.get("flash"):
            self.session["flash"] = []

        self.session["flash"].append([type, message_tag])

    def get_flash(self):
        ret = self.session.get("flash")
        self.session["flash"] = []
        return ret