import click
import eyed3
import os
import shutil

@click.command()
@click.option('-s', '--src-dir', default='.', help='Исходный каталог', show_default=True)
@click.option('-d', '--dst-dir', default='.', help='Целевой каталог', show_default=True)
def music_sort(src_dir, dst_dir):
    """Программа для сортировки музыкальных файлов"""
    while True:
        if os.path.isdir(src_dir):
            # Проверка доступа к каталогу
            try:
                # Получить итератор
                it = os.scandir(src_dir)
            except PermissionError as e:
                print(str(e))
                print('Пожалуйста введит путь к другому каталогу. Введите q для выхода')
                src_dir = input('>>> ')
                if src_dir == 'q':
                    break
            else:
                with it:
                    # Сканировать все файлы в исходном каталоге
                    for entry in it:
                        if not entry.name.startswith('.') and entry.is_file() \
                                and entry.name.lower().endswith('.mp3'):

                            # Сортировка тегов
                            try:
                                audiofile = eyed3.load(entry)
                                # Title
                                if not audiofile.tag.title:
                                    title = entry.name
                                else:
                                    title = audiofile.tag.title.replace('/', ':')
                                # Исполнитель и альбом
                                if not audiofile.tag.artist or not audiofile.tag.album:
                                    print(f'Недостаточно тегов для сортировки файлов: {entry.name}')
                                    continue
                                else:
                                    # ac/dc -_-
                                    artist = audiofile.tag.artist.replace('/', ':')
                                    album = audiofile.tag.album.replace('/', ':')

                                audiofile.tag.save()
                            except AttributeError as e:
                                print(f'Что-то не так с файлом: {entry.name}')
                            except PermissionError as e:
                                print(f'Нет прав изменить файл: {entry.name}')
                                continue
                            # Если файл в порядке, то переместить файл
                            else:
                                new_file_name = f'{title} - {artist} - {album}.mp3'
                                # Если путь существует, переместить файл
                                if os.path.exists(os.path.join(dst_dir, artist, album)):
                                    shutil.move(os.path.join(src_dir, entry.name),
                                                os.path.join(dst_dir, artist, album, new_file_name))

                                else:
                                    # Создать папки для отсортированных файлов
                                    try:
                                        os.makedirs(os.path.join(dst_dir, artist, album))
                                    except PermissionError as e:
                                        print(str(e))
                                        print('Введите путь к другому каталогу. Введите q для выхода.')
                                        dst_dir = input('>>> ')
                                        if dst_dir == 'q':
                                            break
                                    # Переместить файл
                                    else:
                                        shutil.move(os.path.join(src_dir, entry.name),
                                                    os.path.join(dst_dir, artist, album, new_file_name))
                                print(f'{os.path.join(src_dir, entry.name)} '
                                      f'-> {os.path.join(dst_dir, artist, album, new_file_name)}')
                # Закончить программу
                print('Готово')
                break
        # Исходный каталог не найден
        else:
            print('Исходный каталог не найден')
            print('Введит путь к существующему каталог. Введите q для выхода')
            src_dir = input('>>> ')
            if src_dir == 'q':
                break


if __name__ == '__main__':
    music_sort()
