#very basic structure, just for the OAuth to get working 
#from this skeleton we can do other things, like a spotifyWeekly, daylist saving, etc.
#want to create different branches so that we can have a bunch of different versions, or maybe just a bunch of files to make it easier 

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
    return("OAUTH SUCCESSFUL")


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