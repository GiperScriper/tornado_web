"""Notes Structure:

db.notes.insert({
    "title":"My First Note",
    "body": "<p>some text</p>",
    "author": "Toby Segaran",
    "tags": ["python", "web"],
    "date_added":1310248056,
    "date_modified":1310248057,
})

"""
import tornado.ioloop
import tornado.web
import tornado.escape

import pymongo
import json
import time
import logging as logger
import base64, uuid

import settings

from bson.json_util import dumps
from bson.objectid import ObjectId

from tornado.options import define, options
from api.db import *
from api.registration import Registration

define('port', default=8889, help='run on the given port', type=int)



class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_secure_cookie("hekko", "MySecureCookie")
        cookie = self.get_secure_cookie("hekko")
        print "Cookie %s" % cookie
        self.render('notes/index.html', cookie=cookie)


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('notes/login.html')


class RegistrationHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        self.write(data)
        result = Registration(data['email'], data['password'], data['password2'])
        print result.save_user()


class NotesHandler(tornado.web.RequestHandler):     
    def get(self, _id=None): 
        uri = self.request.uri
        method = self.request.method
        print uri
        try:
            result, status_code = get_note_or_notes(_id, method)
            
            self.set_header('Content-Type', 'application/json')
            self.set_status(status_code)
            self.write(result)
        
        except Exception as e:
            self.set_header('Content-Type', 'application/json')            
            self.set_status(400)
            self.write({'error_message': '{0}'.format(e)})
        #self.render('notes/notes.html', notes=notes)

    
    def post(self): 
        try:
            data = json.loads(self.request.body)
            result, status_code = create_note(data)

            self.set_header('Content-Type', 'application/json')
            self.set_status(status_code)
            self.write(result)

        except Exception as e:
            self.set_header('Content-Type', 'application/json')            
            self.set_status(400)
            self.write({'error_message': '{0}'.format(e)})
        

    def put(self, _id=None):
        coll = self.application.db.notes
        data = json.loads(self.request.body)


    
    def delete(self, _id=None):
        try:            
            result, status_code = delete_note(_id)
            
            self.set_header('Content-Type', 'application/json')
            self.set_status(status_code)
            self.write(result)
        
        except Exception as e:
            self.set_header('Content-Type', 'application/json')
            self.set_status(400)
            self.write({'error_message': '{0}'.format(e)})


class Application(tornado.web.Application):
    def __init__(self):
        handlers = ROUTES       
        config = {
            "template_path": settings.TEMPLATE_PATH,
            "static_path": settings.STATIC_PATH,       
            "debug": True,
            "cookie_secret": base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
        }
        #conn = pymongo.Connection("localhost", 27017)
        #self.db = conn["notes"]
        tornado.web.Application.__init__(self, handlers, **config)


ROUTES = [
    (r"/index", IndexHandler),
    (r"/", LoginHandler),
    (r"/notes", NotesHandler),
    (r"/notes/(.*)", NotesHandler),
    (r"/register", RegistrationHandler)
]


if __name__ == "__main__":  
    tornado.options.parse_command_line()
    http_server = Application()
    http_server.listen(options.port)
    logger.info('Tornado server is running..')
    tornado.ioloop.IOLoop.instance().start()