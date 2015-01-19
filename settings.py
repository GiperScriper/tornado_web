import os.path
import base64, uuid

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates')
STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')

COOKIE_SECRET = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)