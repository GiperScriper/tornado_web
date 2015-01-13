import time

from db import db_open_close
from config import UserKeys

class Registration(object):
	def __init__(self, email, password, re_password):
		self.email = email
		self.password = password
		self.re_password = re_password

	def check_email(self):
		pass

	def check_passwd(self):
		return True if str(self.password) == str(self.re_password) else False

	@db_open_close
	def save_user(self, db=None):
		data = {
			UserKeys.Email: self.email,
			UserKeys.Hash: self.password + 'hash@#$',
			UserKeys.DateCreated: int(time.time()),
			UserKeys.Notes: []
		}
		db.notes.insert(data)
		return data

	def _hash_password(self):
		pass