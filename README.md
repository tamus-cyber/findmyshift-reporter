FindMyShift Reporter 🗓️
========================

A Python tool that generates a list of employees who have not filled out their FindMyShift schedules. The tool has two components, `fms_lib.py` that contains all the necessary functions and a `main.py` that is the entry point of the program. The tool supports multiple output formats such as JSON, CSV, HTML and TXT.

Arguments
---------

Here's a rundown of the arguments you can use with FindMyShift Reporter:

- `-f` or `--format`: Specify the output format. The options are `json`, `csv`, `html` and `txt`. The default is `json`.
- `-d` or `--days`: Number of days to fetch. The default is 7 days.

Prerequisites
-------------

To use FindMyShift Reporter, you'll need to set the following environment variables:

- `API_KEY`: The API key for accessing FindMyShift.
- `TEAM_ID`: The ID of the team you want to get the report for.

Additionally, you can set the following environment variables to configure the logging:

- `LOG_LEVEL`: Logging level for the program. The default is `INFO`.

You can also put these environment variables in a `.env` file, and FindMyShift Reporter will automatically pick them up.

Output
------

The output of FindMyShift Reporter is stored in the `outputs` folder as `employees_without_shifts` with the correct file extension.

Usage
-----

To use FindMyShift Reporter, simply run the following command:

css

`python main.py`

And voila! You'll have a report of all employees who haven't filled out their FindMyShift schedules. Happy reporting! 📊

License
-------

FindMyShift Reporter is licensed under the [MIT License](LICENSE.md).
