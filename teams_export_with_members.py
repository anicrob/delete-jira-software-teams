# ==UserScript==
# @name         Get Jira site Teams
# @version      1.0.0
# @description  Get all the teams in a Jira site
# @author       Ariel Mira Franco (from Atlassian)
# ==/UserScript==

import requests
import csv
import time
from datetime import datetime

# Function to make HTTP requests
def make_request(email, token, instance_name, org_id, site_id, after=""):
    url = f"https://{instance_name}.atlassian.net/gateway/api/graphql?q=teamSearchV2"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    data = {
        "operationName": "teamSearchV2",
        "variables": {
            "query": "",
            "memberIds": [],
            "first": 24,
            "organizationId": f"ari:cloud:platform::org/{org_id}",
            "sortBy": [{"field": "DISPLAY_NAME", "order": "ASC"}],
            "siteId": site_id,
        },
        "query": "query teamSearchV2($first: Int, $after: String, $organizationId: ID!, $query: String = \"\", $memberIds: [ID] = [], $sortBy: [TeamSort], $siteId: String!) {\n  team {\n    teamSearch: teamSearchV2(first: $first, after: $after, organizationId: $organizationId, filter: {query: $query, membership: {memberIds: $memberIds}}, sortBy: $sortBy, siteId: $siteId) @optIn(to: [\"Team-search-v2\"]) {\n      nodes {\n        ...TeamNodeV2\n        __typename\n      }\n      pageInfo {\n        hasNextPage\n        endCursor\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment TeamNodeV2 on TeamSearchResultV2 {\n  team {\n    id\n    organizationId\n    membershipSettings\n    description\n    displayName\n    state\n    largeAvatarImageUrl\n    smallAvatarImageUrl\n    largeHeaderImageUrl\n    smallHeaderImageUrl\n    members {\n      nodes {\n        member {\n          id\n          accountStatus\n          name\n          picture\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  memberCount\n  includesYou\n  __typename\n}\n",
    }

    if after:
        data["variables"]["after"] = after

    response = requests.post(
        url, headers=headers, json=data, auth=(email, token)
    )
    return response.json()

# Function to handle paginated responses
def get_teams(email, token, instance_name, org_id, site_id):
    all_teams = []
    after = ""
    print("Export in progress. Please be patient as this operation will take approximately 1 minute for every 500 Teams in your instance...")
    while True:
        response = make_request(email, token, instance_name, org_id, site_id, after)

        # Check for rate limit error in the response
        if response.get("status") == 429:
            print("Rate limit hit, waiting for 1 minute 15 seconds before retrying...")
            time.sleep(75) # 1 minute and 15 seconds
            continue # re-try the same request

        # Check for errors in the response
        if "errors" in response:
            error_message = response["errors"][0]["message"]
            print(f"Error in request: \n{error_message}")
            return []

        if "data" not in response:
            print("Failure: Request failed with error:")
            print(response)
            return []

        teams = response["data"]["team"]["teamSearch"]["nodes"]
        all_teams.extend(teams)

        if not response["data"]["team"]["teamSearch"]["pageInfo"]["hasNextPage"]:
            break

        after = response["data"]["team"]["teamSearch"]["pageInfo"]["endCursor"]
        time.sleep(3)  # To prevent exceeding the rate limit

    return all_teams

# Function to write data to CSV file
def write_to_csv(teams):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"Teams-{timestamp}.csv"

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "id",
            "displayName",
            "description",
            "state",
            "organizationId",
            "membershipSettings",
            "memberCount",
            "members",
            "largeAvatarImageUrl",
            "smallAvatarImageUrl",
            "largeHeaderImageUrl",
            "smallHeaderImageUrl"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for team in teams:
            team_data = team["team"]
            row_data = {
                "id": team_data.get("id", "").replace("ari:cloud:identity::team/", ""),
                "displayName": team_data.get("displayName", ""),
                "description": team_data.get("description", ""),
                "state": team_data.get("state", ""),
                "organizationId": team_data.get("organizationId", "").replace("ari:cloud:platform::org/", ""),
                "membershipSettings": team_data.get("membershipSettings", ""),
                "memberCount": team.get("memberCount", ""),
                "largeAvatarImageUrl": team_data.get("largeAvatarImageUrl", ""),
                "smallAvatarImageUrl": team_data.get("smallAvatarImageUrl", ""),
                "largeHeaderImageUrl": team_data.get("largeHeaderImageUrl", ""),
                "smallHeaderImageUrl": team_data.get("smallHeaderImageUrl", ""),
            }

            # Extract member information
            members = team_data.get("members", {}).get("nodes", [])
            member_data_list = [{"id": member["member"]["id"].replace("ari:cloud:identity::user/", ""), "name": member["member"]["name"]} for member in members]
            row_data["members"] = member_data_list

            writer.writerow(row_data)

    print(f"CSV file '{filename}' created successfully!")

# User input
user_email = input("User Email: ")
user_token = input("User Token: ")
org_id = input("Org ID: ")
site_id = input("Site ID: ")

# Currently, the instance name isn't mandatory as the org ID and site ID are crucial. In case of failure, removing the hardcoded instance_name below and using the commented line for user input will resolve the problem.
instance_name = "atlassian"
#instance_name = input("Instance Name: ")

# Fetching teams
teams_data = get_teams(user_email, user_token, instance_name, org_id, site_id)

# Writing data to CSV
if teams_data:
    write_to_csv(teams_data)
else:
    print("CSV file generation unsuccessful. Please check your input and try running the script again.")