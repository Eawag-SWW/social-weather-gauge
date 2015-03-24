
from instagram.client import InstagramAPI

import secrets

CLIENT_ID = secrets.INSTAGRAM_CLIENT_ID
CLIENT_SECRET = secrets.INSTAGRAM_CLIENT_SECRET

api = InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)


