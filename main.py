from pprint import pprint

import requests


TOKEN = "2619421814940190"


def superhero_request(superheros):
    """
    Функция принимает список супергероев и определяет кто из них самый умный.
    Т.е. у кого параметр "intelligence" максимальный.
    Для решения Задачи №1
    :param superheros: Список супергероев
    :return: Самый умный супергерой
    """
    superhero_intelligence = 0
    superhero_name = ''
    for superhero in superheros:
        url = f'https://www.superheroapi.com/api/{TOKEN}/search/{superhero}'
        response = requests.get(url=url, timeout=5)
        if response.status_code == 200:
            id_superhero = response.json()['results'][0]['id']
            url = f'https://www.superheroapi.com/api/{TOKEN}/{id_superhero}/powerstats/'
            response = requests.get(url=url, timeout=5)
            if superhero_intelligence < int(response.json()['intelligence']):
                superhero_intelligence = int(response.json()['intelligence'])
                superhero_name = superhero
        else:
            print('error')

    return f'Самый умный супергерой: {superhero_name}. \nЕго интеллект: {superhero_intelligence}'


if __name__ == '__main__':
    print('Задача №1')
    print(superhero_request({'Hulk', "Captain America", 'Thanos'}))
