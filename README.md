# RH Support Case Watcher

## Description

Watcher is a Python script that allows you to check whether certain users and support cases are watchers on the Red Hat Customer Portal. The script also allows you to add or delete users as watchers to the specified support cases.

Watcher uses the Red Hat Support API to perform the operations mentioned above. It is important to note that the script can only work if you provide it with valid credentials.

## Parameters

Watcher (wtc) accepts the following command-line parameters:

 Subcommands | Description | 
| ---------- |  ---------- | 
| help  | Show help for subcommands  |
|list| List the given users and support cases as watchers|
|add|Add the given users as watchers to the given support cases|
|del|Delete the given users as watchers to the given support cases|

Options:

`--users` or `-u`: List of user IDs

`--cases` or `-c`: List of case IDs

`-f` or `--filename`: Name of the input file with user and case IDs.

JSON file example:

```
{
  "users": ["user1", "user2"],
  "cases": ["case1", "case2"]
}
``` 

## Examples

Get offline token from https://access.redhat.com/management/api and export as follows:
```
export API_OFFLINE_TOKEN=<your_token>
```

To show help for the subcommands:
```
watcher.py help
```

To list users and support cases as watchers:
```
watcher.py list --users john.doe jane.smith --cases 123456 789012
```

To list users and support cases watchers from an input file:
```
watcher.py list --file list.json
```


To add users as watchers to the given support cases:
```
watcher.py add --users john.doe jane.smith --cases 123456 789012
```

To delete users as watchers from the given support cases:
```
watcher.py del --users john.doe jane.smith --cases 123456 789012
```
