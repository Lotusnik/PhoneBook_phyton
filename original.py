FILENAME = 'phone.txt'  # Имя файла, в котором хранятся данные телефонного справочника

def load_data(filename):  # Функция для загрузки данных из файла
    with open(filename, 'r', encoding='utf-8') as file:  # Открываем файл для чтения
        lines = file.readlines()  # Читаем все строки из файла
    contacts = []  # Создаем пустой список для хранения контактов
    for line in lines:  # Перебираем все строки в файле
        if line.strip():  # Пропускаем пустые строки
            parts = line.split(',')  # Разделяем строку на части по запятым
            if len(parts) == 4:  # Проверяем, что строка состоит из 4 частей
                contacts.append({  # Добавляем контакт в список
                    'last_name': parts[0].strip().capitalize(),  # Фамилия с большой буквы
                    'first_name': parts[1].strip().capitalize(),  # Имя с большой буквы
                    'phone': parts[2].strip(),  # Номер телефона
                    'description': parts[3].strip().capitalize()  # Описание с большой буквы
                })
    return contacts  # Возвращаем список контактов

def save_data(filename, contacts):  # Функция для сохранения данных в файл
    with open(filename, 'w', encoding='utf-8') as file:  # Открываем файл для записи
        for contact in contacts:  # Перебираем все контакты
            line = f"{contact['last_name']}, {contact['first_name']}, {contact['phone']}, {contact['description']}\n"  # Форматируем строку для записи
            file.write(line)  # Записываем строку в файл

def display_contacts(contacts, highlight=None):  # Функция для отображения контактов
    if contacts:  # Проверяем, что список контактов не пуст
        for contact in contacts:  # Перебираем все контакты
            output = f"{contact['last_name']} {contact['first_name']} - {contact['phone']} - {contact['description']}"  # Форматируем строку для отображения
            if highlight and any(highlight.lower() in value.lower() for value in contact.values()):  # Проверяем, нужно ли выделить строку
                output = f"\033[1;32m{output}\033[0m"  # Выделяем строку зеленым цветом
            print(output)  # Печатаем строку
    else:
        print("Контакты не найдены.")  # Сообщаем, что контакты не найдены

def search_contacts(contacts, term):  # Функция для поиска контактов по терму
    results = [contact for contact in contacts if term.lower() in [value.lower() for value in contact.values()]]  # Ищем контакты, содержащие терм
    return results  # Возвращаем список найденных контактов

def add_contact(contacts, last_name, first_name, phone, description):  # Функция для добавления нового контакта
    new_contact = {  # Создаем словарь для нового контакта
        'last_name': last_name.capitalize(),  # Фамилия с большой буквы
        'first_name': first_name.capitalize(),  # Имя с большой буквы
        'phone': phone,  # Номер телефона
        'description': description.capitalize()  # Описание с большой буквы
    }
    contacts.append(new_contact)  # Добавляем новый контакт в список
    print("Новая запись")  # Сообщаем о добавлении новой записи
    print(f"Фамилия: {new_contact['last_name']}")  # Печатаем фамилию
    print(f"Имя: {new_contact['first_name']}")  # Печатаем имя
    print(f"Телефон: {new_contact['phone']}")  # Печатаем номер телефона
    print(f"Описание: {new_contact['description']}")  # Печатаем описание

def update_contact_menu(contact):  # Функция для отображения меню изменения контакта
    while True:  # Бесконечный цикл для отображения меню
        print("\nЧто вы хотите изменить?")  # Печатаем меню
        print("1. Фамилия")
        print("2. Имя")
        print("3. Номер телефона")
        print("4. Описание")
        print("5. Вернуться в главное меню")

        choice = input("Выберите действие: ")  # Запрашиваем выбор пользователя

        if choice == '1':  # Если выбор - изменение фамилии
            new_last_name = input("Введите новую фамилию: ").capitalize()  # Запрашиваем новую фамилию
            contact['last_name'] = new_last_name  # Обновляем фамилию контакта
        elif choice == '2':  # Если выбор - изменение имени
            new_first_name = input("Введите новое имя: ").capitalize()  # Запрашиваем новое имя
            contact['first_name'] = new_first_name  # Обновляем имя контакта
        elif choice == '3':  # Если выбор - изменение номера телефона
            new_phone = input("Введите новый номер телефона: ")  # Запрашиваем новый номер телефона
            contact['phone'] = new_phone  # Обновляем номер телефона контакта
        elif choice == '4':  # Если выбор - изменение описания
            new_description = input("Введите новое описание: ").capitalize()  # Запрашиваем новое описание
            contact['description'] = new_description  # Обновляем описание контакта
        elif choice == '5':  # Если выбор - вернуться в главное меню
            break  # Прерываем цикл
        else:
            print("Неверный выбор, попробуйте снова.")  # Сообщаем о неверном выборе

def update_contact(contacts, term):  # Функция для поиска и изменения контакта
    results = search_contacts(contacts, term)  # Ищем контакты по терму
    if not results:  # Если контакты не найдены
        print("Информация не найдена.")  # Сообщаем об этом
        return False  # Возвращаем False
    else:
        print("Найденные контакты:")  # Сообщаем о найденных контактах
        display_contacts(results, highlight=term)  # Отображаем найденные контакты
        if len(results) == 1:  # Если найден один контакт
            contact = results[0]  # Получаем контакт
            update_contact_menu(contact)  # Открываем меню изменения контакта
            return True  # Возвращаем True
        else:
            print("Найдено несколько записей. Уточните критерии поиска.")  # Сообщаем о нескольких найденных записях
            return False  # Возвращаем False

def delete_contact(contacts, term):  # Функция для удаления контакта
    for contact in contacts:  # Перебираем все контакты
        if term.lower() in [value.lower() for value in contact.values()]:  # Если терм найден в контакте
            contacts.remove(contact)  # Удаляем контакт
            return True  # Возвращаем True
    return False  # Если контакт не найден, возвращаем False

def main():  # Главная функция программы
    contacts = load_data(FILENAME)  # Загружаем контакты из файла
    while True:  # Бесконечный цикл для отображения главного меню
        print("\nТелефонный справочник:")  # Печатаем меню
        print("1. Показать все контакты")
        print("2. Найти контакт")
        print("3. Добавить контакт")
        print("4. Изменить контакт")
        print("5. Удалить контакт")
        print("6. Сохранить и выйти")

        choice = input("Выберите действие: ")  # Запрашиваем выбор пользователя

        if choice == '1':  # Если выбор - показать все контакты
            display_contacts(contacts)  # Отображаем все контакты

        elif choice == '2':  # Если выбор - найти контакт
            term = input("Введите данные для поиска: ")  # Запрашиваем данные для поиска
            results = search_contacts(contacts, term)  # Ищем контакты по терму
            if results:  # Если контакты найдены
                display_contacts(results, highlight=term)  # Отображаем найденные контакты
            else:
                print("Контакт не найден.")  # Сообщаем, что контакт не найден

        elif choice == '3':  # Если выбор - добавить контакт
            last_name = input("Введите фамилию: ").capitalize()  # Запрашиваем фамилию
            first_name = input("Введите имя: ").capitalize()  # Запрашиваем имя
            phone = input("Введите номер телефона: ")  # Запрашиваем номер телефона
            description = input("Введите описание: ").capitalize()  # Запрашиваем описание
            add_contact(contacts, last_name, first_name, phone, description)  # Добавляем контакт

        elif choice == '4':  # Если выбор - изменить контакт
            term = input("Введите данные для поиска контакта, который нужно изменить: ")  # Запрашиваем данные для поиска контакта
            if not update_contact(contacts, term):  # Если контакт не найден или найдено несколько записей
                print("Контакт не найден или найдено несколько записей.")  # Сообщаем об этом

        elif choice == '5':  # Если выбор - удалить контакт
            term = input("Введите данные для поиска контакта, который нужно удалить: ")  # Запрашиваем данные для поиска контакта
            if not delete_contact(contacts, term):  # Если контакт не найден
                print("Контакт не найден.")  # Сообщаем об этом

        elif choice == '6':  # Если выбор - сохранить и выйти
            save_data(FILENAME, contacts)  # Сохраняем данные в файл
            print("Данные сохранены. Выход из программы.")  # Сообщаем о сохранении данных
            break  # Прерываем цикл и выходим из программы

        else:
            print("Неверный выбор, попробуйте снова.")  # Сообщаем о неверном выборе

if __name__ == "__main__":  # Если файл запущен напрямую, а не импортирован
    main()  # Запускаем главную функцию программы
