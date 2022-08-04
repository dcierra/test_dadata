import sqlite3
from dadata import Dadata


def create_bd(url, api_key, change_language):
    conn = sqlite3.connect('settings.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS settings_list(url text, api_key text, change_language text)")
    cur.execute("INSERT INTO settings_list VALUES (:url, :api, :lang)", {'url': url, 'api': api_key, 'lang': change_language})
    conn.commit()
    conn.close()


def get_bd():
    conn = sqlite3.connect('settings.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM settings_list")
    data = cur.fetchall()
    conn.commit()
    conn.close()
    return data


def clear_bd():
    conn = sqlite3.connect('settings.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM settings_list')
    conn.commit()
    conn.close()


def get_info(dadata_connect, change_language):
    value = input("Введите адрес(в свободной форме): ")
    res = dadata_connect.suggest(name="address", query=value, language=change_language)
    for i in range(len(res)):
        print(f'{i} - {res[i]["value"]}')
    ans = int(input(f'Для продолжения выберите цифру с подходящим адресом: '))
    print(f'\nВы выбрали адрес: {res[ans]["value"]}\nЕго широта: {res[ans]["data"]["geo_lat"]}\nЕго долгота: {res[ans]["data"]["geo_lon"]}')


def change_settings():
    url = input('Для работы программы введите следующие данные:\nБазовый URL к сервису dadata(оставьте поле пустым'
                ' для того, чтобы применить значение по умолчанию(): ')
    api_key = input('API ключ для сервиса dadata - ')
    change_language = input('Язык(оставьте поле пустым для того, чтобы применить значение по умолчанию(ru): ')

    if len(url) == 0: url = "8e0bc9474c6d49bb6c3e07fdde92ac1f0eca80cb"
    if len(change_language) == 0: change_language = "ru"

    dadata_connect = Dadata(api_key, url)
    create_bd(url, api_key, change_language)
    return dadata_connect, change_language


def main_f():
    dadata_connect = change_settings()
    get_info(dadata_connect[0], dadata_connect[1])


main_f()
while (input("\nВы желаете выйти?(Да/Нет) \n").lower()) != "да":
    main_f()

ans = input("Хотите очистить БД с настройками?(Да/Нет) ").lower()
if (ans == "да"):
    clear_bd()
