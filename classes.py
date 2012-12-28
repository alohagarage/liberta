import os

from google.appengine.api import urlfetch
from google.appengine.runtime import DeadlineExceededError
import webapp2
import jinja2

jinja_env = jinja2.Environment(autoescape=True, 
                                loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 
                                                                            'templates')))

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class MainHandler(Handler):
    def get(self):
        self.render("index.html")
