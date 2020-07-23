from settings import *

# LOOK FOR A PLAYLIST NAMED up2DateOfflineMusic

Url = 'https://api.deezer.com/user/me/playlists'

# data to be sent to api
Params = {'access_token': AccessToken,
          'limit':1}

# To be sure to get all the playlists
Total = requests.get(url=Url, params=Params).json()['total']

Params = {'access_token': AccessToken,
          'limit':Total}

# sending post request and saving response as response object
# IF MULTIPLE TAKE THE FIRST ONE ONLY

PlaylistId = 0
for Item in requests.get(url=Url, params=Params).json()['data']:
    if Item['title'] == PlaylistName:
        PlaylistId = Item['id']
        break

# If it doesn't exist it CREATEs A PLAYLIST and GET its Id

if PlaylistId == 0:

    # defining the api-endpoint

    Url = 'https://api.deezer.com/user/me/playlists'

    # data to be sent to api

    Data = {'access_token': AccessToken, 'title': PlaylistName}

    # sending post request and saving response as response object

    PlaylistId = requests.post(url=Url, data=Data).json()['id']