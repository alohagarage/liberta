import string
import random
import json
import logging
import os
import urllib

from google.appengine.api import urlfetch
from google.appengine.runtime import DeadlineExceededError
import webapp2
import jinja2

from models import Query

jinja_env = jinja2.Environment(autoescape=True, 
                                loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 
                                                                            'templates')))
HOSTNAME = 'lriserver.com'
PORT = '8000'

def query_in_db(query_id):
    """ Checks to see if this query has already been done """
    q = Query.gql("WHERE query_id = :1", query_id)
    if q.get():
        return q
    else:
        return False

def make_query_id(size=11, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def make_unique_qid():
    q_id = make_query_id()
    while query_in_db(q_id):
        q_id = make_query_id()
    return q_id

def query_to_db(query, params):
    """ Store new query in DB """
    query_id = make_unique_qid()
    q = Query(query_id = query_id, query = query, params = params)
    q.put()
    return q.query_id


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


class QueryHandler(Handler):
    def post(self):
        query = self.request.get('query')
        query = urllib.urlencode({'q': query,
            'opts': '{"use_cached":false}'}
            )
        logging.info("query: %s" % query)
        object_type = self.request.get('object_type')
        verb = self.request.get('verb')
        logging.info("object type: %s, verb: %s" % (object_type, verb))
        url = 'http://%s:%s/%s/%s?%s' % (HOSTNAME, 
                PORT, 
                object_type, 
                verb, 
                query)
        try:
            result = urlfetch.fetch(url=url, deadline=45)
        except DeadlineExceededError as e:
            logging.error("URL Fetch Error: %s" % e)
        logging.info("Made a query with this URL: %s" % url)
        result_json= result.content
        logging.info("Query result: %s" % result_json)
        self.response.headers.add_header('content-type', 
                'application/json', 
                charset='utf-8')
        self.response.out.write(result_json)


class SettingsHandler(Handler):
    def get(self):
        response = json.dumps({'hostname': HOSTNAME, 'port': PORT })
        self.response.headers.add_header('content-type', 
                'application/json', 
                charset='utf-8')
        self.response.out.write(response)

    def post(self):
        logging.info('POSTed these arguments: %s' % self.request.arguments())
        global HOSTNAME, PORT
        HOSTNAME = self.request.get('hostname')
        PORT = self.request.get('port')
        response = json.dumps({'hostname': HOSTNAME, 'port': PORT})
        logging.info('Response: %s' % response)
        self.response.headers.add_header('content-type', 
                'application/json', 
                charset='utf-8')
        self.response.out.write(response)


class QueryIdHandler(Handler):
    def post(self):
        query = self.request.get('query')
        params = self.request.get('params')
        q_id = query_to_db(query, params)
        q_id = json.dumps(q_id)
        logging.info('query saved to db')
        self.response.headers.add_header('content-type', 
                'application/json', 
                charset='utf-8')
        self.response.out.write(q_id)

    def get(self):
        """Generates a unique query_id"""
        query_id = make_unique_qid()
        self.response.headers.add_header('content-type', 
                'application/json', 
                charset='utf-8')
        self.response.out.write(query_id)


class ArchivedQueryHandler(Handler):
    def get(self):
        q_id = self.request.GET['query_id']
        r = query_in_db(q_id)
        response = json.dumps({'query': r.get().query, 
            'params': r.get().params,
            'created': r.get().created.strftime('%r, %m-%d-%y')})
        self.response.headers.add_header('content-type', 
                'application/json', 
                charset='utf-8')
        self.response.out.write(response)


class QueryURLHandler(Handler):
    def get(self, q_id):
        self.render("index.html", is_archived = 'true')
