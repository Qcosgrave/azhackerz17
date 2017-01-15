import sys
import spotipy
import spotipy.util as util
import json

scope = 'user-top-read'

username = 'calvinm13'

token = util.prompt_for_user_token(username, scope, '8e5cac0ed299444480f463d1a662829f', '078527b8e4394a1c8efd5c07bce12568', 'http://localhost/')

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_top_artists()
    # print json.dumps(results, indent=2, sort_keys=True)
else:
    print "Can't get token for", username

artists = []

# Create simple list of artists
for item in results['items']:
    artists.append(item['name'])

print str(artists)
