import os
from dotenv import load_dotenv
import requests
import json
import sys

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")


def get_oauth_token():
    auth_url = "https://accounts.spotify.com/api/token"
    auth_response = requests.post(
        auth_url,
        {
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    )
    auth_response_data = auth_response.json()
    return auth_response_data["access_token"]


def search_spotify(query, token):
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://api.spotify.com/v1/search"
    params = {"q": query, "type": "track", "limit": 1}
    response = requests.get(url, headers=headers, params=params)
    return response.json()


def get_recommendations(seeds, token, limit=10):
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://api.spotify.com/v1/recommendations"

    seed_tracks = [seed["tracks"]["items"][0]["id"] for seed in seeds]

    params = {
        "seed_tracks": ",".join(seed_tracks),
        "limit": limit,
        "market": "US",  # Pin to US, hopefully doesn't cause issue when travelling
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()


def main(songs):
    token = get_oauth_token()
    seeds = []
    for song in songs:
        query = f"{song['name']} {song['artist']}"
        search_result = search_spotify(query, token)
        if search_result["tracks"]["items"]:
            seed = search_result
            seeds.append(seed)

            # Spotify API allows up to 5 seed tracks
            if len(seeds) >= 5:
                break

    recommendations = get_recommendations(seeds, token)
    print(recommendations)
    recommended_tracks = [
        {"name": track["name"], "artist": track["artists"][0]["name"]}
        for track in recommendations["tracks"]
    ]
    print(json.dumps(recommended_tracks, indent=2))


if __name__ == "__main__":
    # accept a json file that has "name", "artist" pairs
    # e.g. [{"name": "Ai Wo Tsutaetaidatoka", "artist": "Aimyon"}, ...]
    songs = json.loads(sys.argv[1])

    main(songs)
