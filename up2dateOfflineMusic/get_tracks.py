from settings import *
from get_playlist import PlaylistId

# GET THE TOTAL NUMBER OF FAVORITES MUSICS AND THE LAST 50 ONES
# defining a params dict for the parameters to be sent to the API
# to get the total number of favorite tracks

# api-endpoint
Url = 'https://api.deezer.com/user/me/tracks'

Params = {'access_token': AccessToken,
    'limit': 1
          }

# sending get request and saving the response as response object
# and extracting total number of favorite tracks

Total = requests.get(url=Url, params=Params).json()['total']

# defining a params dict for the parameters to be sent to the API
# to get the TracksNumber last favorite tracks

Params = {'access_token': AccessToken, 
          'index': Total - TracksNumber,
          'limit': TracksNumber}


# sending get request and saving the response as response object
# and extracting data from json format

TracksFavorite = [str(i) for i in [elem['id'] for elem in
                  requests.get(url=Url, params=Params).json()['data']]]