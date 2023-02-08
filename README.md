FindMyShift Reporter 🗓️
========================

A Python tool that generates a list of employees who have not filled out their FindMyShift schedules. The tool has two components, `fms_lib.py` that contains all the necessary functions and a `main.py` that is the entry point of the program. The tool supports multiple output formats such as JSON, CSV, HTML and TXT. Additionally, the tool can send a Slack alert if there are employees who haven't filled out their schedules.

Arguments
---------

Here's a rundown of the arguments you can use with FindMyShift Reporter:

- `-f` or `--format`: Specify the output format. The options are `json`, `csv`, `html` and `txt`. The default is `json`.
- `-d` or `--days`: Number of days to fetch. The default is 7 days.
- `-a` or `--all`: Fetch all employees, including those who have filled out their schedules. The default is `False`.
- `-s` or `--slack`: Send a Slack alert if there are employees who haven't filled out their schedules. The default is `False`.

Prerequisites
-------------

To use FindMyShift Reporter, you'll need to set the following environment variables:

- `API_KEY`: The API key for accessing FindMyShift.
- `TEAM_ID`: The ID of the team you want to get the report for.

Additionally, you can set the following environment variables to configure the logging:

- `LOG_LEVEL`: Logging level for the program. The default is `INFO`.

If you opt to use Slack alerting, you'll need to set the following environment variables:

- `SLACK_CHANNEL`: The Slack channel to send the alert to.
- `SLACK_TOKEN`: The Slack token to use for sending the alert.
- `SLACK_USERNAME`(optional): The Slack username to use for sending the alert.
- `SLACK_ICON_EMOJI`(optional): The Slack icon emoji to use for sending the alert.

You can also put these environment variables in a `.env` file, and FindMyShift Reporter will automatically pick them up.

Settings
--------

FindMyShift Reporter has a few settings that you can configure in `settings.json`:

```json
{
    "blacklist": [
        # Blacklist of staff IDs to ignore
        "staffIDXXXX",
        "staffIDXXXX",
        ...
    ]
    "aliases": {
        # Aliases for staff IDs
        "staffIDXXXX": "John Doe",
        "staffIDXXXX": "Jane Doe",
        ...
    }
}
```

Output
------

The output of FindMyShift Reporter is stored in the `outputs` folder as `employees_without_shifts` with the correct file extension. If you used the `-a` or `--all` argument, the output will be stored in the `outputs` folder as `all_employees` with the correct file extension.

Usage
-----

To use FindMyShift Reporter, clone the repository and navigate to the directory.

```bash
git clone https://github.com/tamus-cyber/findmyshift-reporter.git
cd findmyshift-reporter
```

Then, simply run the following command:

`python3 main.py`

And voila! You'll have a report of all employees who haven't filled out their FindMyShift schedules. Happy reporting! 📊

Testing
-------

To keep environment clean during testing, there is a `docker-compose.yml` file that will create a container with all the necessary dependencies. To run the tests, simply run the following command:

```bash
docker-compose --env-file .env up && docker-compose rm -fsv
```

License
-------

FindMyShift Reporter is licensed under the [MIT License](LICENSE.md).
