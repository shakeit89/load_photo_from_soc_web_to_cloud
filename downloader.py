from yandex_disc import YaUploader
from vk_class import VkApi
from insta_class import InstApi
from tqdm import tqdm
from datetime import datetime
from time import sleep
import json


def upload_photo_to_ya_disc(ya_token, list_of_photos, name_of_dir="files_for_netology"):

    ya = YaUploader(ya_token)
    if not ya.check_disk(): #проверка на доступность диска
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

def make_json(list_of_photos):
    json_list = []
    for photo in list_of_photos:
        json_list.append({"file_name": photo["name"], "size": photo["sizes"]["type"]})
    with open('photos.json', 'w') as f:
        json.dump(json_list, f)


def input_social_network_and_username():
    while True:
        number = input('Выберите социальную сеть, из которой необходимо скачать фотографии.\n 1. ВКонтакте \n 2. Instagram\n Введите число 1 или 2: ')
        if number not in ("1", "2"):
            print('Введите число 1 или 2!')
            continue
        return number



def input_dir_name_and_count(ya_token, vk_token='', insta_token=''):
    '''Function of inputting of dir name and count of photo'''
    while True:
        dir_name = input('Введите название папки на Я.диске для загрузки фото: ')
        if not dir_name:
            print('Вы не ввели название папки!')
            continue
        while True:
            try:
                count = int(input('Введите количество загружаемых фотографий целым числом больше 0 и меньше 100: '))
            except ValueError('Введено не корректное число! Повторите попытку!'):
                continue
            if 100 <= count or count <= 0:
                continue
            break
        number = input_social_network_and_username()
        if number == "1":
            vk = VkApi(vk_token)
            user_id = input('Введите ник пользователя или его id: ')
            photo_list = vk.make_photo_names(vk.get_max_size_photos(user_id,count))
            make_json(photo_list)
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
