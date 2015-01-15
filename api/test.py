a = ['title', 'body', 'tags']
b = {'title':'main', 'body':'sometest'}

result = { key:(b[key] if key in b.keys() else None) for key in a }


import bcrypt
print bcrypt.hashpw('123', '$2a$12$37qs4pLr.RU06QfWuRjcL.f2xEurgVotVOUtwzQkWfpvegRtXT0DC') \
	== '$2a$12$37qs4pLr.RU06QfWuRjcL.f2xEurgVotVOUtwzQkWfpvegRtXT0DC'

f = {1:1, 2:2}
print any(f), all(f)