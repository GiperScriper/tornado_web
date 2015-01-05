import tornado.ioloop
import tornado.web
import json

from tornado.options import define, options

define('port', default=8889, help='run on the given port', type=int)

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		greeting = self.get_argument('greeting', 'default')

		self.set_header('Content-Type', 'application/json')
		self.write(json.dumps(greeting + ", Happy New Year!"))


class TestHandler(tornado.web.RequestHandler):
	def get(self, input):
		self.write("input: {0}".format(input))


application = tornado.web.Application([
	(r"/", MainHandler),
	(r"/test/(\w+)", TestHandler)
])

if __name__ == "__main__":	
	tornado.options.parse_command_line()
	application.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()