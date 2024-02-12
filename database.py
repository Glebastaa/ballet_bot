import psycopg2


# Функция для подключения к базе данных
def connect_db():
    return psycopg2.connect(
        dbname="ballet",
        user="postgres",
        password="4errmpag2134!zjv",
        host="localhost",
        port="5432",
    )


conn = connect_db()


# Добавление студии
def add_studio(studio_name):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO studios (studio_name) VALUES (%s)",
                    (studio_name,))
        conn.commit()
    return studio_name


# Удаления студии
def delete_studio(studio_name):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM studios WHERE studio_name = %s;",
                    (studio_name,))
        conn.commit()
    return studio_name


# Редактирование имени студии
def edit_studio(studio_name, new_studio_name):
    with conn.cursor() as cur:
        cur.execute("UPDATE studios SET studio_name = %s WHERE studio_name = %s;",
                    (new_studio_name, studio_name))
        conn.commit()
    return new_studio_name


# Список студий
def get_studios():
    with conn.cursor() as cur:
        cur.execute("SELECT studio_name FROM studios")
        studios = cur.fetchall()
    return [studio[0] for studio in studios]


"""Тута будет все про группы"""

# Добавление группы
def add_group(group_name, studio_name, start_time, start_date):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO groups (group_name, studio_name, start_time, start_date) VALUES (%s, %s, %s, %s)",
                    (group_name, studio_name, start_time, start_date))
        conn.commit()
    return group_name


# Получение списка групп
def get_groups(studio_name):
    with conn.cursor() as cur:
        cur.execute("SELECT group_name FROM groups WHERE studio_name = %s",
                    (studio_name,))
        groups = cur.fetchall()
    return [group[0] for group in groups]


# Редактирование имени группы
def edit_group(group_name, new_group_name, studio_name):
    with conn.cursor() as cur:
        cur.execute("UPDATE groups SET group_name = %s WHERE group_name = %s AND studio_name = %s;",
                    (new_group_name, group_name, studio_name))
        conn.commit()
    return new_group_name


# Удаление группы
def delete_group(group_name, studio_name):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM groups WHERE group_name = %s AND studio_name = %s;",
                    (group_name, studio_name))
        conn.commit()
    return group_name


# Получения даты и времени группы
def date_time_group(group_name, studio_name):
    with conn.cursor() as cur:
        cur.execute("SELECT start_date, start_time FROM groups WHERE group_name = %s AND studio_name = %s",
                    (group_name, studio_name))
        group = cur.fetchone()
    return group
