import os
from dotenv import load_dotenv
from flask import Flask, request, redirect, session, url_for, render_template
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import plotly.express as px

def main():
    app = create_app()
    app.run(port=8000, debug=True)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(64)
    load_dotenv()

    @app.route('/')
    def home():
        sp_oauth = create_spotify_oauth()
        if not sp_oauth.validate_token(sp_oauth.cache_handler.get_cached_token()):
            auth_url = sp_oauth.get_authorize_url()
            return redirect(auth_url)
        return redirect(url_for('top_tracks'))

    @app.route('/callback')
    def callback():
        sp_oauth = create_spotify_oauth()

        # Check if the 'error' parameter exists, which indicates the user canceled the authentication
        if 'error' in request.args:
            return redirect(url_for('home'))

        # Check if the 'code' parameter exists in the request arguments
        if 'code' not in request.args:
            return redirect(url_for('home'))

        token_info = sp_oauth.get_access_token(request.args['code'])
        session['token_info'] = token_info
        with open('token_info.json', 'w') as token_file:
            json.dump(token_info, token_file)
        return redirect(url_for('top_tracks'))

    @app.route('/top_tracks')
    def top_tracks():
        data, error = fetch_top_tracks()
        if error:
            session.pop('token_info', None)
            return render_template('error.html', error=error)

        tracks = data['top_tracks']['items']
        return render_template('top_tracks.html', tracks=tracks)

    @app.route('/heatmap')
    def heatmap_route():
        data, error = fetch_top_tracks()
        if error:
            session.pop('token_info', None)
            return render_template('error.html', error=error)

        heatmap_html = visualize_heatmap(data)
        covers = [track['album']['images'][0]['url'] for track in data['top_tracks']['items']]
        return render_template('heatmap.html', heatmap_div=heatmap_html, covers=covers)

    return app

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'),
        redirect_uri=os.getenv('REDIRECT_URI'),
        scope='user-top-read',
        cache_handler=spotipy.cache_handler.FlaskSessionCacheHandler(session),
        show_dialog=True
    )

def fetch_top_tracks():
    sp_oauth = create_spotify_oauth()
    token_info = session.get('token_info')
    if not token_info:
        return None, 'Token not found, please authenticate.'

    token_info = sp_oauth.validate_token(token_info)
    if not token_info:
        return None, 'Token validation failed, please authenticate again.'

    try:
        sp = spotipy.Spotify(auth=token_info['access_token'])
        top_tracks = sp.current_user_top_tracks(limit=10, time_range='short_term')
        if len(top_tracks['items']) < 10:
            return None, 'You need to listen to more songs before trying this :D'
        track_ids = [track['id'] for track in top_tracks['items']]
        audio_features = sp.audio_features(track_ids)

        response = {
            'top_tracks': top_tracks,
            'audio_features': audio_features
        }
        return response, None
    except (spotipy.exceptions.SpotifyException, Exception) as e:
        return None, f'An error occurred: {e}'

def visualize_heatmap(data):
    top_tracks = data['top_tracks']
    audio_features = data['audio_features']

    df = pd.DataFrame(audio_features)
    df['track_name'] = [track['name'] for track in top_tracks['items']]
    df['cover_url'] = [track['album']['images'][0]['url'] for track in top_tracks['items']]
    df = df[['track_name', 'cover_url', 'danceability', 'energy', 'valence', 'acousticness', 'instrumentalness', 'liveness', 'speechiness']]

    # Create heatmap
    heatmap_data = df.drop(columns='cover_url').set_index('track_name').T
    heatmap_fig = px.imshow(heatmap_data,
                            labels={'x': 'Track Name', 'y': 'Audio Feature', 'color': 'Value'},
                            aspect="auto",
                            color_continuous_scale='sunset')

    # Customize heatmap layout
    heatmap_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  
        paper_bgcolor='rgba(0,0,0,0)',  
        font=dict(color='white'),
        title_font=dict(size=24, color='white', family='Raleway'),
        height=625,
        margin=dict(t=125)
    )
    heatmap_fig.update_xaxes(
        showline=False,
        gridcolor='rgba(255,255,255,0.3)'
    )
    heatmap_fig.update_yaxes(
        showline=False,
        gridcolor='rgba(255,255,255,0.3)'
    )

    # Add cover images above the heatmap columns
    for i, cover in enumerate(df['cover_url']):
        heatmap_fig.add_layout_image(
            dict(
                source=cover,
                xref="x",
                yref="paper",
                x=i,
                y=1.075,  
                sizex=0.6,  
                sizey=0.6,  
                xanchor="center",
                yanchor="bottom"
            )
        )

    return heatmap_fig.to_html(full_html=False)

if __name__ == "__main__":
    main()
