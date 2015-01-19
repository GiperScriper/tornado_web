"""Notes Structure:

db.notes.insert({
    "first"
    lastname
    notes: [
    {"title":"My First Note",
    "body": "<p>some text</p>",
    "author": "Toby Segaran",
    "tags": ["python", "web"],
    "date_added":1310248056,
    "date_modified":1310248057,},
    {},

    ]
})

"""
import tornado.ioloop
import tornado.web
import tornado.escape

import pymongo
import json
import time
import logging as logger

import settings

from bson.json_util import dumps
from bson.objectid import ObjectId

from tornado.options import define, options

from api.db import *
from api.registration import Registration
from api.auth import Auth
from api.constants import UserKeys

define('port', default=8889, help='run on the given port', type=int)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user = self.get_secure_cookie("user")
        return user


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.authenticated
    def get(self):
        #self.set_secure_cookie("hekko", "MySecureCookie")
        #cookie = self.get_secure_cookie("hekko")
        self.render('notes/index.html')
        #with open('templates/notes/index.html', 'r') as file:
        #    self.write(file.read())



class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('notes/login.html')


class AuthHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        
        user = Auth(
            data[UserKeys.Email],
            data[UserKeys.Password]
        )

        user_data = user.find_user_by_email()

        if user_data:
            if user.verify_user(user_data[UserKeys.Hash]):
                print "User auth"
                self.set_secure_cookie(
                    UserKeys.User,
                    user_data[UserKeys.Email]
                )
                self.redirect('/index')
            else:
                print "password dont match"


class RegistrationHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        status = {}
        status_code = 400        
        
        result = Registration(
            data[UserKeys.Email], 
            data[UserKeys.Password], 
            data[UserKeys.RePassword]
        )
        
        if result.check_unique_email():
            if result.check_password():
                result.save_user()
                status['message'] = 'complete registration'
                status_code = 201
            else:
                status['error_message'] = "passwords doesn't match"
        else:
            status['error_message'] = 'email already exist'

        self.set_header('Content-Type', 'application/json')            
        self.set_status(status_code)
        self.write(status)


class NotesHandler(tornado.web.RequestHandler):     
    def get(self, _id=None): 
        uri = self.request.uri
        method = self.request.method
        #print uri
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
            "cookie_secret": settings.COOKIE_SECRET,
            "login_url": "/"
        }
        #conn = pymongo.Connection("localhost", 27017)
        #self.db = conn["notes"]
        tornado.web.Application.__init__(self, handlers, **config)


ROUTES = [
    (r"/index", IndexHandler),
    (r"/", LoginHandler),
    (r"/auth", AuthHandler),
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