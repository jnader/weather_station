"""
Typical weather station test program.
To run this script, you should be connected to the internet.
"""

import logging
import requests
import weather_station as ws
import yaml

logger = logging.getLogger()
logging.basicConfig(filename="/tmp/myapp.log", level=logging.INFO, filemode="w")

current_location_request = "http://ip-api.com/json?fields=lat,lon"


def main():
    logger.info("Gettting latitude/longitude from IP address...")
    try:
        r = requests.get(current_location_request)
        if r.status_code != 200:
            logger.error("Couldn't retrieved position from IP...")
            logger.error("Exiting...")
            exit(1)

        latitude, longitude = r.json().values()
        logger.info(f"Found! Latitude: {latitude}, Longitude: {longitude}")

        logger.info("Creating weather station")
        station = ws.WeatherStation(latitude=latitude, longitude=longitude, logger=logger)

        with open("keys.yaml", "r") as f:
            keys = yaml.load(f, yaml.FullLoader)
            station.set_open_weather_api_key(keys["open_weather_api_key"])

        ret = station.get_current_weather_data()
        if not ret:
            logger.error("Failed to retrieve weather data...")
            logger.error("Exiting...")
            exit(1)

        logger.info("Success!")
        logger.info(f"Current weather data: {station.weather_data}")

    except requests.exceptions.ConnectionError as cee:
        logger.error(cee)
        logger.error("Exiting...")
        exit(1)


if __name__ == "__main__":
    main()
