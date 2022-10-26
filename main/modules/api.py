from bs4 import BeautifulSoup
import requests

hosts = ['api.consumet.org']

api = [
    'https://{}/anime/gogoanime/watch/',
    'https://{}/anime/gogoanime/servers/',
    'https://{}/anime/zoro/',
    'https://{}/anime/zoro/info?id=',
    'https://{}/anime/zoro/watch?episodeId=',
    'https://{}/anime/animepahe/',
    'https://{}/anime/animepahe/info/',
    'https://{}/anime/animepahe/watch/',
    'https://animepahe.com/api?m=airing'
]

class AnimePahe():
    def __init__(self) -> None:
        pass

    def search(self):
        json = None
        for host in hosts:
            url = api[5].format(host) + self
            response = requests.get(url)

            if response.status_code == 200:
                json = response.json()
                break
        if not json:
            return

        return json['results']

    def get_latest():
        url = api[8]
        response = requests.get(url).json()
        return response['data']

    def get_episode_links(self):
        json = None
        tries = 0
        while tries < 6:
            for host in hosts:
                tries += 1
                url = api[7].format(host) + self
                response = requests.get(url)

                if response.status_code == 200:
                    json = response.json()
                    break
            print(f'Try {tries} failed -->', self)
        if not json:
            return
        return json
