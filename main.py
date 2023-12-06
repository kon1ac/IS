import sqlite3
import sys
import msvcrt


# Класс для представления сотрудника
class Employee:
    def __init__(self, id, username, password, role, name=None):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
        self.name = name


# Класс информационной системы для тату-салона
class TattooShopSystem:
    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS employees
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             username TEXT NOT NULL,
                             password TEXT NOT NULL,
                             role TEXT NOT NULL)''')
        self.conn.commit()

    def register_employee(self, username, password, role):
        self.cursor.execute('INSERT INTO employees (username, password, role) VALUES (?, ?, ?)',
                            (username, password, role))
        self.conn.commit()
        print('Employee registered successfully!')

    def login(self):
        while True:
            username = input('Enter username: ')
            password = input('Enter password: ')
            self.cursor.execute('SELECT * FROM employees WHERE username = ? AND password = ?',
                                (username, password))
            row = self.cursor.fetchone()
            if row:
                employee = Employee(row[0], row[1], row[2], row[3])
                print('Login successful!')
                return employee
            else:
                print('Invalid username or password. Please try again.')

    def get_employee_name(self, employee):
        if employee.role == 'human_resources_manager':
            self.cursor.execute('SELECT name FROM employees WHERE username = ?',
                                (employee.username,))
            row = self.cursor.fetchone()
            if row:
                employee.name = row[0]

    def close_connection(self):
        self.conn.close()


# Отображение меню пунктов
def show_menu():
    print('1. View Sales Report')  # select * from tattoo
    print('2. Add New Tattoo')  # create from crud
    print('3. Update Tattoo Price')  # update from crud
    print('4. Delete Tattoo')  # delete from crud
    print('5. Exit')  # sys.exit(0)


# Функция для обработки ввода клавиш в меню
def process_selection(employee):
    while True:
        if msvcrt.kbhit():  # Проверка на наличие нажатия клавиши
            key = msvcrt.getch()
            if key == b'\x1b':  # ESC
                return
            elif key == b'1':
                print('Viewing Sales Report')
                # Реализация функционала просмотра отчета о продажах
            elif key == b'2':
                print('Adding New Tattoo')
                # Реализация функционала добавления новой татуировки
            elif key == b'3':
                print('Updating Tattoo Price')
                # Реализация функционала обновления цены татуировки
            elif key == b'4':
                print('Deleting Tattoo')
                # Реализация функционала удаления татуировки
            elif key == b'5':
                sys.exit(0)
            else:
                print('Invalid selection. Please try again.')


# Пример использования
def main():
    tattoo_system = TattooShopSystem('tattoo_shop.db')

    # Регистрация сотрудников
    tattoo_system.register_employee('admin', 'admin123', 'admin')
    tattoo_system.register_employee('cashier', 'cashier123', 'cashier')
    tattoo_system.register_employee('hr_manager', 'hr123', 'hr_manager')

    # Авторизация
    employee = tattoo_system.login()

    # Получение имени сотрудника (если есть)
    tattoo_system.get_employee_name(employee)

    # Вывод имени или логина после авторизации
    if employee.name:
        print(f'Welcome, {employee.name}!')
    else:
        print(f'Welcome, {employee.username}!')

    while True:
        # Вывод меню
        show_menu()

        # Обработка выбора пункта
        process_selection(employee)

    tattoo_system.close_connection()


if __name__ == '__main__':
    main()
