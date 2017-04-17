import requests
from datetime import datetime, timedelta


def get_trending_repositories(top_size, days):
    now = datetime.now()
    timedelta_days = now - timedelta(days=days)
    date_created = timedelta_days.strftime('%Y-%m-%d')
    params = {
        'q': 'created:>{}'.format(date_created),
        'sort': 'stars',
        'order': 'desc',
        'per_page': top_size
    }
    request = requests.get('https://api.github.com/search/repositories', params=params)
    return request.json()


def get_list_issues(repo_owner, repo_name):
    request = requests.get('https://api.github.com/repos/{}/{}/issues'.format(repo_owner, repo_name))
    if request.status_code == requests.codes.ok:
        return request.json()
    url = 'https://github.com/{}/{}/issues'.format(repo_owner, repo_name)
    error = [{'title': 'Лимит превышен. Открытые задачи можете посмотреть по ссылке {}'.format(url)}]
    return error



def print_trending_repository(repository):
    created_at = datetime.strptime(repository['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    created_at = created_at.strftime('%d.%m.%Y %H:%M:%S')
    
    print('Название: {}'.format(repository['name']))
    print('Дата создания: {}'.format(created_at))
    print('Ссылка: {}'.format(repository['html_url']))
    print('Количество форков: {}'.format(repository['forks_count']))
    print('Количество звезд: {}'.format(repository['stargazers_count']))
    print('Количество открытых задач: {}'.format(repository['open_issues_count']))

def print_list_issues(repository, issues):
    if repository['open_issues_count'] and issues:
        print('Список открытых задач:')
        for issue in issues:
            print('\tТема: {}'.format(issue['title']))    




def main():
    top_size = 20
    days = 7
    trending_repositories = get_trending_repositories(top_size, days)

    for repository in trending_repositories['items']:        
        if repository['open_issues_count']:
            issues = get_list_issues(repository['owner']['login'], repository['name'])
            print_list_issues(repository, issues)
            print()

if __name__ == '__main__':
    main()
