import psycopg2


with psycopg2.connect(host="127.0.0.1", database="Information_of_clients_db", user="postgres", password="trollhamaren123") as conn:

    def Create_table():
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """CREATE TABLE clients(
                        id_client serial PRIMARY KEY,
                        first_name varchar(50) NOT NULL,
                        last_name varchar(50) NOT NULL,
                        email varchar(50) NOT NULL UNIQUE);
                        
                        CREATE TABLE phone_number(
                        id_phone_number serial PRIMARY KEY,
                        phone_number_client BIGINT UNIQUE NULL CHECK 
                        (phone_number_client>0 and phone_number_client<9999999999));
                        
                        CREATE TABLE clients_number_phone(
                        client_id INTEGER REFERENCES clients(id_client),
                        phone_number_id INTEGER REFERENCES phone_number(id_phone_number));"""
                )
                print('Таблицы созданы!')
            conn.commit()
        except Exception as _ex:
            conn.commit()
            cursor.close()
            print('ОШИБКА: Таблица уже создана!',_ex)
    def Add_new_user(first_name_client, last_name_client, email_client, client_phone_number):
        try:

            with conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO clients (first_name, last_name, email) values (%s, %s, %s);""",
                    (first_name_client, last_name_client, email_client)
                )
            conn.commit()
        except Exception as _ex:
            conn.commit()
            cursor.close()
            print(_ex)
            return
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO phone_number (phone_number_client) VALUES (%s);""" % (client_phone_number)
                               )
            conn.commit()
        except Exception as _ex:
            conn.commit()
            cursor.close()
            print('Введён неверный номер!', _ex)
            return
        try:

            with conn.cursor() as cursor:
                cursor.execute("SELECT id_client FROM clients WHERE email = '%s';" % (email_client))
                id_client = cursor.fetchone()[0]
            with conn.cursor() as cursor:
                cursor.execute("SELECT id_phone_number FROM phone_number WHERE phone_number_client = '%s';" % client_phone_number)
                id_phone = cursor.fetchone()[0]
            with conn.cursor() as cursor:
                cursor.execute("""INSERT INTO clients_number_phone (client_id, phone_number_id) VALUES (%s, %s);""" %
                               (id_client, id_phone)
                               )
            conn.commit()
            print('Данные записаны в таблицу!')
        except Exception as _ex:
            conn.commit()
            cursor.close()
            print("Введены неверные данные.")
            return

    def Add_number_phone(id_user, number_phone):
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO phone_number (phone_number_client) VALUES ('%s');""" % (number_phone)
                )
            conn.commit()
        except Exception as _ex:
            conn.commit()
            cursor.close()
            print('Неверный номер!', _ex)
            return
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id_phone_number FROM phone_number WHERE phone_number_client = '%s';" % number_phone)
                id_phone = cursor.fetchone()[0]
                print(id_phone)
                with conn.cursor() as cursor:
                    cursor.execute("""INSERT INTO clients_number_phone (client_id, phone_number_id) VALUES (%s, %s);""" %
                                   (id_user, id_phone)
                                   )
                    conn.commit()
        except Exception as _ex:
            conn.commit()
            cursor.close()
            print('Введены некоректные данные!')
            return
    def Change_client_data(id_user):

        first_name_cange = input('Введите имя для изменения: ')
        last_name_change = input('Введите фамилию для изменения: ')
        email_cange = input('Введите email для изменения: ')
        number_phone_change = input('Введите номер телефона для изменения: ')
        try:
            with conn.cursor() as cursor:
                cursor.execute("""UPDATE clients SET first_name=%s, last_name=%s, email=%s WHERE id_client =%s;""",
                               (first_name_cange, last_name_change, email_cange, id_user)
                               )
            conn.commit()
        except Exception as _ex:
            conn.commit()
            cursor.close()
            print('Выввели неверные данные!', _ex)
            return
        try:
            with conn.cursor() as cursor:
                cursor.execute("""SELECT phone_number_id FROM clients_number_phone WHERE client_id = %s;""", id_user)
                id_phone = cursor.fetchone()[0]
            with conn.cursor() as cursor:
                cursor.execute("""UPDATE phone_number SET phone_number_client=%s WHERE id_phone_number = %s;""",
                               (number_phone_change, id_phone)
                               )
            conn.commit()
        except Exception as _ex:
            conn.commit()
            cursor.close()
            print('Вы ввели неверный номер!', _ex)
            return

    def Delete_phone(id_client):
        try:
            with conn.cursor() as cursor:
                cursor.execute("""SELECT count(phone_number_id) FROM clients_number_phone WHERE client_id = %s;""", id_client)
                id_phone_count = cursor.fetchone()[0]
            if id_phone_count > 1:
                with conn.cursor() as cursor:
                    cursor.execute("""SELECT phone_number_id FROM clients_number_phone WHERE client_id = %s;""", id_client)
                    for selection in cursor.fetchall():
                        with conn.cursor() as cursor:
                            cursor.execute(
                                """SELECT phone_number_client FROM phone_number WHERE id_phone_number = %s;""", selection)
                            list_phone = cursor.fetchall()
                            print('Номер телефона  - ', list_phone)
                delete_list_phone = input('Введите номер телефона для удаления: ')
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id_phone_number FROM phone_number WHERE phone_number_client = %s;" % delete_list_phone)
                    delete_id_phone = cursor.fetchone()[0]
                    print(delete_id_phone)
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM clients_number_phone WHERE phone_number_id = %s;" % delete_id_phone)
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM phone_number WHERE phone_number_client = %s;" % delete_list_phone)
                conn.commit()
                print('Удаление завершено!')
            elif id_phone_count == 1:
                with conn.cursor() as cursor:
                    cursor.execute("""SELECT phone_number_id FROM clients_number_phone WHERE client_id = %s;""", id_client)
                    delete_phone_id = cursor.fetchone()[0]
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM clients_number_phone WHERE phone_number_id = %s;" % delete_phone_id)
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM phone_number WHERE id_phone_number = %s;" % delete_phone_id)
                conn.commit()
                print('Удаление завершено!')
            elif id_phone_count == 0:
                print('У клиента нет ни одного номера телефона!')
            else:
                print('Вы ввели неверный id!')
        except Exception as _ex:
            conn.commit()
            cursor.close()
            print('Введены неверные данные!', _ex)
            return
    def Delete_client(id_client):
        t = []
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT phone_number_id FROM clients_number_phone WHERE client_id = %s;", id_client)
                for i in cursor.fetchall():
                    for o in i:
                        t.append(o)
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM clients_number_phone WHERE client_id = %s;" % id_client)
                conn.commit()
            for q in t:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM phone_number WHERE id_phone_number = %s;" % q)
                conn.commit()
        except Exception as _ex:
            conn.commit()
            cursor.close()
            print('Вы ввели неверные данные(id пользователя)', _ex)
            return
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM clients WHERE id_client = %s;" % id_client)
            conn.commit()
            print('Удаление завершено!')
        except Exception as _ex:
            conn.commit()
            cursor.close()
            print('Вы ввели неверные данные(id пользователя)', _ex)

    def Client_search(search_data):
        try:
            with conn.cursor() as cursor:
                cursor.execute("""SELECT clients.id_client, clients.first_name, clients.last_name, clients.email,
                phone_number.phone_number_client 
                FROM clients
                JOIN clients_number_phone ON clients.id_client = clients_number_phone.client_id
                JOIN phone_number ON clients_number_phone.phone_number_id = phone_number.id_phone_number
                WHERE clients.first_name LIKE '%s';""" % search_data
                               )
                result_search_first = cursor.fetchall()
                if result_search_first != []:
                    print(result_search_first)
                    return

            with conn.cursor() as cursor:
                cursor.execute("""SELECT clients.id_client, clients.first_name, clients.last_name, clients.email,
                phone_number.phone_number_client 
                FROM clients
                JOIN clients_number_phone ON clients.id_client = clients_number_phone.client_id
                JOIN phone_number ON clients_number_phone.phone_number_id = phone_number.id_phone_number
                WHERE clients.last_name LIKE '%s';""" % search_data
                               )
                result_search_last = cursor.fetchall()
                if result_search_last != []:
                    print(result_search_last)
                    return


            with conn.cursor() as cursor:
                cursor.execute("""SELECT clients.id_client, clients.first_name, clients.last_name, clients.email,
                phone_number.phone_number_client 
                FROM clients
                JOIN clients_number_phone ON clients.id_client = clients_number_phone.client_id
                JOIN phone_number ON clients_number_phone.phone_number_id = phone_number.id_phone_number
                WHERE clients.email LIKE '%s';""" % search_data
                               )
                result_search_email = cursor.fetchall()
                if result_search_email != []:
                    print(result_search_email)
                    return


            with conn.cursor() as cursor:
                cursor.execute("""SELECT clients.id_client, clients.first_name, clients.last_name, clients.email,
                phone_number.phone_number_client 
                FROM clients
                JOIN clients_number_phone ON clients.id_client = clients_number_phone.client_id
                JOIN phone_number ON clients_number_phone.phone_number_id = phone_number.id_phone_number
                WHERE phone_number.phone_number_client = %s;""" % search_data
                               )
                result_search_phone = cursor.fetchall()
                if result_search_phone != []:
                    print(result_search_phone)
                    return
                if result_search_first == [] and result_search_last == [] and result_search_email == [] and result_search_phone == []:
                    print('Пользователя с такими данными не найдено!')
        except Exception as _ex:
            conn.commit()
            cursor.close()
            print('Вы ввели неверные данные!', _ex)
            return


command_db = 0
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
while command_db != 'exit':
    command_db = input('Введите команду: ')
    if command_db == "1":
        Create_table()
    elif command_db == "2":
        first_name = input('Введите имя: ')
        last_name = input('Введите фамилию: ')
        email = str(input('Введите email: '))
        phone_number = input('Введите номер телефона в формате 9181111111: ')
        Add_new_user(first_name, last_name, email, phone_number)
    elif command_db == "3":
        id_user = input('Введите id клиента: ')
        number_phone = input('Введите номер телефона: ')
        Add_number_phone(id_user, number_phone)
    elif command_db == "4":
        id_user_change = input('Введите id пользователя: ')
        Change_client_data(id_user_change)
    elif command_db == "5":
        id_client_delete_phone = input('Ввеите id клиента: ')
        Delete_phone(id_client_delete_phone)
    elif command_db == "6":
        id_client_delete = input('Введите id клиента: ')
        Delete_client(id_client_delete)
    elif command_db == "7":
        search_data = input("Введите данные для поиска (имя, фамилия, email или телефон):")
        Client_search(search_data)
conn.close()
