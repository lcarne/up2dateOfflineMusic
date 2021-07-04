from django.shortcuts import render
import requests


# Create your views here.
def index(request):
    return render(request, 'test.html')


def profile(request):
    return render(request, 'profile.html')


def active_up2date(request):
    # LOOK FOR A PLAYLIST NAMED up2DateOfflineMusic
    playlists_endpoint = 'https://api.deezer.com/user/me/playlists'
    tracks_endpoint = 'https://api.deezer.com/user/me/tracks'
    playlist_name = 'up2DateOfflineMusic'
    # Data to be sent to api
    access_token = request.user.social_auth.get(provider='deezer').extra_data.get('access_token')
    params = {'access_token': access_token,
              'limit': 1}
    # To be sure to get all the playlists
    params = {'access_token': access_token,
              'limit': requests.get(url=playlists_endpoint, params=params).json()['total']}

    # sending post request and saving response as response object
    # IF MULTIPLE TAKE THE FIRST ONE ONLY
    playlist_id = 0
    for i in requests.get(url=playlists_endpoint, params=params).json()['data']:
        if i.get('title') == playlist_name:
            playlist_id = i.get('id')
            break

    if playlist_id == 0:
        playlist_id = requests.post(url=playlists_endpoint,
                                    data={'access_token': access_token, 'title': playlist_name}).json().get('id')

    # GET THE TOTAL NUMBER OF FAVORITES MUSICS AND THE LAST 50 ONES
    # defining a params dict for the parameters to be sent to the API
    # to get the total number of favorite tracks
    # sending get request and saving the response as response object
    # and extracting total number of favorite tracks

    nb_tracks = requests.get(url=tracks_endpoint, params={'access_token': access_token,
                                                          'limit': 1}).json()['total']

    # defining a params dict for the parameters to be sent to the API
    # to get the TracksNumber last favorite tracks
    # sending get request and saving the response as response object
    # and extracting data from json format

    favorite_tracks = [str(i) for i in [elem.get('id') for elem in
                                        requests.get(url=tracks_endpoint, params={'access_token': access_token,
                                                                                  'index': nb_tracks - 50,
                                                                                  'limit': 50}).json()['data']]]

    playlist_id_endpoint = f'https://api.deezer.com/playlist/{str(playlist_id)}/tracks'

    # To be sure to get all the songs in the playlist
    nb_tracks = requests.get(url=playlist_id_endpoint,
                             params={'access_token': access_token, 'limit': 1}).json().get('total')

    params = {'access_token': access_token, 'index': 0, 'limit': nb_tracks}

    # sending get request and saving the response as response object
    # and extracting data from json format

    playlist_tracks = [str(i) for i in [elem['id'] for elem in
                                        requests.get(url=playlist_id_endpoint,
                                                     params={'access_token': access_token,
                                                             'index': 0, 'limit': nb_tracks}).json()['data']]]

    # playlist track ids not in the last 50 favorites music
    tracks_to_delete = [x for x in playlist_tracks if x not in favorite_tracks]

    # New favorites not in the playlist
    tracks_to_add = [x for x in favorite_tracks if x not in playlist_tracks]

    # DELETE SONGS IN THE PLAYLIST
    requests.delete(url=playlist_id_endpoint, params={'access_token': access_token, 'songs': ','.join(tracks_to_delete)})

    # POST SONGS TO THE PLAYLIST
    requests.post(url=playlist_id_endpoint, data={'access_token': access_token, 'songs': ','.join(tracks_to_add)})
    return render(request, 'profile.html')
