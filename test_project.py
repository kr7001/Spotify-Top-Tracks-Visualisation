import pytest
from flask import session
from project import create_app, visualize_heatmap

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    return app.test_client()

def test_home(client, mocker):
    # Mock the Spotify OAuth creation
    mock_oauth = mocker.MagicMock()
    mocker.patch('project.create_spotify_oauth', return_value=mock_oauth)
    mock_oauth.validate_token.return_value = None
    mock_oauth.get_authorize_url.return_value = '/mock_auth_url'

    # Test the home route
    response = client.get('/')
    assert response.status_code == 302
    assert '/mock_auth_url' in response.location

def test_callback(client, mocker):
    # Mock the Spotify OAuth creation
    mock_oauth = mocker.MagicMock()
    mocker.patch('project.create_spotify_oauth', return_value=mock_oauth)

    # Simulate an error from Spotify authentication
    response = client.get('/callback?error=access_denied')
    assert response.status_code == 302
    assert '/' in response.location

    # Simulate missing code in the request
    response = client.get('/callback')
    assert response.status_code == 302
    assert '/' in response.location

def test_callback_with_code(client, mocker):
    # Mock the Spotify OAuth creation and token retrieval
    mock_oauth = mocker.MagicMock()
    mocker.patch('project.create_spotify_oauth', return_value=mock_oauth)
    mock_oauth.get_access_token.return_value = {'access_token': 'mock_token'}

    # Test the callback route with a code
    response = client.get('/callback?code=mock_code')
    assert response.status_code == 302
    assert '/top_tracks' in response.location

def test_top_tracks(client, mocker):
    # Mock the fetch top tracks function
    mocker.patch('project.fetch_top_tracks', return_value=({"top_tracks": {"items": []}}, None))

    # Simulate a session with a valid token
    with client.session_transaction() as sess:
        sess['token_info'] = {'access_token': 'mock_token'}

    # Test the top tracks route
    response = client.get('/top_tracks')
    assert response.status_code == 200
    assert b'TOP 10 SPOTIFY TRACKS' in response.data

def test_heatmap(client, mocker):
    # Mock the fetch top tracks and visualize heatmap functions
    mocker.patch('project.fetch_top_tracks', return_value=({"top_tracks": {"items": []}}, None))
    mocker.patch('project.visualize_heatmap', return_value='<div>Mock Heatmap</div>')

    # Simulate a session with a valid token
    with client.session_transaction() as sess:
        sess['token_info'] = {'access_token': 'mock_token'}

    # Test the heatmap route
    response = client.get('/heatmap')
    assert response.status_code == 200
    assert b'<div>Mock Heatmap</div>' in response.data

def test_visualize_heatmap():
    # Mock data input
    data = {
        'top_tracks': {'items': [{'name': 'Song 1', 'album': {'images': [{'url': 'image_url_1'}]}}, {'name': 'Song 2', 'album': {'images': [{'url': 'image_url_2'}]}}]},
        'audio_features': [
            {'danceability': 0.5, 'energy': 0.6, 'valence': 0.7, 'acousticness': 0.2, 'instrumentalness': 0.3, 'liveness': 0.4, 'speechiness': 0.1},
            {'danceability': 0.6, 'energy': 0.7, 'valence': 0.8, 'acousticness': 0.3, 'instrumentalness': 0.4, 'liveness': 0.5, 'speechiness': 0.2}
        ]
    }
    heatmap_html = visualize_heatmap(data)
    assert 'html' in heatmap_html  # Check if HTML is returned