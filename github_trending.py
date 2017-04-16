import requests
from datetime import datetime, timedelta
import sys
from pprint import pprint


class LimitExceeded(Exception):
    def __init__(self, repo_owner, repo_name):
        url = 'https://github.com/{}/{}/issues'.format(repo_owner, repo_name)
        message = 'Лимит превышен. Открытые задачи можете посмотреть по ссылке {}'.format(url)
        super().__init__(message)

def get_trending_repositories(top_size):
    now = datetime.now()
    seven_days_ago = now - timedelta(days=7)
    date_created = seven_days_ago.strftime('%Y-%m-%d')
    params = {
        'q': 'created:>{}'.format(date_created),
        'sort': 'stars',
        'order': 'desc',
        'per_page': top_size
    }
    request = requests.get('https://api.github.com/search/repositories', params=params)
    return request.json()


def get_open_issues_amount(repo_owner, repo_name):
    request = requests.get('https://api.github.com/repos/{}/{}/issues'.format(repo_owner, repo_name))
    if request.status_code == requests.codes.ok:
        return request.json()
    raise LimitExceeded(repo_owner, repo_name)


def main():
    top_size = 20
    trending_repositories = get_trending_repositories(top_size)

    for repository in trending_repositories['items']:
        created_at = datetime.strptime(repository['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        created_at = created_at.strftime('%d.%m.%Y %H:%M:%S')
        
        print('Название: {}'.format(repository['name']))
        print('Дата создания: {}'.format(created_at))
        print('Ссылка: {}'.format(repository['html_url']))
        print('Количество форков: {}'.format(repository['forks_count']))
        print('Количество звезд: {}'.format(repository['stargazers_count']))
        print('Количество открытых задач: {}'.format(repository['open_issues_count']))

        if repository['open_issues_count']:
            try:
                issues = get_open_issues_amount(repository['owner']['login'], repository['name'])
            except LimitExceeded as error:
                print(error)
            else:
                if repository['open_issues_count'] and issues:
                    print('Список открытых задач:')
                    for issue in issues:
                        print('\tТема: {}'.format(issue['title']))        

        print()

if __name__ == '__main__':
    main()
