API Reference
=========

Requests
________

HTTPS requests are sent to `https://pressurenet.cumulonimbus.ca/live/` with the following parameters and options. 

Time values are represented as the number of milliseconds since 00:00:00 Coordinated Universal Time (UTC), 1 January 1970 (Unix epoch).

**api_key** `key`
    Your pressureNET Live API key. Required to authenticate your account.

**format** `response_format`
    Specify the format in which the response will be returned. May be `json` (the default) or `xml`.

**limit** `n`
    Limit the number of results returned. Must be less than `10000`.

**since_last_call** `bool`
    If `true`, the data since the end time of the your last call to the pressureNET Live API is returned (`start_time` and `end_time` will be ignored). If you haven’t made any calls yet, `since_last_call` should be set to false and `start_time` and `end_time` should be used. Defaults to `false` (`start_time` and `end_time` required).

**start_time** `time`
    The starting time with which to filter the response data, in ms since Unix epoch.

**end_time** `time`
    The end time with which to filter the response data, in ms since Unix epoch.

**global** `bool`
    If `true`, data from everywhere in the world is returned (`min_lat`, `max_lat`, `min_lon`, and `max_lon` will be ignored). Defaults to `false` (`min_lat`, `max_lat`, `min_lon`, and `max_lon` required). 

**min_lat** `lat`
    The minimum latitude with which to filter the response data. Must be between `-90` and `90`.

**max_lat** `lat`
    The maximum latitude with which to filter the response data. Must be between `-90` and `90`.

**min_lon** `lon`
    The minimum longitude with which to filter the response data. Must be between `-180` and `180`.

**max_lon** `lon`
    The maximum longitude with which to filter the response data. Must be between `-180` and `180`.


Responses
_________

The server will respond with a list of objects, each of which describe a measurement that was taken by a user of pressureNET. Each response object has the following fields:

**user_id**

    Unique ID of the user

**latitude**

    Latitude of measurement

**longitude**

    Longitude of measurement

**location_accuracy**

    Accuracy/confidence level for location data

**date_recorded**

    Time of measurement (milliseconds since Unix epoch)

**tzoffset**

    User’s timezone

**measurement**

    Atmospheric pressure in millibars

**reading_accuracy**

    Atmospheric pressure in millibars

**sharing**

    Sharing privacy level (see sharing levels)

**client_key**

    Unique ID of the data source client application

**observation_type**

    ‘reading’ could be pressure, temperature or humidity

**observation_unit**

    Unit of ‘reading’

**provider**

    Location type: GPS, network
