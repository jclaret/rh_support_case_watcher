# Examples
#   export API_OFFLINE_TOKEN=<your_token> # Get your token https://access.redhat.com/management/api
#   python watcher.py list --users rhn-support-jclaretm --case 03112577
#   python watcher.py add --users rhn-support-jclaretm --case 03112577
#   python watcher.py del --users rhn-support-jclaretm --case 03112577
#
import os
import requests
import json
import argparse
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

# Read environment variables for URL and TOKEN
API_URL = os.getenv('REDHAT_API_URL', default="https://api.access.redhat.com/support")
API_TOKEN = os.getenv('REDHAT_API_TOKEN')

# Define subcommands and arguments using argparse
parser = argparse.ArgumentParser(description='Script to check if given users and support cases are watchers on the Red Hat Customer Portal.')
subparsers = parser.add_subparsers(dest='subcommand', required=True)

# Help subcommand
help_parser = subparsers.add_parser('help', help='Show help for subcommands')
help_parser.add_argument('command', nargs='?', help='Subcommand to show help for')

# List subcommand
list_parser = subparsers.add_parser('list', help='List the given users and support cases as watchers')
list_parser.add_argument('--users', '-u', required=True, nargs='+', help='List of user IDs to check')
list_parser.add_argument('--cases', '-c', required=True, nargs='+', help='List of case IDs to check')

# Add subcommand
add_parser = subparsers.add_parser('add', help='Add the given users as watchers to the given support cases')
add_parser.add_argument('--users', '-u', required=True, nargs='+', help='List of user IDs to add as watchers')
add_parser.add_argument('--cases', '-c', required=True, nargs='+', help='List of case IDs to add the users as watchers to')

# Del subcommand
add_parser = subparsers.add_parser('del', help='Del the given users as watchers to the given support cases')
add_parser.add_argument('--users', '-u', required=True, nargs='+', help='List of user IDs to delete as watchers')
add_parser.add_argument('--cases', '-c', required=True, nargs='+', help='List of case IDs to delete the users as watchers to')


# Define functions for each subcommand
def show_help(args):
    if args.command:
        parser.print_help(subcommand=args.command)
    else:
        parser.print_help()

def refresh_access_token():
    # Define the application credentials
    CLIENT_ID = "rhsm-api"
    REFRESH_TOKEN = os.environ.get('API_OFFLINE_TOKEN')

    # Define the authorization URL
    AUTH_URL = "https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "refresh_token": REFRESH_TOKEN
    }
    response = requests.post(AUTH_URL, headers=headers, data=data)
    if response.status_code == 200:
        global API_TOKEN
        API_TOKEN = json.loads(response.text)['access_token']  # access token that is valid for five minutes
        print("[INFO] Refreshed access token.")
    else:
        print("[FAIL] Failed to refresh access token: %s" % response.text)

def list_watchers(args):
    # Define headers and params for API request
    headers = {'Authorization': 'Bearer ' + API_TOKEN}
    refresh_access_token

    # Loop through each user and case ID and check if they are watchers
    for user_id in args.users:
        for case_id in args.cases:
            # Make API request to get case details
            response = requests.get(API_URL + '/v1/cases/' + case_id, headers=headers)
            # Check if request was successful
            if response.status_code == requests.codes.ok:
                if 'notifiedUsers' in json.loads(response.text):
                    case_data = json.loads(response.text)['notifiedUsers']
                    # Extract the ssoUsername values
                    sso_usernames = [user["ssoUsername"] for user in case_data]
                    # Check if user ID is a watcher
                    if user_id in sso_usernames:
                        print(Fore.GREEN + f'User {user_id} is a watcher on case {case_id}')
                    else:
                        print(Fore.RED + f'User {user_id} is not a watcher on case {case_id}')
                else:
                    print(Fore.RED + f'User {user_id} is not a watcher on case {case_id}')
            else:
                print(Fore.YELLOW + f'Error checking case {case_id}: {response.text}')

def add_watchers(args):
    # Define headers for API requests
    headers = {'Authorization': 'Bearer ' + API_TOKEN}

    # Loop through each user and case ID and add the user as a watcher to the case
    for user_id in args.users:
        for case_id in args.cases:
            # Make API request to update case details
            response = requests.post(API_URL + '/v1/cases/' + case_id + '/notifiedusers', headers=headers, json={"user":[{"ssoUsername": user_id}]})
            if response.status_code == requests.codes.ok or response.status_code == requests.codes.created:
                print(Fore.GREEN + f'User {user_id} added as a watcher to case {case_id}')
            else:
                print(Fore.YELLOW + f'Error adding user {user_id} as a watcher to case {case_id}: {response.text}')

def del_watchers(args):
    # Define headers for API requests
    headers = {'Authorization': 'Bearer ' + API_TOKEN}

    # Loop through each user and case ID and del the user as a watcher to the case
    for user_id in args.users:
        for case_id in args.cases:
            # Make API request to update case details
            response = requests.delete(API_URL + '/v1/cases/' + case_id + '/notifiedusers/' + user_id, headers=headers)
            if response.status_code == requests.codes.ok:
                print(Fore.GREEN + f'User {user_id} deleted as a watcher to case {case_id}')
            else:
                print(Fore.YELLOW + f'Error deleting user {user_id} as a watcher to case {case_id}: {response.text}')

# Define main function
def main():
    refresh_access_token()  # Call the function to refresh the access token
    args = parser.parse_args()
    if args.subcommand == 'help':
        show_help(args)
    elif args.subcommand == 'list':
        list_watchers(args)
    elif args.subcommand == 'add':
        add_watchers(args)
    elif args.subcommand == 'del':
        del_watchers(args)

if __name__ == '__main__':
    main()
