import tkinter as tk  # Импортируем библиотеку tkinter для создания графического интерфейса
from tkinter import messagebox, simpledialog  # Импортируем дополнительные модули для диалоговых окон

FILENAME = 'phone.txt'

# Функция для загрузки данных из файла
def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:  # Открываем файл для чтения
        lines = file.readlines()  # Читаем все строки из файла
    contacts = [  # Используем списковое включение для создания списка контактов
        {'last_name': parts[0].strip().capitalize(),
         'first_name': parts[1].strip().capitalize(),
         'phone': parts[2].strip(),
         'description': parts[3].strip().capitalize()}
        for line in lines if (parts := line.split(',')) and len(parts) == 4
        # Проверяем, что строка разделена на 4 части
    ]
    return contacts  # Возвращаем список контактов


# Функция для сохранения данных в файл
def save_data(filename, contacts):
    with open(filename, 'w', encoding='utf-8') as file:  # Открываем файл для записи
        file.writelines(  # Записываем контакты в файл
            f"{contact['last_name']}, {contact['first_name']}, {contact['phone']}, {contact['description']}\n"
            for contact in contacts  # Перебираем все контакты
        )


# Функция для отображения контактов в Listbox
def display_contacts(listbox, contacts):
    listbox.delete(0, tk.END)  # Очищаем Listbox
    for contact in contacts:  # Перебираем все контакты
        listbox.insert(tk.END,
                       f"{contact['last_name']} {contact['first_name']} - {contact['phone']} - {contact['description']}")  # Добавляем каждый контакт в Listbox


# Функция для поиска контактов по заданному терму
def search_contacts(contacts, term):
    term = term.lower()  # Приводим терм к нижнему регистру
    return [contact for contact in contacts if any(
        term in value.lower() for value in contact.values())]  # Возвращаем список контактов, которые содержат терм


# Функция для добавления нового контакта
def add_contact(contacts, last_name, first_name, phone, description):
    new_contact = {  # Создаем словарь для нового контакта
        'last_name': last_name.capitalize(),
        'first_name': first_name.capitalize(),
        'phone': phone,
        'description': description.capitalize()
    }
    contacts.append(new_contact)  # Добавляем новый контакт в список контактов
    messagebox.showinfo("Новая запись",
                        f"Фамилия: {new_contact['last_name']}\nИмя: {new_contact['first_name']}\nТелефон: {new_contact['phone']}\nОписание: {new_contact['description']}")  # Показываем сообщение с данными нового контакта


# Функция для отображения меню изменения контакта
def update_contact_menu(contact, refresh_display):
    fields = ['last_name', 'first_name', 'phone', 'description']  # Поля контакта
    field_names = ['Фамилия', 'Имя', 'Номер телефона', 'Описание']  # Имена полей

    def update_field(field_index):  # Вложенная функция для изменения поля контакта
        new_value = simpledialog.askstring("Изменить контакт",
                                           f"Введите новое {field_names[field_index].lower()}: ").capitalize()  # Запрашиваем новое значение
        if new_value:
            contact[fields[field_index]] = new_value  # Обновляем поле контакта
            refresh_display()  # Обновляем отображение контактов

    update_window = tk.Toplevel()  # Создаем новое окно
    update_window.title("Изменить контакт")  # Устанавливаем заголовок окна

    for i, name in enumerate(field_names):  # Перебираем все имена полей
        tk.Button(update_window, text=f"Изменить {name}", command=lambda i=i: update_field(i)).pack(
            pady=5)  # Создаем кнопку для изменения поля

    tk.Button(update_window, text="Вернуться в главное меню", command=update_window.destroy).pack(
        pady=5)  # Создаем кнопку для закрытия окна


# Функция для поиска и изменения контакта
def update_contact(contacts, listbox, refresh_display):
    term = simpledialog.askstring("Изменить контакт",
                                  "Введите данные для поиска контакта, который нужно изменить:")  # Запрашиваем терм для поиска
    results = search_contacts(contacts, term)  # Ищем контакты
    if not results:
        messagebox.showinfo("Результат поиска",
                            "Информация не найдена.")  # Если контакты не найдены, показываем сообщение
    elif len(results) == 1:
        messagebox.showinfo("Найденные контакты",
                            f"{results[0]['last_name']} {results[0]['first_name']} - {results[0]['phone']} - {results[0]['description']}")  # Если найден один контакт, показываем его
        update_contact_menu(results[0], refresh_display)  # Открываем меню изменения контакта
    else:
        messagebox.showinfo("Результат поиска",
                            "Найдено несколько записей. Уточните критерии поиска.")  # Если найдено несколько контактов, показываем сообщение
        for contact in results:  # Перебираем все найденные контакты
            messagebox.showinfo("Контакт",
                                f"{contact['last_name']} {contact['first_name']} - {contact['phone']} - {contact['description']}")  # Показываем каждый контакт


# Функция для удаления контакта
def delete_contact(contacts, listbox):
    term = simpledialog.askstring("Удалить контакт",
                                  "Введите данные для поиска контакта, который нужно удалить:")  # Запрашиваем терм для поиска
    result = next((contact for contact in contacts if term.lower() in [value.lower() for value in contact.values()]),
                  None)  # Ищем контакт
    if result:
        contacts.remove(result)  # Удаляем контакт
        display_contacts(listbox, contacts)  # Обновляем отображение контактов
        messagebox.showinfo("Результат удаления", "Контакт удален.")  # Показываем сообщение об успешном удалении
    else:
        messagebox.showinfo("Результат удаления", "Контакт не найден.")  # Показываем сообщение, если контакт не найден


# Кастомное диалоговое окно для добавления контакта
class ContactDialog(simpledialog.Dialog):
    def body(self, master):
        self.title("Добавить контакт")  # Устанавливаем заголовок окна

        tk.Label(master, text="Фамилия:").grid(row=0)  # Метка для ввода фамилии
        tk.Label(master, text="Имя:").grid(row=1)  # Метка для ввода имени
        tk.Label(master, text="Телефон:").grid(row=2)  # Метка для ввода телефона
        tk.Label(master, text="Описание:").grid(row=3)  # Метка для ввода описания

        self.last_name_entry = tk.Entry(master)  # Поле ввода для фамилии
        self.first_name_entry = tk.Entry(master)  # Поле ввода для имени
        self.phone_entry = tk.Entry(master)  # Поле ввода для телефона
        self.description_entry = tk.Entry(master)  # Поле ввода для описания

        self.last_name_entry.grid(row=0, column=1)  # Размещаем поле ввода для фамилии
        self.first_name_entry.grid(row=1, column=1)  # Размещаем поле ввода для имени
        self.phone_entry.grid(row=2, column=1)  # Размещаем поле ввода для телефона
        self.description_entry.grid(row=3, column=1)  # Размещаем поле ввода для описания

        return self.last_name_entry  # Возвращаем начальное поле для фокуса

    def apply(self):
        self.last_name = self.last_name_entry.get().capitalize()  # Получаем и капитализируем фамилию
        self.first_name = self.first_name_entry.get().capitalize()  # Получаем и капитализируем имя
        self.phone = self.phone_entry.get()  # Получаем телефон
        self.description = self.description_entry.get().capitalize()  # Получаем и капитализируем описание


# Главный класс приложения
class PhonebookApp(tk.Tk):
    def __init__(self):
        super().__init__()  # Инициализация базового класса
        self.title("Телефонный справочник")  # Устанавливаем заголовок окна
        self.geometry("800x400")  # Устанавливаем размер окна

        self.contacts = load_data(FILENAME)  # Загружаем контакты

        self.create_widgets()  # Создаем виджеты
        self.refresh_display()  # Обновляем отображение контактов

    def create_widgets(self):
        self.listbox = tk.Listbox(self, width=80, height=20)  # Создаем Listbox для отображения контактов
        self.listbox.pack(side=tk.LEFT, padx=10, pady=10)  # Размещаем Listbox в окне

        button_frame = tk.Frame(self)  # Создаем фрейм для кнопок
        button_frame.pack(side=tk.RIGHT, padx=10, pady=10)  # Размещаем фрейм в окне

        self.add_button = tk.Button(button_frame, text="Добавить контакт",
                                    command=self.add_contact)  # Кнопка для добавления контакта
        self.add_button.pack(pady=5)  # Размещаем кнопку

        self.update_button = tk.Button(button_frame, text="Изменить контакт",
                                       command=lambda: update_contact(self.contacts, self.listbox,
                                                                      self.refresh_display))  # Кнопка для изменения контакта
        self.update_button.pack(pady=5)  # Размещаем кнопку

        self.delete_button = tk.Button(button_frame, text="Удалить контакт",
                                       command=lambda: delete_contact(self.contacts,
                                                                      self.listbox))  # Кнопка для удаления контакта
        self.delete_button.pack(pady=5)  # Размещаем кнопку

        self.save_exit_button = tk.Button(button_frame, text="Сохранить и выйти",
                                          command=self.save_and_exit)  # Кнопка для сохранения и выхода
        self.save_exit_button.pack(pady=5)  # Размещаем кнопку

    def add_contact(self):
        dialog = ContactDialog(self)  # Открываем диалоговое окно для добавления контакта
        if dialog.last_name and dialog.first_name and dialog.phone and dialog.description:  # Проверяем, что все поля заполнены
            add_contact(self.contacts, dialog.last_name, dialog.first_name, dialog.phone,
                        dialog.description)  # Добавляем контакт
            self.refresh_display()  # Обновляем отображение контактов

    def refresh_display(self):
        display_contacts(self.listbox, self.contacts)  # Обновляем отображение контактов в Listbox

    def save_and_exit(self):
        save_data(FILENAME, self.contacts)  # Сохраняем контакты в файл
        messagebox.showinfo("Сохранение данных",
                            "Данные сохранены. Программа завершена.")  # Показываем сообщение о сохранении
        self.destroy()  # Закрываем окно


if __name__ == "__main__":
    app = PhonebookApp()  # Создаем экземпляр приложения
    app.mainloop()  # Запускаем главный цикл приложения
