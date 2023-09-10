import os

import requests
from bs4 import BeautifulSoup


URL = "https://hollowknight.fandom.com/ru/wiki/Голоса_персонажей/Неигровые_персонажи"
AUDIO_URL = "https://static.wikia.nocookie.net/hollowknight/images/0/02/Старейшина_голос1.ogg/revision/latest?cb" \
            "=20170721201606&path-prefix=ru"


def create_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_response(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Status code = {response.status_code} for url {url}")
    return response


def download_audio_file(audio_url=AUDIO_URL, filename='test.odd'):
    if os.path.exists(filename):
        return True
    response = get_response(audio_url)
    with open(filename, "wb") as file:
        file.write(response.content)
    return True


def main(url=URL):
    response = get_response(url)

    project_dir = os.getcwd()
    base_dir = os.path.join(project_dir, 'Hollow Knight')
    create_if_not_exists(base_dir)

    soup = BeautifulSoup(response.content, "html.parser")
    persons = soup.find_all("div", class_="hk-voice")

    for person in persons:
        person_name = list(filter(lambda x: x, person.text.split('\n')))[0]
        while person_name[-1] == ' ':
            person_name = person_name[:-1]
        print(person_name)

        person_dir = os.path.join(base_dir, person_name)
        create_if_not_exists(person_dir)

        audio_files = person.find_all("span", class_="audio-button")
        for i, audio_file in enumerate(audio_files):
            audio_filename = os.path.join(person_dir, f"{person_name}_{i}.odd")
            audio_file_ref = list(audio_file.children)[0].attrs['src']
            download_audio_file(audio_file_ref, audio_filename)

    return True


if __name__ == '__main__':
    result = main()
    if result:
        print("-" * 10)
        print("The script was executed successfully")
