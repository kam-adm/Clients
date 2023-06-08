import psycopg2


def Create_table(cursor):
    try:
        cursor.execute(
            """CREATE TABLE clients(
                id_client serial PRIMARY KEY,
                first_name varchar(50) NOT NULL,
                last_name varchar(50) NOT NULL,
                email varchar(50) NOT NULL UNIQUE);
                
                CREATE TABLE phone_number(
                id_phone_number serial PRIMARY KEY,
                client_id INTEGER REFERENCES clients(id_client),
                phone_number_client BIGINT UNIQUE NULL CHECK 
                (phone_number_client>0 and phone_number_client<99999999999));"""
        )
        print('Таблицы созданы!')
    except Exception as _ex:
        conn.commit()
        print('ОШИБКА: Таблица уже создана!', _ex)
    conn.commit()
def Add_new_user(cursor, first_name_client, last_name_client, email_client, client_phone_number):
    try:
        cursor.execute(
            """INSERT INTO clients (first_name, last_name, email) values (%s, %s, %s);""",
            (first_name_client, last_name_client, email_client)
        )
    except Exception as _ex:
        print(_ex)
        conn.commit()
        return
    try:
        cursor.execute("SELECT id_client FROM clients WHERE email = '%s';" % (email_client))
        id_client = cursor.fetchone()[0]
        cursor.execute(
            """INSERT INTO phone_number (phone_number_client, client_id) VALUES (%s, %s);""" % (client_phone_number, id_client))
    except Exception as _ex:
        print(_ex)
        conn.commit()
        return
    conn.commit()
    print('Пользователь успешно добавлен!')
def Add_number_phone(cursor, id_user, number_phone):
    try:
        cursor.execute(
            """INSERT INTO phone_number (client_id, phone_number_client) VALUES ('%s', '%s');""" % (id_user, number_phone)
        )

    except Exception as _ex:
        print('Неверный номер!', _ex)
        conn.commit()
        return
    conn.commit()
    print('Номер телефона успешно добавлен!')

def Change_client_data(cursor, id_user , data_change, command_change ):
    if command_change == "1":
        try:
            cursor.execute("""UPDATE clients SET first_name=%s WHERE id_client =%s;""",
                           (data_change, id_user)
                           )
        except Exception as _ex:
            print('Выввели неверные данные!', _ex)
            conn.commit()
            return
        conn.commit()
    elif command_change == "2":
        try:
            cursor.execute("""UPDATE clients SET last_name=%s WHERE id_client =%s;""",
                           (data_change, id_user)
                           )
        except Exception as _ex:
            print('Выввели неверные данные!', _ex)
            conn.commit()
            return
        conn.commit()
    elif command_change == "3":
        try:
            cursor.execute("""UPDATE clients SET email=%s WHERE id_client =%s;""",
                           (data_change, id_user)
                           )
        except Exception as _ex:
            print('Выввели неверные данные!', _ex)
            conn.commit()
            return
        conn.commit()
    elif command_change == "4":
        try:
            cursor.execute("""SELECT count(id_phone_number) FROM phone_number WHERE client_id = %s;""", id_user)
            id_phone_count = cursor.fetchone()[0]
            if id_phone_count > 1:
                cursor.execute("""SELECT id_phone_number FROM phone_number WHERE client_id = %s;""", id_user)
                for selection in cursor.fetchall():
                    cursor.execute(
                        """SELECT phone_number_client FROM phone_number WHERE id_phone_number = %s;""", selection)
                    list_phone_change = cursor.fetchall()
                    print(f'Номер телефона  -  {list_phone_change}')
                change_phone = input('Введите номер телефона который нужно изменить: ')
                cursor.execute(
                    """UPDATE phone_number SET phone_number_client = %s WHERE phone_number_client = %s;""",
                    (data_change, change_phone))
                print('Изменение завершено успешно!')
            elif id_phone_count == 1:
                cursor.execute("""UPDATE phone_number SET phone_number_client=%s WHERE client_id = %s;""" %
                               (data_change, id_user)
                               )
            elif id_phone_count == 0:
                print('У пользователя нет телефона!')

        except Exception as _ex:
            print('Вы ввели неверный номер!', _ex)
            conn.commit()
            return
        conn.commit()


def Delete_phone(cursor, id_client):
    try:
        cursor.execute("""SELECT count(id_phone_number) FROM phone_number WHERE client_id = %s;""", id_client)
        id_phone_count = cursor.fetchone()[0]
        if id_phone_count > 1:
            cursor.execute("""SELECT phone_number_client FROM phone_number WHERE client_id = %s;""", id_client)
            for selection in cursor.fetchall():
                list_phone = selection
                print(f'Номер телефона  -  {list_phone}')
            delete_phone = input('Введите номер телефона для удаления: ')
            cursor.execute("DELETE FROM phone_number WHERE phone_number_client = %s;" % delete_phone)
            print('Удаление завершено!')
        elif id_phone_count == 1:
            cursor.execute("DELETE FROM phone_number WHERE client_id = %s;" % id_client)
            print('Удаление завершено!')
        elif id_phone_count == 0:
            print('У клиента нет ни одного номера телефона!')
        else:
            print('Вы ввели неверный id!')
    except Exception as _ex:
        print('Введены неверные данные!', _ex)
        conn.commit()
        return
    conn.commit()
def Delete_client(cursor, id_client):
    try:
        cursor.execute("DELETE FROM phone_number WHERE client_id = %s;" % id_client)
        cursor.execute("DELETE FROM clients WHERE id_client = %s;" % id_client)
        print('Удаление завершено!')
    except Exception as _ex:
        print('Вы ввели неверные данные(id пользователя)', _ex)
        conn.commit()
    conn.commit()

def Client_search(cursor, search_data):
    try:
        cursor.execute(f"""SELECT clients.id_client, clients.first_name, clients.last_name, clients.email,
        phone_number.phone_number_client 
        FROM clients
        JOIN phone_number ON clients.id_client = phone_number.client_id
        WHERE clients.first_name = '{search_data}' OR clients.last_name = '{search_data}' 
        OR clients.email = '{search_data}';""")
        a = cursor.fetchall()
        if a != []:
            print(f'{a}')
        elif a == []:
            cursor.execute(f"""SELECT clients.id_client, clients.first_name, clients.last_name, clients.email,
            phone_number.phone_number_client 
            FROM clients
            JOIN phone_number ON clients.id_client = phone_number.client_id
            WHERE phone_number.phone_number_client = '{search_data}';""")
            a = cursor.fetchall()
            if a != []:
                print(a)
            elif a == []:
                print('Выввели неверные данные!')
    except Exception as _ex:
        print('Вы ввели неверные данные')
        conn.commit()
    conn.commit()

if __name__ == "__main__":

    with psycopg2.connect(host="127.0.0.1", database="", user="",
                              password="") as conn:
        with conn.cursor() as cur:

            print('''Выберите значение команды:
              1 - Создать структуру БД
              2 - Создать клиента
              3 - Добавить номер телефона существующему клиенту
              4 - Изменить существующего клиента
              5 - Удалить номер телефона
              6 - Удалить клиента
              7 - Поиск клиента по его данным: имени, фамилии, email или телефону
              Введите exit для выхода из программы.\n'''
                  )

            command_db = 0
            while command_db != 'exit':
                command_db = input('Введите команду: ')
                if command_db == "1":
                    Create_table(cur)
                elif command_db == "2":
                    first_name = input('Введите имя: ')
                    last_name = input('Введите фамилию: ')
                    email = str(input('Введите email: '))
                    phone_number = input('Введите номер телефона в формате 89181111111: ')
                    Add_new_user(cur, first_name, last_name, email, phone_number)
                elif command_db == "3":
                    id_user = input('Введите id клиента: ')
                    number_phone = input('Введите номер телефона: ')
                    Add_number_phone(cur, id_user, number_phone)
                elif command_db == "4":
                    print("""Какие данные вы хотите изменить
                    1 -  Имя
                    2 -  Фамилия
                    3 -  email
                    4 -  номер телефона""")
                    command_change = input('Введите комманду: ')
                    id_user_change = input('Введите id пользователя: ')
                    if command_change == "1":
                        first_name_cange = input('Введите имя для изменения: ')
                        Change_client_data(cur, id_user_change, first_name_cange, command_change)
                    elif command_change == "2":
                        last_name_change = input('Введите фамилию для изменения: ')
                        Change_client_data(cur, id_user_change, last_name_change, command_change)
                    elif command_change == "3":
                        email_change = input('Введите email для изменения: ')
                        Change_client_data(cur, id_user_change, email_change, command_change)
                    elif command_change == "4":
                        number_phone_change = input('Введите номер телефона для изменения: ')
                        Change_client_data(cur, id_user_change, number_phone_change, command_change)
                    else:
                        print('Вы ввели неверную комманду!')
                elif command_db == "5":
                    id_client_delete_phone = input('Ввеите id клиента: ')
                    Delete_phone(cur, id_client_delete_phone)
                elif command_db == "6":
                    id_client_delete = input('Введите id клиента: ')
                    Delete_client(cur, id_client_delete)
                elif command_db == "7":
                    search_data = input("Введите данные для поиска (имя, фамилия, email или телефон):")
                    Client_search(cur, search_data)
    conn.close()
