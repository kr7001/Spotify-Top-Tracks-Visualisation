# Spotify Top Tracks Visualization

**Author:** Kai Rong Lee

**Video Demo:** [YouTube](https://youtu.be/MTFReW54fO0)

## Introduction

My Spotify Top Tracks Visualization project is a web application built using Flask that interacts with the Spotify API to provide an interactive experience for users to explore their top 10 tracks. The application enables users to authenticate via Spotify, fetch their top 10 tracks, and visualize various audio features of these tracks in a heatmap format. This project aims to merge functionality with aesthetic appeal, utilising HTML, CSS, and Plotly for enhanced visualizations. The color palette I chosen for this web application are inspired by the film 'La la land'.

## Files and Functions

### project.py

This is the core file of the application and contains all the primary logic needed to run the Flask web application. The key functionalities within this file include:

- **Route Handlers:** These handle the routing for various parts of the application, such as the home page, Spotify callback, and the pages displaying the user's top tracks and the heatmap visualization.
  - **Home Route:** Directs users to the Spotify authentication page to initiate the OAuth2 flow.
  - **Callback Route:** Manages the response from Spotify post-authentication, retrieves the access token, and handles any necessary data processing.
  - **Top Tracks Route:** Fetches and displays the user's top 10 tracks.
  - **Heatmap Route:** Displays the audio features of the top tracks in a heatmap format.

- **Spotify OAuth:** Manages the OAuth2 flow necessary for authenticating with Spotify and obtaining access tokens. This includes:
  - **Requesting Authorization:** Directs the user to Spotify’s authorization page.
  - **Handling the Callback:** Processes the response from Spotify to obtain the access token.

- **Fetch Top Tracks:** This function uses the Spotify API to fetch the user's top tracks. It makes authenticated API calls to retrieve data about the user's most listened-to tracks, ensuring that the data is current and accurate.
  - **Data Retrieval:** The function processes JSON responses from the API to extract relevant information such as track names, artists, and album details.
  - **Error Handling:** Ensures that any issues with data retrieval are handled using try-except, providing appropriate feedback to the user.

- **Visualize Heatmap:** This function generates HTML for visualizing the audio features of the tracks in a heatmap. Using Plotly, it creates an interactive and visually engaging heatmap that allows users to explore different audio features such as danceability, energy, and valence.
  - **Plotly Integration:** Utilizes Plotly’s graphing libraries to create dynamic heatmaps.
  - **HTML Generation:** Embeds the heatmap within HTML for display on the web page.

### test_project.py

This file contains test cases written using the pytest framework to ensure the application functions as expected. Key tests include:

- **Home Route Test:** Verifies that the home route correctly redirects users to Spotify’s authorization URL.
- **Callback Route Test:** Ensures that the callback route correctly handles Spotify’s response and processes the access token.
- **Fetch Top Tracks Test:** Tests the function that fetches top tracks to ensure it retrieves accurate data from the Spotify API.
- **Visualize Heatmap Test:** Ensures that the heatmap visualization function generates the correct HTML and properly integrates Plotly’s features.

### .env

This file stores environment variables necessary for interacting with the Spotify API:

- **CLIENT_ID:** Spotify client ID
- **CLIENT_SECRET:** Spotify client secret
- **REDIRECT_URI:** The URI where Spotify will redirect after the user authenticates

### requirements.txt

This file lists all the Python dependencies required for the project. The primary dependencies include:

- **Flask:** A lightweight WSGI web application framework used for developing the web application.
- **Requests:** A simple HTTP library for making API requests to Spotify.
- **Plotly:** A graphing library used to create interactive heatmaps for visualizing audio features.
- **pytest:** A testing framework for writing and running tests.

## Implementation Details

### OAuth2 Authentication

The application uses Spotify’s OAuth2 mechanism to authenticate users. This involves redirecting users to Spotify’s login page, obtaining their consent to access their data, and then using the returned authorization code to request an access token. This token is used for subsequent API requests to fetch the user’s top tracks.

### Fetching Data

After obtaining the access token, the application makes a request to the Spotify API’s `/me/top/tracks` endpoint to retrieve the user's top 10 tracks. The response includes detailed information about each track, such as its name, artist, album, and various audio features like danceability, energy, and valence.

### Data Visualization

Once the top tracks are fetched, the application uses Plotly to create a heatmap of the audio features. This heatmap is then embedded into the web page using HTML and CSS. The heatmap allows users to visually compare the audio features of their favorite tracks, providing insights into their listening preferences.

### User Interface

The application’s user interface is designed with simplicity and aesthetics in mind. HTML and CSS are used to create a clean and intuitive layout, making it easy for users to navigate between pages and understand the visualizations.

### Testing

Comprehensive testing ensures the reliability and accuracy of the application. The tests verify that each route behaves as expected, the data fetched from Spotify is correct, and the visualizations are properly generated.

