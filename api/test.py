a = ['title', 'body', 'tags']
b = {'title':'main', 'body':'sometest'}

result = { key:(b[key] if key in b.keys() else None) for key in a }


import bcrypt


print bcrypt.hashpw('123')

