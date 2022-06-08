from downloader import Download

# Возможна такая ситуация, что мы хотим показать друзьям фотографии из социальных сетей, но соц. сети могут быть недоступны по каким-либо причинам. Давайте защитимся от такого.
# Нужно написать программу для резервного копирования фотографий с профиля(аватарок) пользователя vk в облачное хранилище Яндекс.Диск.
# Для названий фотографий использовать количество лайков, если количество лайков одинаково, то добавить дату загрузки.
# Информацию по сохраненным фотографиям сохранить в json-файл.
#
# Задание:
# Нужно написать программу, которая будет:
#
# Получать фотографии с профиля. Для этого нужно использовать метод photos.get.
# Сохранять фотографии максимального размера(ширина/высота в пикселях) на Я.Диске.
# Для имени фотографий использовать количество лайков.
# Сохранять информацию по фотографиям в json-файл с результатами.
# Входные данные:
# Пользователь вводит:
#
# id пользователя vk;
# токен с Полигона Яндекс.Диска. Важно: Токен публиковать в github не нужно!
# Выходные данные:
# json-файл с информацией по файлу:
#     [{
#     "file_name": "34.jpg",
#     "size": "z"
#     }]
# Измененный Я.диск, куда добавились фотографии.​​.



if __name__ == '__main__':
    # token_vk = input('Введите токен ВК: ')
    # token_ya = input('Введите токен Я.диска: ')
    id_vk = input('Введите id Вконтакте: ')
    dir_name = input('Введите название папки на Я.диске для загрузки фото')
    count = int(input('Введите количество загружаемых фотографий'))
    dl = Download()
    dl.upload_photo_from_vk_to_ya_disc(user_id=id_vk, count=count, name_of_dir=dir_name )