import time
import bcrypt

from db import db_open_close
from config import UserKeys


class Registration(object):
	def __init__(self, email, password, re_password):
		self.email = email
		self.password = password
		self.re_password = re_password

	
	@db_open_close
	def check_unique_email(self, db=None):
		email = db.notes.find_one({UserKeys.Email: self.email}, {UserKeys.Email: True})
		return True if not email else False 

	
	def check_password(self):
		return True if str(self.password) == str(self.re_password) else False

	
	@db_open_close
	def save_user(self, db=None):
		data = {
			UserKeys.Email: self.email,
			UserKeys.Hash: self._get_hashed_password(self.password),
			UserKeys.DateCreated: int(time.time()),
			UserKeys.Notes: []
		}
		db.notes.insert(data)
		return data

	
	def _get_hashed_password(self, password):
		return bcrypt.hashpw(password, bcrypt.gensalt(4))


# if bcrypt.hashpw(password, hashed) == hashed:
#...     print("It Matches!")
#... else:
#...     print("It Does not Match :(")