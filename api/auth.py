import bcrypt

from decorators import db_open_close
from constants import UserKeys


class Auth(object):
	def __init__(self, email, password):
		self.email = email
		self.password = password

	def verify_user(self, hash):
		return bcrypt.hashpw(self.password, hash) == hash

	@db_open_close
	def find_user_by_email(self, db=None):
		user = db.notes.find_one(
			{ UserKeys.Email: self.email }, 
			{ UserKeys.Email: True, UserKeys.Hash: True }
		)
		return user if user else False