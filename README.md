# Spotify Top Tracks Visualization
#### Author: Kai Rong Lee
#### Video Demo:  https://youtu.be/MTFReW54fO0

## Introduction

My Spotify Top Tracks Visualization project is a web application built using Flask that interacts with the Spotify API. The application allows users to authenticate via Spotify and fetch their top 10 tracks. After authenticating, the first web page will display the user's top 10 tracks, and the second web page displays the audio features of these tracks in a heatmap format, generated using Plotly. HTML and CSS are used to enhance the aesthetics of the web pages.

## Files and Functions

### `project.py`

This is the main application file which contains the core logic for the Flask web application. It includes the following key functionalities:

- **Route Handlers**: Handles various routes such as the home page, callback from Spotify, and displaying top tracks and heatmaps.
- **Spotify OAuth**: Manages the OAuth2 flow for authenticating with Spotify and obtaining access tokens.
- **Fetch Top Tracks**: A function to fetch the top tracks of the user using the Spotify API.
- **Visualize Heatmap**: A function to generate HTML for visualizing audio features in a heatmap.

### `test_project.py`

This file contains test cases for the application using the `pytest` framework. It includes tests for:

- Home route to ensure proper redirection to Spotify's authorization URL.
- Callback route to handle the response from Spotify after authentication.
- Fetching top tracks and verifying the retrieved data.
- Visualizing the heatmap and ensuring the HTML is correctly generated.

### `.env`

This file contains environment variables needed for the application to interact with the Spotify API. It includes:

- `CLIENT_ID`: Spotify client ID.
- `CLIENT_SECRET`: Spotify client secret.
- `REDIRECT_URI`: URI where Spotify will redirect after authentication.

### `requirements.txt`

This file lists all the Python dependencies required for the project. These dependencies can be installed using pip:

```bash
pip install -r requirements.txt
