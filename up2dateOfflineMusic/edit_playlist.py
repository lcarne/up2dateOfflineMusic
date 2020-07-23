from settings import *
#from get_playlist import PlaylistId
from get_tracks import PlaylistId, TracksFavorite

# GET SONGS ON THE PLAYLIST

# defining the api-endpoint

Url = 'https://api.deezer.com/playlist/' + str(PlaylistId) + '/tracks'

# data to be sent to api
Params = {'access_token': AccessToken,
          'limit':1}

# To be sure to get all the songs in the playlist
Total = requests.get(url=Url, params=Params).json()['total']

Params = {'access_token': AccessToken, 'index': 0, 'limit': Total}

# sending get request and saving the response as response object
# and extracting data from json format

TracksPlaylist = [str(i) for i in [elem['id'] for elem in
                  requests.get(url=Url, params=Params).json()['data']]]

# playlist track ids not in the last 50 favorites music

TracksToDelete = [x for x in TracksPlaylist if x not in TracksFavorite]

# New favorites not in the playlist

TracksToAdd = [x for x in TracksFavorite if x not in TracksPlaylist]

# DELETE SONGS IN THE PLAYLIST
# data to be sent to api

Params = {'access_token': AccessToken,
          'songs': ','.join(TracksToDelete)}

requests.delete(url=Url, params=Params)

# POST SONGS TO THE PLAYLIST

# data to be sent to api

Data = {'access_token': AccessToken, 'songs': ','.join(TracksToAdd)}

# sending post request 

requests.post(url=Url, data=Data)
