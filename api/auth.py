import bcrypt

from db import db_open_close


class Auth(object):
	def __init__(self, email, password):
		self.email = email
		self.password = password

	def auth_user(self, db=None):
		pass

	def verify_email(self, db=None):
		pass