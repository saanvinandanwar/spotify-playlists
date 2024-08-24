# spotify-playlists

Automatically adds Discovery Weekly songs to one playlist

Steps to Code -- Program Planning

Go to spotify api > playlists > get playlist items
Need one required parameter, need the playlist id
To get playlist id, we should "get current user's playlists", which will give us all the playlist ids
Need to get all playlists, giving us the names and ids. then find discovery weekly playlist, get id of that, and use the id to get items in the playlist
Need to be able to add the songs to a new playlist, "saved weekly"
Check if it exists, if not create one, if it does get its id via the API
"Create playlist" if it doesn't exist
then the "add items to playlist" section, putting them into playlist from the discover weekly
to add songs, we need the URIs, and so we get them from each track
when we get the songs from "get playlist items", we have the URI, so we pull them from the playlist, save it, and then add it to another playlist
create list of URIs and then save to new playlist
OAuth -- need to implement it and have the user's permission

also need an OAuth token
can go to Spotify Api console to see what data returns look like >> what kind of info we get back on the playlists >> play around with it, get more familiar


Installing packages/modules
terminal >> /usr/bin/python3 pip install <package_name>

to run >> python3 spotifyWeekly.py


incase the port is busy, go to terminal 
 - to see if anyhting is running >> lsof -i :<port number>    ex. lsof -i :5000
 - to delete >> kill -9 <process id number>