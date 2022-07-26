from yandex_disc import YaUploader
from vk_class import VkApi
from insta_class import InstApi
from tqdm import tqdm
from datetime import datetime
from time import sleep
import json


def upload_photo_to_ya_disc(ya_token, list_of_photos, name_of_dir="files_for_netology"):
    ya = YaUploader(ya_token)
    if not ya.check_disk():  # проверка на доступность диска
        return
    # создаем имена по сценарию из файла с данными о фото:
    if not list_of_photos:
        return
    count = len(list_of_photos)
    t = tqdm(total=len(list_of_photos))
    for photo in list_of_photos:
        ya.upload_from_href(photo['url'], photo['name'], name_of_dir)
        sleep(0.1)
        t.update()
    t.close()
    print(f'\nВсе файлы загружены (в количестве {len(list_of_photos)} при запросе {count} фотографий)')
    with open('logs.txt', 'a') as f:
        f.write(f'{datetime.now().strftime(f"%H:%M:%S:%f %d/%m/%Y")} | '
                f'Все файлы загружены (в количестве {len(list_of_photos)} при запросе {count} фотографий)\n')


def make_json_from_vk(list_of_photos):
    if not list_of_photos:
        print('Файл JSON не создан, так как некорректные данные!')
        return
    json_list = []
    for photo in list_of_photos:
        json_list.append({"file_name": photo["name"], "size": photo["sizes"]["type"]})
    with open('photos.json', 'w') as f:
        json.dump(json_list, f)


def input_social_network_and_username():
    while True:
        number = input(
            'Выберите социальную сеть, из которой необходимо скачать фотографии.\n 1. ВКонтакте \n 2. Instagram\n '
            'Введите число 1 или 2: ')
        if number not in ("1", "2"):
            print('Введите число 1 или 2!')
            continue
        return number


def make_photo_names(list_of_photos: list):
    '''создаем имена файлов по условию: имя - количество лайков, если их число совпадает - то лайк + дата создания'''
    if not list_of_photos:
        return False
    set_of_names = set()  # массив всех имен
    set_of_repeated_names = set()  # массив повторных имен
    for photo in list_of_photos:
        name = str(photo["likes"]["count"])
        if name in set_of_names:
            set_of_repeated_names.add(name)
        photo["name"] = name
        set_of_names.add(name)
        photo['url'] = photo['sizes']['url']  # выводим url на верхний уровень
    for photo in list_of_photos:
        if photo["name"] in set_of_repeated_names:  # если имя совпадает с именем в массиве с повторами,
            # то меняем все одинаковые имена
            photo["name"] = f'{photo["name"]}_{datetime.fromtimestamp(photo["date"]).strftime("%d-%m-%Y_%H-%M-%S")}'

    return list_of_photos


def download_photo(ya_token, vk_token='', insta_token=''):
    '''Function of inputting of dir name and count of photo'''
    while True:
        dir_name = input('Введите название папки на Я.диске для загрузки фото: ')
        if not dir_name:
            print('Вы не ввели название папки!')
            continue
        while True:
            try:
                count = int(input('Введите количество загружаемых фотографий целым числом больше 0 и меньше 100: '))
            except ValueError:
                print('Введено не корректное число! Повторите попытку!')
                continue
            if 100 <= count or count <= 0:
                continue
            break
        number = input_social_network_and_username()
        if number == "1":
            vk = VkApi(vk_token)
            user_id = input('Введите ник пользователя или его id: ')
            photo_list = make_photo_names(vk.get_max_size_photos(user_id, count))
            make_json_from_vk(photo_list)
        if number == "2":
            insta_api = InstApi(insta_token)
            user_id = input('Введите id пользователя (ник не подходит): ')
            dict1 = insta_api.get_user_info(user_id)
            new_list = insta_api.get_list_of_photos(dict1, count)
            photo_list = insta_api.make_dict_of_photos(new_list)
        upload_photo_to_ya_disc(ya_token, photo_list, dir_name)
        question = input("Если готовы продолжать запросы - введите 'да', если хотите выйти - любую другую фразу: ")
        if question != "да":
            break