from google.appengine.ext import ndb

class Link(ndb.Model):
    url = ndb.StringProperty(required = True)
    name = ndb.StringProperty(required = True)
    tags = ndb.StringProperty(required = True)

class Container(ndb.Model):
    user = ndb.UserProperty(required = True)
    links = ndb.StructuredProperty(Link, repeated = True)