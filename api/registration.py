class Registration(object):
	def __init__(self, email, password, password2):
		self.email = email
		self.password = password
		self.password2 = password2

	def check_email(self):
		pass

	def check_passwd(self):
		return True if self.password == self.password2 else False

	def save_user(self):
		return self.check_passwd()

	def _hash_password(self):
		pass