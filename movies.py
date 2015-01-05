import tornado.ioloop
import tornado.web

from tornado.options import define, options

import settings

define('port', default=8889, help='run on the given port', type=int)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('movie/index.html')


class MovieHandler(tornado.web.RequestHandler):
	def post(self):
		name = self.get_argument('name', None)
		rating = self.get_argument('rating', None)
		self.render('movie/movie.html', name=name, rating=rating)

# routes
ROUTES = [
	(r"/", IndexHandler),
	(r"/movie", MovieHandler)
]

application = tornado.web.Application(
	handlers=ROUTES,	
	template_path=settings.TEMPLATE_PATH,
	static_path=settings.STATIC_PATH,
	debug=True # this mode restart server on change
)

if __name__ == "__main__":	
	tornado.options.parse_command_line()
	application.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()