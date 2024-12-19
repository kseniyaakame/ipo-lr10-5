import requests
from bs4 import BeautifulSoup
import json

# URL страницы с популярными репозиториями
url = 'https://github.com/trending'

# Получаем HTML-код страницы
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Находим все репозитории
repositories = soup.find_all('article', class_='Box-row')

# Список для хранения данных
popular_repos = []

for index, repo in enumerate(repositories[:5], start=1):  # Добавляем индекс
    repo_name_tag = repo.find('h2', class_='h3 lh-condensed')
    if repo_name_tag:
        repo_name = repo_name_tag.text.strip().replace('\n', ' ').strip()
    else:
        continue

    # Получаем ссылку на репозиторий
    repo_link = 'https://github.com' + repo_name_tag.find('a')['href'] if repo_name_tag.find('a') else 'N/A'

    stars_tag = None
    links = repo.find_all('a')
    for link in links:
        if link.get('href') and '/stargazers' in link.get('href'):
            stars_tag = link
            break

    stars = stars_tag.text.strip() if stars_tag else '0'
    popular_repos.append({
        'rank': index,  # Добавляем ранг
        'repository': repo_name,
        'stars': stars,
        'link': repo_link  # Добавляем ссылку на репозиторий
    })

# Выводим данные на экран
index = 1
for repo in popular_repos:
    print(f"{index}. Repository: {repo['repository']}; Stars: {repo['stars']};")
    index += 1


# Сохраняем данные в файл data.json
with open('data.json', 'w') as json_file:
    json.dump(popular_repos, json_file, indent=4)


# Читаем данные из файла data.json
with open('data.json', 'r') as json_file:
    data = json.load(json_file)

# Генерируем HTML-страницу
html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trending GitHub Repositories</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #f0f0f0, #e0e0e0);
            margin: 0;
            padding: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:hover {
            background-color: #f1f1f1;
        }
    </style>
</head>
<body>
    <h1>Trending GitHub Repositories</h1>
    <table>
        <tr>
            <th>Rank</th>
            <th>Repository</th>
            <th>Stars</th>
        </tr>
'''

# Добавляем данные в таблицу
for item in data:
    html_content += f'''
        <tr>
            <td>{item['rank']}</td>
            <td><a href="{item['link']}" target="_blank">{item['repository']}</a></td>
            <td>{item['stars']}</td>
        </tr>
    '''

# Закрываем таблицу и добавляем ссылку на источник
html_content += '''
    </table>
    <p>Source: <a href="https://github.com/trending" target="_blank">GitHub Trending</a></p>
</body>
</html>
'''

# Сохраняем HTML-код в файл index.html
with open('index.html', 'w') as html_file:
    html_file.write(html_content)