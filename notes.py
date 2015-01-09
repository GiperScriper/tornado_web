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

import pymongo
import json
import time
import logging as logger

import settings

from bson.json_util import dumps
from bson.objectid import ObjectId

from tornado.options import define, options
from api.db import *

define('port', default=8889, help='run on the given port', type=int)



class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('notes/index.html')


class NotesHandler(tornado.web.RequestHandler):     
    def get(self, _id=None): 
        try:
            result = get_note_or_notes(_id)
            
            self.set_header('Content-Type', 'text2/html')
            self.set_status(200)
            self.write(result)
        
        except Exception as e:
            self.set_header('Content-Type', 'text2/html')            
            self.set_status(400)
            self.write({'error_message': '{0}'.format(e)})
        #self.render('notes/notes.html', notes=notes)

    
    def post(self): 
        notes_fields = ['title', 'body', 'author', 'tags']
        
        coll = self.application.db.notes
        data = json.loads(self.request.body)        
        data.update({'date_added': int(time.time())}) 
        coll.insert(data)
        
        self.set_header('Content-Type', 'application/json')
        self.set_status(201)
        self.write(dumps(data))


    def put(self, _id=None):
        coll = self.application.db.notes
        data = json.loads(self.request.body)


    
    def delete(self, _id=None):
        try:            
            if _id:
                coll = self.application.db.notes
                note = coll.find_one({"_id": ObjectId(_id)})
                coll.remove({"_id": ObjectId(_id)})
                status_code = 204 if note else 404
                print note
                self.set_header('Content-Type', 'application/json')
                self.set_status(status_code)
                self.write(dumps(note))
        
        except Exception as e:
            self.set_header('Content-Type', 'application/json')
            self.set_status(400)
            self.write({'error_message': '{0}'.format(e)})

    


class Application(tornado.web.Application):
    def __init__(self):
        handlers = ROUTES       
        config = dict(
            template_path=settings.TEMPLATE_PATH,
            static_path=settings.STATIC_PATH,       
            debug=True
        )
        conn = pymongo.Connection("localhost", 27017)
        self.db = conn["notes"]
        tornado.web.Application.__init__(self, handlers, **config)


ROUTES = [
    (r"/", IndexHandler),
    (r"/notes", NotesHandler),
    (r"/notes/(.*)", NotesHandler)
]


if __name__ == "__main__":  
    tornado.options.parse_command_line()
    http_server = Application()
    http_server.listen(options.port)
    logger.info('Tornado server is running..')
    tornado.ioloop.IOLoop.instance().start()