from flask import Flask, render_template,request,redirect,url_for,session,send_from_directory
import requests
import json
from spotify_code import *
from boto.s3.connection import S3Connection
import os
s3 = S3Connection(os.environ.get('app_secret_key'), os.environ.get('CLI_ID'))
#4 lines below for testing only
#import authorise_keys
#CLI_ID = authorise_keys.CLI_ID
#CLI_SEC = authorise_keys.CLI_SEC
#app_secret_key = authorise_keys.app_secret_key
#use in heroku


app = Flask(__name__)
app.secret_key = authorise_keys.app_secret_key
API_BASE = 'https://accounts.spotify.com'
REDIRECT_URI = "https://myspotifyquiz.herokuapp.com/api_callback"
SHOW_DIALOG = False
#what the spotify app is allowed to do
SCOPE = 'playlist-read-private,user-library-read'

@app.route('/favicon.ico')
def favicon():
    favicon = '/img/favicon.ico'
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico',mimetype='/img/favicon.ico')

@app.route("/")
def load_home():

    return render_template('home.html')


# authorization-code-flow Step 1. Have your application request authorization;
# the user logs in and authorizes access
@app.route("/verify")
def verify():
    auth_url = f'{API_BASE}/authorize?client_id={CLI_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}&show_dialog={SHOW_DIALOG}'
    return redirect(auth_url)
# authorization-code-flow Step 2.
# Have your application request refresh and access tokens;
# Spotify returns access and refresh tokens
@app.route("/api_callback")
def api_callback():
    session.clear()
    code = request.args.get('code')

    auth_token_url = f"{API_BASE}/api/token"
    res = requests.post(auth_token_url, data={
        "grant_type":"authorization_code",
        "code":code,
        "redirect_uri":REDIRECT_URI,
        "client_id":CLI_ID,
        "client_secret":CLI_SEC
        })

    res_body = res.json()
    session["toke"] = res_body.get("access_token")

    #redirects to loading which is just an empty html that says loading
    #this is so user can't press login multiple time which would cause multiple graph.html to be loaded which is a slow process
    return redirect("select_type")

@app.route("/select_type",methods=['POST','GET'])
def get_type():
        if request.method == 'POST':
            response = request.get_json()
            session['type'] = response['type']
            return session['type']
        else:
            return render_template('select_type.html')

@app.route("/search/<error_message>", methods=['POST','GET'])
def get_artist_post(error_message):
    type = session.get('type')
    if request.method == 'POST':
        text = request.form['text']
        processed_text = text.upper()
        print(processed_text)
        return redirect(url_for('select_artist', data = processed_text,))
    else:
        return render_template('search.html',type=type,error_message=error_message)

#addded the /artist/ to stop people stumbling onto pages they're not meant to
#ie if they entered end_page it would take them to the end page
@app.route('/select/<data>', methods=['POST','GET'])
def select_artist(data):
    type = None
    if (type == None):
        type = session.get('type')

    if request.method == 'POST':
        response = request.get_json()
        session['id'] = response['chosen_id']
        return render_template('loading.html')
    else:
        print(type)
        auth = spotipy.Spotify(auth=session['toke'])
        get_artist_or_playlist = search_for_artist_or_playlist(auth, data,type)
        if (len(get_artist_or_playlist) > 0):
            get_artist = json.dumps(get_artist_or_playlist)
            return render_template('select_from_search.html',data = get_artist, type = type)
        else:
            return redirect(url_for('get_artist_post', error_message ="cannot find any " +str(type)+ " with that name"))


@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/quiz_page')
def pass_to_quiz():
    id = session.get('id')
    type = session.get('type')
    auth = spotipy.Spotify(auth=session['toke'])

    #print(type)
    if (type == "artists"):
        json_data= get_tracks(auth,id)
    if (type == "playlists"):
        json_data = get_tracks_for_playlist_or_saved(auth,id,type)
    if type == "saved_songs":
        json_data = get_tracks_for_playlist_or_saved(auth,None,type)

    if (len(json_data)<11):
        errormessage = "that " + str(type) + " only has " + str(len(json_data)) + " songs"
        return redirect(url_for('get_artist_post', error_message=errormessage))
    else:
        return render_template('quiz_page.html', data = json_data)


if __name__ == "__main__":
    #to run on loacal machine change line 14 to
    #REDIRECT_URI = "http://127.0.0.1:5000/api_callback"
    #to run on heroku
    #REDIRECT_URI = "https://myspotifyquiz.herokuapp.com/api_callback"
    app.run(debug=False)
