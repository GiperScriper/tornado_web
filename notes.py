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

from tornado.options import define, options

import pymongo

import settings

define('port', default=8889, help='run on the given port', type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('notes/index.html')


class NotesHandler(tornado.web.RequestHandler):
    def get(self):
        coll = self.application.db.notes
        notes = coll.find()
        self.render('notes/notes.html', notes=notes)
     


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
    (r"/notes", NotesHandler)
]


if __name__ == "__main__":  
    tornado.options.parse_command_line()
    http_server = Application()
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()