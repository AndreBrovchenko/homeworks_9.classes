from pprint import pprint

import requests
import datetime


class YaUploader:
    """
    Класс для работы с Яндекс.Диск
    Для решения Задачи №2
    """
    def __init__(self, token_ya: str):
        """
        :param token_ya: значение ТОКЕНА для доступа к Яндекс.Диск-у
        """
        self.token = token_ya

    def get_headers(self):
        """
        Метод для формирования атрибута "headers" запроса
        :return:
        """
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def get_files_list(self):
        """
        Метод для получения списка файлов
        :return:
        """
        url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(url=url, headers=headers)
        return response.json()

    def _get_upload_link(self, disk_file_path):
        """
        Метод для получения ссылки для загрузки файла на Яндекс.Диск
        :param disk_file_path: Путь к файлу на Яндекс.Диске
        :return:
        """
        # disk_file_path - это путь к файлу на Яндекс.Диск-е
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload(self, file_path: str, file_to_disk):
        """
        Метод загружает файл на Яндекс.Диск
        :param file_path: Путь к файлу на локальном дичке для загрузки на Яндекс.Диск
        :param file_to_disk:  Путь к файлу на Яндекс.Диске
        :return:
        """
        response = self._get_upload_link(file_to_disk)
        download_link = response.get('href', '')
        response = requests.put(url=download_link, data=open(file_path, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")


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


def get_list_questions(tag, page):
    """
    Список вопросов за последние два дня с определенным тегом
    Для решения Задачи №3
    :param tag: тег для фильтра вопросов
    :param page: номер запрашиваемой страницы, т.к. данные возвращаются постранично
    :return: Очередная страница с данными
    """
    url = 'https://api.stackexchange.com/2.3/questions'
    current_date = datetime.datetime.today()
    todate = str(int(current_date.timestamp()))
    past_date = datetime.datetime.today() - datetime.timedelta(days=2)
    fromdate = str(int(past_date.timestamp()))
    params = {
        "page": page,
        "pagesize": "100",
        "fromdate": fromdate,
        "todate": todate,
        "order": "desc",
        "sort": "activity",
        "tagged": tag,
        "site": "stackoverflow"
    }
    response = requests.get(url=url, params=params, timeout=5)
    return response.json()


if __name__ == '__main__':
    print('Задача №1')
    print(superhero_request({'Hulk', "Captain America", 'Thanos'}))
    print('Задача №2')
    # Получить путь к загружаемому файлу и токен от пользователя
    path_to_file = input('Введите путь к файлу: ')
    path_to_disk = input('Введите путь для записи на Я.Диск: ')
    token = input('Введите ТОКЕН: ')
    uploader = YaUploader(token)
    uploader.upload(path_to_file, path_to_disk)
    print('Задача №3')
    number_page = 1
    row = 0
    questions = get_list_questions('python', number_page)
    # цикл с таким условием не подходит, потому что вопросы с последней страницы не выводятся
    # while questions['has_more']:
    # пока список вопросов ['items'] на странице не пуст
    while questions['items']:
        print(f'Page: {number_page}')
        for el in questions['items']:
            row += 1
            # print(el['title'])
            print(f"{row}. {el['title']}")
        number_page += 1
        questions = get_list_questions('python', number_page)
