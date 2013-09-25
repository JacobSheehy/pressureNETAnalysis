Introduction
============
We recommend that you set up a recurring task on a server to access our live stream. With the flexibility we provide in this API there are many methods you can use to establish the data stream on your end. Here’s a simple python script that will make an API call and print the results to the screen. This can be modified to run in a cron job and save the output to a file or database.

Examples
________

Example python code to make an API call and print results::

    import urllib2
    data = urllib2.urlopen('https://pressurenet.cumulonimbus.ca/live/?global=true&since_last_call=true&format=json&api_key=APIKEY')
    content = data.read()
    print content

For the API calls themselves, we provide four general use cases and example calls.


Use Case 1: Total user control in a region
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Supply detailed parameters without using dynamic features such as since_last_call or global. Latitude and longitude bounds are specified and long with start and end times.

Example API call::

    https://pressurenet.cumulonimbus.ca/live/?min_lat=44.77865108875515&max_lat=47.77865108875515&min_lon=-74.93251647949216&max_lon=-70.93251647949216&start_time=1351396800000&end_time=1359694800000&format=json&api_key=testkey


Use Case 2: Recent measurements in a region
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

User sets since_last_call=true and does not specify global. Latitude and longitude bounds are set but start and end times are not.

Example API call::

    https://pressurenet.cumulonimbus.ca/live/?since_last_call=true&min_lat=44.77865108875515&max_lat=47.77865108875515&min_lon=-74.93251647949216&max_lon=-70.93251647949216&format=json&api_key=testkey


Use Case 3: Recent global measurements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

User passes global=true and since_last_call=true. No location or time parameters are passed.

Example API call::

    https://pressurenet.cumulonimbus.ca/live/?since_last_call=true&global=true&format=json&api_key=testkey


Use Case 4: Time-specified global measurements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
User passes global=true but not since_last_call. No location parameters are passed but start and end times are required.

Example API call::

    https://pressurenet.cumulonimbus.ca/live/?global=true&start_time=1351396800000&end_time=1359694800000&format=json&api_key=testkey
