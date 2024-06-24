FILENAME = 'phone.txt'  # Имя файла, в котором хранятся данные телефонного справочника

def load_data(filename):  # Функция для загрузки данных из файла
    with open(filename, 'r', encoding='utf-8') as file:  # Открываем файл для чтения с указанием кодировки
        lines = file.readlines()  # Читаем все строки из файла
    contacts = [  # Создаем список контактов, используя списковое включение
        {'last_name': parts[0].strip().capitalize(),  # Фамилия с большой буквы
         'first_name': parts[1].strip().capitalize(),  # Имя с большой буквы
         'phone': parts[2].strip(),  # Номер телефона
         'description': parts[3].strip().capitalize()}  # Описание с большой буквы
        for line in lines if (parts := line.split(',')) and len(parts) == 4  # Разделяем строки на части и проверяем, что их четыре
    ]
    return contacts  # Возвращаем список контактов

def save_data(filename, contacts):  # Функция для сохранения данных в файл
    with open(filename, 'w', encoding='utf-8') as file:  # Открываем файл для записи с указанием кодировки
        file.writelines(  # Записываем контакты в файл
            f"{contact['last_name']}, {contact['first_name']}, {contact['phone']}, {contact['description']}\n"  # Форматируем строку для записи
            for contact in contacts  # Перебираем все контакты
        )

def display_contacts(contacts, highlight=None):  # Функция для отображения контактов
    if not contacts:  # Проверяем, что список контактов не пуст
        print("Контакты не найдены.")  # Сообщаем, что контакты не найдены
        return  # Выходим из функции
    for contact in contacts:  # Перебираем все контакты
        output = f"{contact['last_name']} {contact['first_name']} - {contact['phone']} - {contact['description']}"  # Форматируем строку для отображения
        if highlight and any(highlight.lower() in value.lower() for value in contact.values()):  # Проверяем, нужно ли выделить строку
            output = f"\033[1;32m{output}\033[0m"  # Выделяем строку зеленым цветом
        print(output)  # Печатаем строку

def search_contacts(contacts, term):  # Функция для поиска контактов по терму
    term = term.lower()  # Приводим терм к нижнему регистру
    return [contact for contact in contacts if any(term in value.lower() for value in contact.values())]  # Возвращаем список найденных контактов

def add_contact(contacts, last_name, first_name, phone, description):  # Функция для добавления нового контакта
    new_contact = {  # Создаем словарь для нового контакта
        'last_name': last_name.capitalize(),  # Фамилия с большой буквы
        'first_name': first_name.capitalize(),  # Имя с большой буквы
        'phone': phone,  # Номер телефона
        'description': description.capitalize()  # Описание с большой буквы
    }
    contacts.append(new_contact)  # Добавляем новый контакт в список
    print("Новая запись")  # Сообщаем о добавлении новой записи
    display_contacts([new_contact])  # Отображаем новый контакт

def update_contact_menu(contact):  # Функция для отображения меню изменения контакта
    fields = ['last_name', 'first_name', 'phone', 'description']  # Поля контакта
    field_names = ['Фамилия', 'Имя', 'Номер телефона', 'Описание']  # Имена полей
    while True:  # Бесконечный цикл для отображения меню
        print("\nЧто вы хотите изменить?")  # Печатаем меню
        for i, name in enumerate(field_names, 1):  # Перебираем имена полей с номерами
            print(f"{i}. {name}")  # Печатаем номер и имя поля
        print("5. Вернуться в главное меню")  # Печатаем опцию возврата в главное меню
        choice = input("Выберите действие: ")  # Запрашиваем выбор пользователя
        if choice in map(str, range(1, 5)):  # Если выбор в диапазоне от 1 до 4
            new_value = input(f"Введите новое {field_names[int(choice) - 1].lower()}: ").capitalize()  # Запрашиваем новое значение
            contact[fields[int(choice) - 1]] = new_value  # Обновляем поле контакта
        elif choice == '5':  # Если выбор - возврат в главное меню
            break  # Прерываем цикл
        else:
            print("Неверный выбор, попробуйте снова.")  # Сообщаем о неверном выборе

def update_contact(contacts, term):  # Функция для поиска и изменения контакта
    results = search_contacts(contacts, term)  # Ищем контакты по терму
    if not results:  # Если контакты не найдены
        print("Информация не найдена.")  # Сообщаем об этом
    elif len(results) == 1:  # Если найден один контакт
        print("Найденные контакты:")  # Сообщаем о найденных контактах
        display_contacts(results, highlight=term)  # Отображаем найденный контакт
        update_contact_menu(results[0])  # Открываем меню изменения контакта
    else:
        print("Найдено несколько записей. Уточните критерии поиска.")  # Сообщаем о нескольких найденных записях
        display_contacts(results, highlight=term)  # Отображаем найденные контакты

def delete_contact(contacts, term):  # Функция для удаления контакта
    result = next((contact for contact in contacts if term.lower() in [value.lower() for value in contact.values()]), None)  # Ищем контакт
    if result:  # Если контакт найден
        contacts.remove(result)  # Удаляем контакт
        return True  # Возвращаем True
    return False  # Если контакт не найден, возвращаем False

def main():  # Главная функция программы
    contacts = load_data(FILENAME)  # Загружаем контакты из файла
    actions = {  # Словарь для выбора действий
        '1': lambda: display_contacts(contacts),  # Показать все контакты
        '2': lambda: display_contacts(search_contacts(contacts, term := input("Введите характеристику для поиска: ")), highlight=term),  # Найти контакт
        '3': lambda: add_contact(  # Добавить контакт
            contacts,
            input("Введите фамилию: ").capitalize(),
            input("Введите имя: ").capitalize(),
            input("Введите номер телефона: "),
            input("Введите описание: ").capitalize()
        ),
        '4': lambda: update_contact(contacts, input("Введите данные для поиска контакта, который нужно изменить: ")),  # Изменить контакт
        '5': lambda: print("Контакт не найден.") if not delete_contact(contacts, input("Введите данные для поиска контакта, который нужно удалить: ")) else print("Контакт удален."),  # Удалить контакт
        '6': lambda: (save_data(FILENAME, contacts), print("Данные сохранены. Выход из программы."), exit())  # Сохранить и выйти
    }
    while True:  # Бесконечный цикл для отображения главного меню
        print("\nТелефонный справочник:")  # Печатаем меню
        for i, action in enumerate(["Показать все контакты", "Найти контакт", "Добавить контакт", "Изменить контакт", "Удалить контакт", "Сохранить и выйти"], 1):  # Перебираем все действия с номерами
            print(f"{i}. {action}")  # Печатаем номер и действие
        choice = input("Выберите действие: ")  # Запрашиваем выбор пользователя
        actions.get(choice, lambda: print("Неверный выбор, попробуйте снова."))()  # Выполняем выбранное действие или сообщаем о неверном выборе

if __name__ == "__main__":  # Проверяем, что файл запущен напрямую, а не импортирован
    main()  # Запускаем главную функцию программы


