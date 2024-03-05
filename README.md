# Deleting Jira Software Teams

## Table of Contents
* [Use Case](#use-case)
* [Setup Instructions](#setup-instructions)
* [Basic Auth](#basic-auth)
* [Credits](#credits)

## Use Case

While doing test migrations, the Jira Software teams get copied over to the Jira organization (meaning it is visible across sites). After doing a few tests, this will leave you having to manually delete hundreds or even thousands of teams. To do this programically, there's a few steps:

1. Run the Python script to GET the ids of all of the teams in a CSV file
2. Run the Node.js script to DELETE the teams

```
Note: the roadmap is to get this script onto one Python script
```

## Setup Instructions

## Instructions for Step 1

### Step 1: Download Python and Verify Installation
If you haven't installed Python yet, you can download the latest version from the official [Python website](https://www.python.org/downloads/). After installation, open a command prompt or terminal and use the following command to verify the installation: 
```
python --version
```

Alternatively, if you're using Python 3, you may need to use the 'python3' command instead of 'python': 
```python3 --version
```

This should display the installed Python version:

[pending images]

Also be sure to add Python to your path if this the first time you are using Python. [Resource](https://phoenixnap.com/kb/add-python-to-path). [Here's](https://blog.enterprisedna.co/where-is-python-installed/) how to find the python path.

Also ensure you have the requests package installed by running this:

```
$ python -m pip install requests
```


### Step 2: Download the Python Script
Ensure that you have a directory set up with the teams_export_with_members.py script.

### Step 3: Execute the Python Script
Open a command prompt or terminal, navigate to the script's directory, and run it using the following command: 

```
python teams_export_with_members.py
```

For Python 3 users: 
```
python3 teams_export_with_members.py
```

The script will sequentially request the following information:

1. Atlassian Account username. This is the email address used to log in.
2. API token. If you do not possess one, you can generate it following the instructions provided here: [Create an API token](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/#Create-an-API-token). (Note this is NOT in base64 format!)
3. Organization ID. [What it is the Organization ID and where to find it](https://confluence.atlassian.com/jirakb/what-it-is-the-organization-id-and-where-to-find-it-1207189876.html).
4. Site ID. [How to find Cloud Site Id](https://confluence.atlassian.com/jirakb/how-to-find-cloud-site-id-1272283178.html).


After entering this data, the script will fetch Teams and Team Members, generating a CSV file in the same folder where the script is executed upon completion.


## Instructions for Step 2

Here are the setup steps:

1. Ensure you have Node.js downloaded: https://nodejs.org/en 

Select the option on the left. 

To check and see if you have node already installed or if the install was successful, run the command:

~~~
node -v
~~~

2. After doing a git clone, install the necessary packages. They are already added to the package.json, so all that's needed is to run the following commmand:
~~~
npm i
~~~

3. Set up an .env file

Run the following command:
~~~
touch .env
~~~

Add 3 values to this file with the following titles:

URL = '' - this is the URL of the Atlassian Cloud site

ORG_ID = '' - this is the org id of the Atlassian Cloud org

API_KEY = '' - this is a user's PERSONAL API token in base64 format. See Basic Auth section for more details

### Note: you can use the .env.TEMPLATE file as a reference.

To use this script, run it by using the following command:

~~~
npm run start
~~~

## Basic Auth

Atlassian uses Basic Auth for a few of their REST endpoints for their authentication headers. Here are the steps to get your API token into Basic Auth format:

1. Ensure you have an API key created. Go here to create one if needed: https://id.atlassian.com/manage-profile/security/api-tokens

2. The format of basic auth is username:password then base64. The username is your email associated with your Atlassian account and then the password is the API key.

3. In the terminal run this command: (replacing user@example.com with your Atlassian account email and api_token_string with your api ke from step 1)

~~~
echo -n user@example.com:api_token_string | base64
~~~

## Credits

The Python script was created by Atlassian and its documentation can be found [here](https://confluence.atlassian.com/jirakb/exporting-atlassian-teams-and-members-data-from-my-organization-1364560115.html).

It uses [GraphQL](https://developer.atlassian.com/platform/teams/teams-graphql-api/using-team-query/) and the [teamSearchV2 query](https://developer.atlassian.com/platform/teams/graphql/#queries_teamSearchV2)

The delete team script was created by anicrob, and it uses this [REST API endpoint](https://developer.atlassian.com/platform/teams/rest/v1/api-group-teams-public-api/#api-gateway-api-public-teams-v1-org-orgid-teams-teamid-delete)

You can find more of my work at [anicrob](https://github.com/anicrob).