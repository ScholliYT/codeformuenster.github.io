import requests
import json
import sys

githubToken = ""
githubOrganization = "codeformuenster"
hideRepos = { "WhatsMyDistrict" }
repoJSONOutputFile = "repos.json"
userJSONOutputFile = "members.json"

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
        "html_url": repo["homepageUrl"],
        "url": repo["url"]
        })
  return cursor

def getUsers(userarray):
  query = """
  {
    organization(login: \"""" + githubOrganization + """\") {
      members(first: 100) {
        totalCount
        edges {
          cursor
          node {
            avatarUrl
            login
            url
            name
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
  users = data["data"]["organization"]["members"]["edges"]

  for user in users:
      user = user["node"]
      print( "Reading user ==============================> " + user["name"]);
      userarray.append({
        "avatarUrl": user["avatarUrl"],
        "login": user["login"],
        "html_url": user["url"],
        "name": user["name"]
        })

if(githubToken == "") :
  print("No Token!")
  sys.exit()

# Repos
print("Fetching all repositories from " + githubOrganization)

repodata = []
lastCursor = getRepos("", repodata)
while lastCursor != "":
  lastCursor = getRepos(lastCursor, repodata)

print("Finished fetching data from GitHub.")

print("Writing data to "+ repoJSONOutputFile + " file...")
with open('json/' + repoJSONOutputFile, 'w') as outfile:
    json.dump(repodata, outfile, indent=4)
print("Finished writing data to "+ repoJSONOutputFile +" file.")


# Users
print("Fetching all users from " + githubOrganization)

userdata = []
getUsers(userdata)

print("Finished fetching data from GitHub.")

print("Writing data to " + userJSONOutputFile + " file...")
with open('json/' + userJSONOutputFile, 'w') as outfile:
    json.dump(userdata, outfile, indent=4)
print("Finished writing data to " + userJSONOutputFile + " file.")