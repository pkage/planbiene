import falcon
import json

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

api = falcon.API()
api.add_route('/quote', QuoteResource())
api.add_route('/spotify/config', SpotifyConfigResource())
