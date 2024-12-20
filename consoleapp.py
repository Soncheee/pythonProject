from multiprocessing.sharedctypes import Value
import requests
import json

# Ваш API-ключ для Google Books API (зарегистрируйтесь на https://console.cloud.google.com/, чтобы получить ключ)
API_KEY = "AIzaSyDn9yBPBZ-4nKtiAVE8knpwT5mYV5VAjLI"
BASE_URL = "https://www.googleapis.com/books/v1/volumes"

# Имена файлов для хранения списков
FAVOURITES_FILE = 'favourites.json'
READED_FILE = 'readed.json'
RATING_FILE = 'rating.json'

def load_list(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def add_to_list(filename, value):
    """
    Добавляет элемент в файл и сразу обновляет локальный список.
    """
    # Загружаем текущий список из файла
    lst = load_list(filename)
    # Проверяем, есть ли уже элемент
    if value not in lst:
        lst.append(value)  # Добавляем новый элемент
        save_list(filename, lst)  # Сохраняем изменения в файл

        # Обновляем локальный список
        if filename == FAVOURITES_FILE:
            favourites.append(value)
        elif filename == READED_FILE:
            readed.append(value)
        elif filename == RATING_FILE:
            rating.append(value)
        else:
            print(f"Ошибка: неизвестный файл {filename}")

def save_list(filename, lst):
    with open(filename, 'w') as file:
        json.dump(lst, file)

favourites = load_list(FAVOURITES_FILE)
readed = load_list(READED_FILE)
rating = load_list(RATING_FILE)


def search_books_by_author(author_name, many_not=0):
    # Формируем запрос к Google Books API
    params = {
        'q': f'inauthor:{author_name}',  # Поиск книг по автору
        'key': API_KEY,
        'maxResults': 10,  # Максимум 10 книг
    }

    try:
        # Выполняем GET-запрос
        response = requests.get(BASE_URL, params=params)

        # Проверяем статус ответа
        if response.status_code == 200:
            data = response.json()
            # Проверяем, есть ли результаты
            if 'items' in data:
                print(f"Книги автора '{author_name}':")
                for item in data['items']:
                    title = item['volumeInfo'].get('title', 'Без названия')
                    authors = item['volumeInfo'].get('authors', ['Неизвестный автор'])
                    published_date = item['volumeInfo'].get('publishedDate', 'Неизвестно')
                    print(
                        f"- Название: {title}\n  Автор(ы): {', '.join(authors)}\n  Дата публикации: {published_date}\n")
                    answers_to_add = input("Хотите ли вы добавить эту книгу в список избранных или уже прочитанного?(да/нет) ")
                    if answers_to_add == "нет":
                        many_not += 1
                        if many_not <= 3:
                            continue
                        else:
                            more = input("Хотите больше книг этого автора?да/нет ")
                            if more == "да":
                                continue
                            elif more == "нет":
                                print("OK")
                                break
                        continue
                    elif answers_to_add == "да":
                        add_to = input("куда вы хотите добавить: избранное или прочитанное? ")
                        if add_to == "избранное":
                            add_to_list(FAVOURITES_FILE, title)
                            print("Книга добавлена в избранное")
                        elif add_to == "прочитанное":
                            add_to_list(READED_FILE, title)
                            print("Книга добавлена в прочитанное")
                            y_o_n = input("Уже читали эту книгу? Хотите оценить её?.да/нет ")
                            if y_o_n == "да":
                                rate = input("Напишите оценку от 1 до 10 ")
                                try:
                                    if 1 <= int(rate) <= 10:
                                        rated_book = f"{title}: {rate}"
                                        add_to_list(RATING_FILE, rated_book)  # Добавление оценки в список rating
                                    else:
                                        print("Ты можешь ввести только оценку от 1 до 10")
                                except ValueError:
                                    print("Ты можешь ввести только целое число от 1 до 10")
                        else:
                            print("Не пиши ерунду")
                    else:
                        print("Не пиши ерунду")
            else:
                print(f"Книги автора '{author_name}' не найдены.")
        else:
            print(f"Ошибка: код ответа {response.status_code}")
            print(f"Сообщение: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка подключения: {e}")

def search_books_by_title(book_title, many_not=0):
    # Формируем запрос к Google Books API
    params = {
        'q': f'intitle:{book_title}',  # Поиск книг по названию
        'key': API_KEY,
        'maxResults': 10,  # Максимум 10 книг
    }

    try:
        # Выполняем GET-запрос
        response = requests.get(BASE_URL, params=params)

        # Проверяем статус ответа
        if response.status_code == 200:
            data = response.json()
            # Проверяем, есть ли результаты
            if 'items' in data:
                print(f"Книги с названием '{book_title}':")
                for item in data['items']:
                    title = item['volumeInfo'].get('title', 'Без названия')
                    authors = item['volumeInfo'].get('authors', ['Неизвестный автор'])
                    published_date = item['volumeInfo'].get('publishedDate', 'Неизвестно')
                    print(
                        f"- Название: {title}\n  Автор(ы): {', '.join(authors)}\n  Дата публикации: {published_date}\n")
                    answers_to_add = input("Хотите ли вы добавить эту книгу в список избранных или уже прочитанного?(да/нет) ")
                    if answers_to_add == "нет":
                        many_not += 1
                        if many_not <= 3:
                            continue
                        else:
                            more = input("Хотите больше книг с этим названием?да/нет ")
                            if more == "да":
                                continue
                            elif more == "нет":
                                print("OK")
                                break
                        continue
                    elif answers_to_add == "да":
                        add_to = input("куда вы хотите добавить: избранное или прочитанное? ")
                        if add_to == "избранное":
                            add_to_list(FAVOURITES_FILE, title)
                            print("Книга добавлена в избранное")
                        elif add_to == "прочитанное":
                            add_to_list(READED_FILE, title)
                            print("Книга добавлена в прочитанное")
                            y_o_n = input("Уже читали эту книгу? Хотите оценить её?.да/нет ")
                            if y_o_n == "да":
                                rate = input("Напишите оценку от 1 до 10 ")
                                try:
                                    if 1 <= int(rate) <= 10:
                                        rated_book = f"{title}: {rate}"
                                        add_to_list(RATING_FILE, rated_book)  # Добавление оценки в список rating
                                    else:
                                        print("Ты можешь ввести только оценку от 1 до 10")
                                except ValueError:
                                    print("Ты можешь ввести только целое число от 1 до 10")
                        else:
                            print("Не пиши ерунду")
                    else:
                        print("Не пиши ерунду")
            else:
                print(f"Книги с названием '{book_title}' не найдены.")
        else:
            print(f"Ошибка: код ответа {response.status_code}")
            print(f"Сообщение: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка подключения: {e}")

def fav(favourites, readed):
    fav_or_readed = input("Хотите посмотреть избранное и прочитанное?.Напишите да или нет ")
    if fav_or_readed == "нет":
        print("ok")
    elif fav_or_readed == "да":
        print(f"Избранное: {', '.join(favourites)}")
        print(f"Прочитанное: {', '.join(readed)}")
    else:
        print("Да ты уже достал")

def books_rating(rating):
    us = input("Хотите посмотреть оцененные вами книги?да/нет ")
    if us == "да":
        print(f"Оценённые: {', '.join(rating)}")
    elif us == "нет":
        print("ok")
    else:
        print("Пиши по-человечески")

search_type = input("Хотите искать по автору или по названию книги? (автор/название): ")
if search_type.lower() == "автор":
    author_name = input("Введите имя автора для поиска книг: ")
    author_name.title()
    search_books_by_author(author_name)
elif search_type.lower() == "название":
    book_title = input("Введите название книги для поиска: ")
    book_title.title()
    search_books_by_title(book_title)
else:
    print("Пиши название или автора")



fav(favourites, readed)
books_rating(rating)