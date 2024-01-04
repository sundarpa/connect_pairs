import requests


def get_commit_info(owner, repo, sha, token):
    # GitHub API endpoint for commit details
    url = f'https://api.github.com/repos/{owner}/{repo}/commits/{sha}'

    # Headers with the personal access token for authentication
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Make a GET request to the GitHub API
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        commit_info = response.json()
        commit_date = commit_info.get('commit', {}).get('author', {}).get('date', 'N/A')
        return commit_date
    else:
        print(f"Error fetching commit info: {response.status_code}, {response.text}")
        return 'N/A'


def get_github_tags(owner, repo, directory, token):
    # GitHub API endpoint for tags
    url = f'https://api.github.com/repos/{owner}/{repo}/tags'

    # Headers with the personal access token for authentication
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Parameters to filter tags based on directory
    params = {
        'path': directory
    }

    print(f'GitHub API URL: {url}')

    # Make a GET request to the GitHub API
    response = requests.get(url, headers=headers, params=params)

    # Print the full response for debugging
    print(f'Response: {response.text}')

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        tags_info = []
        for tag in response.json():
            tag_name = tag['name']
            sha = tag['commit']['sha']
            tag_date = get_commit_info(owner, repo, sha, token)

            tags_info.append({
                'name': tag_name,
                'date': tag_date,

            })

        return tags_info
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


owner = 'Vidya2000'
repo = 'SearchTool'
directory = "tool_installer"
token = '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'

tags_info = get_github_tags(owner, repo, directory, token)

if tags_info:
    print(f'Tags in directory "{directory}":')
    for tag in tags_info:
        print(f'Tag: {tag["name"]}, Created at: {tag["date"]}')
else:
    print('Failed to retrieve tags.')
