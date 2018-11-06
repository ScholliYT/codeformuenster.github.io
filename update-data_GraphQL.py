import requests
import json

githubToken = ""
githubOrganization = "codeformuenster"
hideRepos = { "WhatsMyDistrict" }

def getRepos(cursor, repoarray):
  query = """
  {
    organization(login: \"""" + githubOrganization + """\") {
      repositories(first: 100, after: \"""" + cursor + """\") {
        totalCount
        edges {
          cursor
          node {
            createdAt
            updatedAt
            url
            name
            description
            homepageUrl
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
  repos = data["data"]["organization"]["repositories"]["edges"]
  reposCount = data["data"]["organization"]["repositories"]["totalCount"]

  #if len(repos) != reposCount:
  #    print("Recieved invalid Data while parsing repositories!")
  #    raise SystemExit
  cursor = ""
  for repo in repos:
      cursor = repo["cursor"]
      repo = repo["node"]
      if repo["name"] in hideRepos:
          print("Skipping repository " + repo["name"])
          continue
      print( "Reading repository ==============================> " + repo["name"]);
      repoarray.append({
        "updated_at": repo["updatedAt"],
        "created_at": repo["createdAt"],
        "description": repo["description"],
        "name": repo["name"],
        "total_tasks": repo["totalIssueCount"]["totalCount"],
        "closed_tasks": repo["closedIssueCount"]["totalCount"],
        "html_url": repo["url"],
        "url": repo["homepageUrl"]
        })
  return cursor



"""
{
  repositoryOwner(login: "ScholliYT") {
    repositories(last: 100) {
      totalCount
      edges {
        node {
          createdAt
          updatedAt
          url
          name
          description
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

print("Fetching all repositories from " + githubOrganization)

repodata = []
lastCursor = getRepos("", repodata)
while lastCursor != "":
  lastCursor = getRepos(lastCursor, repodata)

print("Finished fetching data from GitHub.")

with open('json/pythonTest.json', 'w') as outfile:
    json.dump(repodata, outfile, indent=4)


