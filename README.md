# Spotify Reccomender Apple Shortcut

I like Apple Music for its features and sound quality but I miss the Spotify reccomendation algorithm lol. Little script that uses Spotify API to integrate into Apple Shortcuts via the SSH script action to get the best of both worlds ^_^.

## Usage

You need to store secrets in `.env`.

```py
CLIENT_ID=xxxxxx
CLIENT_SECRET=xxxxxx
REDIRECT_URI=url
```

## Apple Shortcut Action

These are the steps to create the Apple Shortcut action:

## Acknowledgements

This mainly uses the [reccomendation call](https://developer.spotify.com/documentation/web-api/reference/get-recommendations). I'll have to see if there are any other calls that can enhance the query, closely matching to how Spotify reccomends songs in-app.