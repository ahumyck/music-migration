import json
import logging
from typing import List

from yandex_music.client import Client
from yandex_music.exceptions import YandexMusicError

credentials_filename = 'credentials.json'
token_filename = 'token.json'


def read_json(filename):
    with open(filename) as f:
        return json.load(f)


def save_json(filename, dictionary):
    with open(filename, 'w') as f:
        json.dump(dictionary, f)


def get_login_and_password(filename):
    credentials = read_json(filename)
    return credentials['address'], credentials['password']


def get_track_name(full_track):
    return full_track.artists[0].name + " " + full_track.title


def generate_token(credentials_file):
    login, password = get_login_and_password(credentials_file)
    return Client().generate_token_by_username_and_password(username=login, password=password)


def get_client(token_file, credentials_file):
    token = read_json(token_file)['token']
    cl = Client.from_token(token)
    if cl.me.account.login is None:
        token = generate_token(credentials_file)  # TODO: ask user for input
        save_json(token_file, wrap_token(token))
        cl = Client.from_token(token)
    return cl


def wrap_token(token):
    return {'token': token}


def create_playlist(client, title="Music Migration"):
    for playlist in client.users_playlists_list():
        print(playlist.title)
        if playlist.title == title:
            raise YandexMusicError("such album already exists")
    return client.usersPlaylistsCreate(title=title)


def add_song_to_playlist(client: Client, playlist_kind: str or int, full_track_ids: str or List[str]):
    if isinstance(full_track_ids, list):
        for i, full_track_id in enumerate(full_track_ids):
            track_id, album_id = full_track_id.split(':')
            print(i)
            playlist = client.users_playlists_insert_track(playlist_kind, track_id, album_id, revision=i + 1)
            if playlist is None:
                print(f"Cant add {full_track_id} to playlist")
    else:
        track_id, album_id = full_track_ids.split(':')
        client.users_playlists_insert_track(playlist_kind, track_id, album_id)


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    client = get_client(token_filename, credentials_filename)

    track_list = client.users_likes_tracks()
    # print(track_list)
    track_ids = [t.track_id for t in track_list.tracks]
    # print(track_ids)
    full_tracks = client.tracks(track_ids)
    # tracks_map = dict(zip(track_ids, full_tracks))
    print(track_ids[0])
    # print(track_id, tracks_map[track_id])
    # print(full_tracks[0], type(full_tracks[0]))
    track_names = [get_track_name(full_track) for full_track in full_tracks]
    print(track_names[0])

    # print(client.albums)

    r = create_playlist(client)
    add_song_to_playlist(client, r.kind, track_ids)

    print(r)
