import tornado.ioloop
import tornado.web

from tornado.options import define, options

import settings
import pymongo

define('port', default=8889, help='run on the given port', type=int)


class WordHandler(tornado.web.RequestHandler):
    def get(self, word):
        coll = self.application.db.words
        word_doc = coll.find_one({"word": word})
        if word_doc:
            del word_doc["_id"]
            self.write(word_doc)
        else:
            self.set_status(404)
            self.write({"error": "word not found"})

    def post(self, word):
        coll = self.application.db.words
        definition = self.get_argument('definition', None)        
        if word and definition:
            coll.insert({'word': word, 'definition': definition})
            self.write(word + ',' + definition)
        else:
            self.set_status(200)
            self.write({"error" : "Not enough data"})


class Application(tornado.web.Application):
    def __init__(self):
        handlers = ROUTES
        template_path = settings.TEMPLATE_PATH
        static_path = settings.STATIC_PATH
        conn = pymongo.Connection("localhost", 27017)
        self.db = conn["example"]
        tornado.web.Application.__init__(self, handlers, debug=True)

ROUTES = [
    (r"/(\w+)", WordHandler)
]


if __name__ == "__main__":  
    tornado.options.parse_command_line()
    http_server = Application()
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()