'''created by fwk
   2017/10/31
   get commit from https://api.github.com/'''
import requests
import json
from redis import Redis


def get_data(project_url):
    '''
    repository_API = "https://api.github.com/repositories?since=1"
    repository_json = requests.get(repository_API, timeout=30).json()
    
    f = open('./github.json', 'w')
    f.write(json.dumps(repository_json).replace(', ', ',\n'))
    f.close()
    '''

    # example: https://github.com/wycats/merb-core convert to https://api.github.com/repos/wycats/merb-core/commits
    url_prefix = 'https://api.github.com/repos/'
    commit_url = url_prefix + project_url[19:] + '/commits'
    token = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
             'Authorization': 'token ' + 'e3572f2f2cf0e8075fd3dea841050257063809d5'}
    commit_json = requests.get(commit_url, headers=token, timeout=30).json()
    print 'Project name: ' + project_url[19:]

    for item in commit_json:
        if isinstance(item, dict) and isinstance(item['commit'], dict) and isinstance(item['commit']['committer'],dict):
            info = 'committer_name: ' + item['commit']['committer']['name'] + '/ ' +\
                'commit_date: ' + item['commit']['committer']['date']  + '/ ' +\
                'message: ' + item['commit']['message'].replace('\n', '')
            print info


if __name__ == '__main__':
    get_data('https://github.com/wycats/merb-core')
