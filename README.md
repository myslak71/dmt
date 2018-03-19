# dmt 
[![Build Status](https://travis-ci.org/kedod/dmt.svg?branch=master)](https://travis-ci.org/kedod/dmt)
[![Coverage Status](https://coveralls.io/repos/github/kedod/dmt/badge.svg?branch=master)](https://coveralls.io/github/kedod/dmt?branch=master&service=github)
[![Requirements Status](https://requires.io/github/kedod/dmt/requirements.svg?branch=master)](https://requires.io/github/kedod/dmt/requirements/?branch=master)
___
Log time from Toggl to Jira tasks smoothly.


### Installing

pip install https://github.com/kedod/dmt/archive/master.zip

### Example
```python
from dmt.deliver_my_time import Dmt
dmt = Dmt('toggl_token', 'https://jira_url.example', 'jira_user', 'jira_pass')
dmt.log_time_to_jira(days=30, pattern=r'task-\d+', comment=' time logged by dmt; toggle entry {}')
```
___
Code listed above will find every toggl entry, which match regex pattern, for the last 30 days. Then log every entry to corresponding Jira ticket (e.g https://jira_url.example/task-1) and mark toggl entry as 'logged' to prevent log it in the future.
 
### Auto log
You can use crontab for Linux or Task Scheduler for Windows to run python script with every computer boot.
 

### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details



