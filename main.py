import json
import logging

from yandex_music.client import Client

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
    return full_track.artists[0].name, full_track.title


def get_client(token_file, credentials_file):
    token = read_json(token_file)['token']
    client = Client.from_token(token)

    return client


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    login, password = get_login_and_password(credentials_filename)
    print(login, password)
    token = Client().generate_token_by_username_and_password(username=login, password=password)
    client = Client.from_token(token)
    cl2 = Client.from_token("")
    print(client)
    print(cl2)

    track_list = client.users_likes_tracks()
    print(track_list)
    track_ids = [t.track_id for t in track_list.tracks]
    print(track_ids)
    full_tracks = client.tracks(track_ids)
    track_names = [get_track_name(full_track) for full_track in full_tracks]
    print(track_names)
