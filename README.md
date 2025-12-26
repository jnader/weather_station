# Weather station

This is a simple weather station which uses:
- IP API to get geolocation from IP address.
- Open Weather API to retrieve weather forecasts, nowcasts and history.

## Requirements

- Install python dependencies:
```
pip3 install -r requirements.txt
```

- Create `keys.yaml` file with this template:
```
open_weather_api_key: <OPEN_WEATHER_API_KEY>
```
and fill it with your own API keys.

## Test

- You can run `weather_station.py` test example:
```
python3 test_weather_station.py
```