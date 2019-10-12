import falcon
import json

from falcon.http_status import HTTPStatus

class SilenceCORS(object):
    def process_request(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')
        resp.set_header('Access-Control-Max-Age', 1728000)  # 20 days
        if req.method == 'OPTIONS':
            raise HTTPStatus(falcon.HTTP_200, body='\n')


class SpotifyConfigResource:
    def on_get(self, req, resp):
        """send over the client_id"""

        # this probably isn't good
        secrets = json.load(open('secrets.json', 'r'))

        resp.media = {
            'client_id': secrets['client_id']
        }
        

class QuoteResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        quote = {
            'quote': (
                "I've always been more interested in "
                "the future than in the past."
            ),
            'author': 'Grace Hopper'
        }

        resp.media = quote

api = falcon.API(middleware=[SilenceCORS()])
api.add_route('/quote', QuoteResource())
api.add_route('/spotify/config', SpotifyConfigResource())
