# RH Support Case Watcher

## Description

watcher_case is a Python script that allows you to check whether certain users and support cases are watchers on the Red Hat Customer Portal. Also allows you to add or delete users as watchers to the specified support cases.

watcher_case uses the Red Hat Support API to perform the operations mentioned above. It is important to note that the script can only work if you provide it with valid credentials/token to authenticate the calls to APIs for Red Hat services. 

See [Requirements](#requirements) and [Red Hat API References](#red-hat-api-references).

## Parameters

watcher_case accepts the following command-line parameters:

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

## Requirements

Install Python packages with pip and requirements.txt

```
pip install -r requirements.txt
```

Generate an offline token here [Red Hat API Tokens](https://access.redhat.com/management/api) to authenticate the calls to APIs for Red Hat services. It will expire after 30 days of inactivity.

```
export API_OFFLINE_TOKEN=<your_token>
```

## Examples

To show help for the subcommands:
```
watcher_case.py --help
```

To show help for the subcommands:
```
watcher_case.py list --help
```

To list users and support cases as watchers:
```
watcher_case.py list --users john.doe jane.smith --cases 123456 789012
```

To list users and support cases watchers from an input file:
```
watcher_case.py list --file list.json
```

To add users as watchers to the given support cases:
```
watcher_case.py add --users john.doe jane.smith --cases 123456 789012
```

To add users and support cases watchers from an input file:
```
watcher_case.py add --file list.json
```

To delete users as watchers from the given support cases:
```
watcher_case.py del --users john.doe jane.smith --cases 123456 789012
```

To delete users and support cases watchers from an input file:
```
watcher_case.py del --file list.json
```

## Red Hat API References

See below Red Hat API references  
 
- [Getting started with Red Hat APIs](https://access.redhat.com/articles/3626371)
- [Swagger Documentation](https://access.redhat.com/management/api/case_management)
- [Red Hat API Tokens](https://access.redhat.com/management/api)
- [Migrating scripts to use supported Customer Portal APIs](https://access.redhat.com/articles/6873281)
