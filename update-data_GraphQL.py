import requests
import json

githubToken = ""
hideRepos = { "WhatsMyDistrict", "StickTron" }


query = """
{
  repositoryOwner(login: "ScholliYT") {
    repositories(last: 100) {
      totalCount
      edges {
        node {
          name
          closedIssueCount: issues(states: CLOSED) {
            totalCount
          }
          totalIssueCount: issues {
            totalCount
          }
        }
      }
    }
  }
}
"""

headers = { 'Content-Type': 'application/json', 'Authorization': 'bearer ' + githubToken }
payload = { 'query': query}
r = requests.post("https://api.github.com/graphql", data=json.dumps(payload), headers=headers)
data = r.json()
repos = data["data"]["repositoryOwner"]["repositories"]["edges"]
reposCount = data["data"]["repositoryOwner"]["repositories"]["totalCount"]

if len(repos) != reposCount:
    print("Recieved invalid Data while parsing repositories!")
    raise SystemExit

for repo in repos:
    repo = repo["node"]
    if repo["name"] in hideRepos:
        print("Skipping repository " + repo["name"])
        continue
    print( "Reading repository ==============================> " + repo["name"]);
    print(repo)


