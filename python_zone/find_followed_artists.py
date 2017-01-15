import sys
import os
import spotipy
import spotipy.util as util
import json

scope = 'user-follow-read'

username = 'calvinm13'

token = util.prompt_for_user_token(username, scope, '8e5cac0ed299444480f463d1a662829f', '078527b8e4394a1c8efd5c07bce12568', 'http://localhost/')

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_followed_artists()
    # print json.dumps(results, indent=2, sort_keys=True)
else:
    print "Can't get token for", username

artists = []

# Create simple array of artists
for item in results['artists']['items']:
    artists.append(item['name'])

for item in artists:
    os.system("python find_events.py '" + item + "'")
