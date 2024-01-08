import requests
from requests.auth import HTTPBasicAuth
from decouple import config
import base64

def get_credentials():
    username = config('GITHUB_USERNAME')
    password = config('GITHUB_PASSWORD')
    return username, password

def encode_credentials(username, password):
    credentials = f'{username}:{password}'
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    return encoded_credentials

def get_file_commit_shas(owner, repo, file_path):
    url = f'https://api.github.com/repos/{owner}/{repo}/commits'
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }

    # Parameters to filter commits based on the file path
    params = {
        'path': file_path
    }

    # Make a GET request to the GitHub API with basic authentication
    credentials = get_credentials()
    encoded_credentials = encode_credentials(*credentials)
    auth_header = {'Authorization': f'Basic {encoded_credentials}'}
    response = requests.get(url, headers={**headers, **auth_header}, params=params)
    print(f'Response: {response.text}')

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        commits_info = [{'sha': commit['sha'], 'url': commit['url'], 'timestamp': commit['commit']['author']['date']} for commit in response.json()]
        return commits_info
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def get_download_url_for_commit(owner, repo, sha):
    url = f'https://api.github.com/repos/{owner}/{repo}/zipball/{sha}'
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }

    # Make a GET request to the GitHub API with basic authentication
    credentials = get_credentials()
    encoded_credentials = encode_credentials(*credentials)
    auth_header = {'Authorization': f'Basic {encoded_credentials}'}
    response = requests.get(url, headers={**headers, **auth_header}, allow_redirects=False)

    if response.status_code == 302:
        download_url = response.headers.get('Location')
        return download_url
    else:
        print(f"Error fetching download URL: {response.status_code}, {response.text}")
        return None

owner = 'Vidya2000'
repo = 'testing'
file_path = "testing_1/vidya.xlsx"

commit_info_list = get_file_commit_shas(owner, repo, file_path)

if commit_info_list:
    print(f'Commits for file "{file_path}":')
    for commit_info in commit_info_list:
        sha = commit_info['sha']
        timestamp = commit_info['timestamp']
        download_url = get_download_url_for_commit(owner, repo, sha)
        if download_url:
            print(f'Commit SHA: {sha}, Timestamp: {timestamp}, Download URL: {download_url}')
else:
    print('Failed to retrieve commits.')
