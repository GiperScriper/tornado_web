a = ['title', 'body', 'tags']
b = {'title':'main', 'body':'sometest'}

result = { key:(b[key] if key in b.keys() else None) for key in a }
print test