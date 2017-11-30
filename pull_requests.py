import requests
import argparse

from urllib import parse # for parsing pagination
from IPython import embed # for interactive exploration

parser = argparse.ArgumentParser()
parser.add_argument("-token", required=True, help="Github Account Token Required for Authentication")
parser.add_argument("-org", required=True, help="Organization to count pull requests")
args = parser.parse_args()

headers = headers = {"Authorization": "Bearer %s" % args.token}

# first, get list of org's repos, and make sure auth works
r = requests.get('https://api.github.com/orgs/%s/repos' % args.org, headers=headers)

if r.status_code != 200:
    if r.status_code == 403 or r.status_code == 401:
        print("Couldn't authenticate with Github. Check your authorization token.")
        print(r.content)
        exit()
    elif r.status_code == 404:
        print("Are you sure that organization exists? Github couldn't find it.")
        print(r.content)
        exit()
    else:
        print("Couldn't connect to API.")
        print(r.status_code)
        print(r.json())
        exit()

repositories = r.json()
print("Found %i repositories for %s organization" % (len(repositories), args.org))

pull_requests = {"total_prs": 0}

# Loop over each repo for org
for repo in repositories:
    r = requests.get("https://api.github.com/repos/%s/%s/pulls?state=all&per_page=100"
                     % (args.org, repo["name"]), headers=headers)

    # If we need to paginate
    if 'link' in r.headers:
        current_page = 1
        total_pages = int(parse.parse_qs(r.links['last']['url'])['page'][0]) # gets the page no from url
        pull_requests[repo["name"]] = []

        while 'next' in r.links:
            print("In page %i of %i, there are %i pull requests" % (current_page, total_pages, len(r.json())))
            pull_requests[repo["name"]].extend(r.json())
            r = requests.get(r.links['next']['url'], headers=headers)
            current_page += 1
        print("In page  %i of %i, there are %i pull requests" % (current_page, total_pages, len(r.json())))

        pull_requests[repo["name"]].extend(r.json())
        pull_requests['total_prs'] += len(pull_requests[repo["name"]])
        print("There are %i total pull requests for %s" % (len(pull_requests[repo["name"]]), repo["name"]))
    # we don't need to paginate
    else:
        number_open = len(r.json())
        print("In %s, there are %i pull requests" % (repo["name"], number_open))
        pull_requests[repo["name"]] = r.json()
        pull_requests['total_prs'] += number_open

# pull_requests is now a dictionary with all pull requests
print("There are %i total pull requests" % pull_requests["total_prs"])
embed()
