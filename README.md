# Sync Streaming Music

Sync your music across multiple streaming music services. Currently, only [Youtube Music](https://music.youtube.com/) and [Spotify](https://open.spotify.com/) are available.

This project is based on [ytmusicapi](https://github.com/sigma67/ytmusicapi) and [spotipy](https://github.com/spotipy-dev/spotipy).

It is a work in progress. It is not ready for production use. At the moment, it is only possible to sync playlists from csv files (one for each playlist) to Youtube Music. If you want to try the application, you can use the template playlists in the `resources\playlists` folder or download your favorite one from [Exportify](https://watsonbox.github.io/exportify/).

## Setup

### Requirements

- [Python](https://www.python.org/) 3.6 or higher
- dependencies listed in `requirements.txt`. Install them with `pip install -r requirements.txt`

### Configuration

1. Follow [these steps](https://ytmusicapi.readthedocs.io/en/stable/setup.html#copy-authentication-headers) to obtain your YouTube Music authentication header.

2. Create a `.env` file in the root directory of the project and assign your YouTube Music authentication header to the `HEADER_RAW` variable. Consider making use of `.env.example` as a guide.

## Usage

### Quick Start

Once you have configured the application and added your playlists (in csv format) to the `resources/playlist folder`, you can run it with the following command:

```bash
python ./src/main.py
```

All of your favorite playlists are now available in your YouTube Music account!

## Contributing

If you wish to contribute or you have just found any bug, please open an issue or a pull request on our GitHub repository. Thank you!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.
