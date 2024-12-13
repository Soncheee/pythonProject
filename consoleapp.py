import requests

# Ваш API-ключ для Google Books API (зарегистрируйтесь на https://console.cloud.google.com/, чтобы получить ключ)
API_KEY = "AIzaSyDn9yBPBZ-4nKtiAVE8knpwT5mYV5VAjLI"
BASE_URL = "https://www.googleapis.com/books/v1/volumes"

favourites = []
readed = []

def search_books_by_author(authorname, many_not=0):
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
                    answers_to_add = (input("Хотите ли вы добавить эту книгу в список избранных или уже прочитанного?(да/нет) "))
                    if answers_to_add == "нет":
                        many_not += 1
                        if many_not <= 3:
                            continue
                        else:
                            more = input(("Хотите больше книг этого автора?да/нет "))
                            if more == "да":
                                continue
                            elif more == "нет":
                                print("OK")
                                break
                        continue
                    elif answers_to_add == "да":
                        add_to = input("куда вы хотите добавить: избранное или прочитанное? ")
                        if add_to == "избранное":
                            favourites.append(title)
                            print("Книга добавлена в избранное")
                        elif add_to == "прочитанное":
                            readed.append(title)
                            print("Книга добавлена в прочитанное")
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
                    answers_to_add = (input("Хотите ли вы добавить эту книгу в список избранных или уже прочитанного?(да/нет)"))
                    if answers_to_add == "нет":
                        many_not += 1
                        if many_not <= 3:
                            continue
                        else:
                            more = input(("Хотите больше книг с этим названием?да/нет"))
                            if more == "да":
                                continue
                            elif more == "нет":
                                print("OK")
                                break
                        continue
                    elif answers_to_add == "да":
                        add_to = input("куда вы хотите добавить: избранное или прочитанное?")
                        if add_to == "избранное":
                            favourites.append(title)
                            print("Книга добавлена в избранное")
                        elif add_to == "прочитанное":
                            readed.append(title)
                            print("Книга добавлена в прочитанное")
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

