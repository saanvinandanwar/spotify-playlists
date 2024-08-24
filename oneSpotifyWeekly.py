#THIS ONLY WORKS IF DISCOVER WEEKLY IS SHOWN ON YOUR PROFILE 
#WANT TO LEARN ABOUT FOLDER MANIPULATION TOO 
#HOW CAN I DO IF ITS NOT IN MY PROFILE AND PUBLIC, AND SAVE STUFF TO A FOLDER 

#date - august 23rd, 2024

import spotipy
import time 
import webbrowser
from spotipy.oauth2 import SpotifyOAuth 

from flask import Flask, request, url_for, session, redirect

app = Flask(__name__) #using flask for OAuth, to automate process 

#want to store the token value so we can keep signing in 
app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = 'sdkjfskhioq23pihewojrnfksjd' #to prevent unauthorized access 

TOKEN_INFO = 'token_info' #where we want to store the token info 

@app.route('/') #home route
def login():
    auth_url = create_spotify_oauth().get_authorize_url() #will generate an authorization url 
    return redirect(auth_url)

@app.route('/callback')
def callback(): #calls this function when we hit the redirect url from the first route 
    session.clear() #clears any existing sessions and data 
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code) #get_access_token method exchanges auth code for a token 
    session[TOKEN_INFO] = token_info
    return redirect(url_for('save_discover_weekly', external=True))

@app.route('/saveDiscoverWeekly')
def save_discover_weekly(): #called when we go to this route 
    #want to first get the token info 

    try: 
        token_info = get_token()
    except: 
        print("User not logged in")
        return redirect('/')
    #return("OAUTH SUCCESSFUL")

    #PART THAT SAVES THE DISCOVER WEEKLY TO THE BIG WEEKLY PLAYLIST
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_id = sp.current_user()['id']
    
    discover_weekly_playlist_id = None
    saved_weekly_playlist_id = None #since it didn't exist for the first time 

    current_playlists = sp.current_user_playlists() #going to return the entire object
    #want to loop through the list and find playlist where the name matches
    for playlist in current_playlists['items']:
        print(f"Found playlist: {playlist['name']}")
        if (playlist['name'] == "Discover Weekly"):
            discover_weekly_playlist_id = playlist['id'] #finds id for discover weekly playlist
        if (playlist['name'] == "Saved Weekly"): #does same for saved weekly, assuming its made
            saved_weekly_playlist_id = playlist['id']
    if not discover_weekly_playlist_id:  
        return 'Discover Weekly key not found'
    if not saved_weekly_playlist_id: #create new playlist 
        new_playlist = sp.user_playlist_create(user_id, "Saved Weekly", public=True)
        saved_weekly_playlist_id = new_playlist['id'] #any empty playlist 
        
    
    discover_weekly_playlist = sp.playlist_items(discover_weekly_playlist_id)
    song_uris = [] #want to take tracks from discover weekly and add to list
    for song in discover_weekly_playlist['items']: #looping through each song
        song_uri = song['track']['uri'] #targeting song by uri
        song_uris.append(song_uri)
    sp.playlist_add_items(saved_weekly_playlist_id, song_uris)
    return("SUCCESS!!!!")


def get_token():
    token_info = session.get(TOKEN_INFO, None) #retrieves the token 
    #if token doesn't exist, redirect to login with oauth 
    if not token_info:
        return redirect(url_for('login', external=False))
    
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60 #checking 60 seconds, if it happens to expire soon 
    if (is_expired):
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info


def create_spotify_oauth(): #function to create spotify oauth
    #get client id from spotify dashboard
    return SpotifyOAuth(client_id = "a72f8461ef054ec09214622684f1ecdd",
                        client_secret = "b5df371313104a5db231fb7bc4fadba6",
                        redirect_uri = url_for('callback', _external=True),
                        scope = 'user-library-read playlist-modify-public playlist-modify-private' ) #project specific

if __name__ == '__main__': #so that it automatically opens into a webpage
    webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=True)