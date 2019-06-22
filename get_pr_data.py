import csv
import requests

"""
Pulls all PR's submitted to CenterForOpenScience.osf.io and returns a CSV of
their titles, authors, and date created

See Github v3 dev docs:
https://developer.github.com/v3/pulls/#list-pull-requests

Unauthenticated rate limit - 60 requests/hr
Authenticate to get 5000 requests
"""

BASE_PULL_URL = 'https://api.github.com/repos/CenterForOpenScience/osf.io/pulls?state=all'
pr_data = []

def get_pull_requests(url):
    resp = requests.get(url)
    data = resp.json()
    for pr in data:
        pr_data.append([
            pr['title'].encode('utf-8'),
            pr['created_at'],
            pr['user']['login']
        ])
    next = resp.links.get('next')
    print next
    if next:
        url = next['url']
        return get_pull_requests(url)

def write_pr_data_to_csv(data):
    with open('output.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows([['title', 'author', 'created']])
        writer.writerows(data)
    return

def main():
    get_pull_requests(BASE_PULL_URL)
    write_pr_data_to_csv(pr_data)


if __name__ == "__main__":
    main()
