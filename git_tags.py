import requests
from requests.auth import HTTPBasicAuth

def get_file_commit_shas(owner, repo, file_path, username, password):
    # GitHub API endpoint for commits of a file
    url = f'https://api.github.com/repos/{owner}/{repo}/commits'

    # Headers with basic authentication
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }

    # Parameters to filter commits based on the file path
    params = {
        'path': file_path
    }

    print(f'GitHub API URL: {url}')

    # Make a GET request to the GitHub API with basic authentication
    response = requests.get(url, headers=headers, params=params, auth=HTTPBasicAuth(username, password))

    # Print the full response for debugging
    print(f'Response: {response.text}')

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        commits_info = [{'sha': commit['sha'], 'url': commit['url'], 'timestamp': commit['commit']['author']['date']} for commit in response.json()]
        return commits_info
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def get_download_url_for_commit(owner, repo, sha, username, password):
    # GitHub API endpoint for archive link (ZIP format)
    url = f'https://api.github.com/repos/{owner}/{repo}/zipball/{sha}'

    # Headers with basic authentication
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }

    # Make a GET request to the GitHub API with basic authentication
    response = requests.get(url, headers=headers, allow_redirects=False, auth=HTTPBasicAuth(username, password))

    # Check if the request was successful (status code 302 for redirect)
    if response.status_code == 302:
        download_url = response.headers.get('Location')
        return download_url
    else:
        print(f"Error fetching download URL: {response.status_code}, {response.text}")
        return None

owner = 'Vidya2000'
repo = 'testing'
file_path = "testing_1/vidya.xlsx"  # Provide the path to the specific file
username = 'Vidya2000'
password = 'Vidya@2427'

commit_info_list = get_file_commit_shas(owner, repo, file_path, username, password)

if commit_info_list:
    print(f'Commits for file "{file_path}":')
    for commit_info in commit_info_list:
        sha = commit_info['sha']
        timestamp = commit_info['timestamp']
        download_url = get_download_url_for_commit(owner, repo, sha, username, password)
        if download_url:
            print(f'Commit SHA: {sha}, Timestamp: {timestamp}, Download URL: {download_url}')
else:
    print('Failed to retrieve commits.')
