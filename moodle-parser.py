import requests
import re
from bs4 import BeautifulSoup
import json
from getpass import getpass


# Data for sign in
URL = input("auth_page: ")
login = input("Login: ")
passwd = getpass("Password: ")


# Headers for GET request
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Cookie': 'MoodleSession=1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Mobile Safari/537.36 Edg/101.0.1210.47',
    'Path': '/'
}

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='coursebox')
    courses = []
    for item in items:
        listTeachers = []
        teachers = item.find('ul', class_='teachers').findAll('li')
        for teacher in teachers:
            listTeachers.append({
                'name': teacher.find('a').get_text(),
                'link': teacher.find('a').get('href')
            })
        courses.append({
            'name': item.find('h3', class_='coursename').find('a', class_='aalink').get_text(),
            'teachers': listTeachers,
            'link': item.find('h3', class_='coursename').find('a', class_='aalink').get('href')
            })
    for i in range(0, len(courses)):
         print(courses[i])

    with open(f"{login}.json", 'w', encoding='utf-8') as f:
        json.dump(courses, f, ensure_ascii=False, indent=4)

def get_html(URL, params=None):
    session = requests.session()
    r = session.get(URL, headers=HEADERS)
    # Получаем moodleSession и передаем в заголовках POST запроса
    moodleSession = 'MoodleSession='+session.cookies['MoodleSession']
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Cookie': moodleSession,
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Mobile Safari/537.36 Edg/101.0.1210.47',
    'Path': '/'
    }
    cookie = r.cookies.get_dict()
    pattern = '<input type="hidden" name="logintoken" value="\w{32}">'
    token = re.findall(pattern, r.text)
    token = re.findall("\w{32}", token[0])
    payload = {'username': login, 'password': passwd, 'anchor': '', 'logintoken': token[0]}
    r = session.post(URL, headers=headers, cookies=cookie, data=payload)
    return r

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Error')
        return

parse()
