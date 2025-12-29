"""
Typical weather station test program.
To run this script, you should be connected to the internet.
"""

import logging
import sys
import requests
import yaml

import weather_station as ws

logger = logging.getLogger()
logging.basicConfig(filename="/tmp/myapp.log", level=logging.INFO, filemode="w")

IP_LOCATION_REQUEST = "http://ip-api.com/json?fields=lat,lon"


def main():
    """Main function"""
    logger.info("Gettting latitude/longitude from IP address...")
    try:
        response = requests.get(IP_LOCATION_REQUEST)
        if response.status_code != 200:
            logger.error("Couldn't retrieved position from IP...")
            logger.error("Exiting...")
            sys.exit(1)

        latitude, longitude = response.json().values()
        logger.info("Found! Latitude: %s , Longitude: %s", latitude, longitude)

        logger.info("Creating weather station")
        station = ws.WeatherStation(
            latitude=latitude, longitude=longitude, logger=logger
        )

        with open("keys.yaml", "r", encoding="utf-8") as file:
            keys = yaml.load(file, yaml.FullLoader)
            station.set_open_weather_api_key(keys["open_weather_api_key"])

        ret = station.get_current_weather_data()
        if not ret:
            logger.error("Failed to retrieve weather data...")
            logger.error("Exiting...")
            sys.exit(1)

        ret = station.get_5_day_3_hour_forecast_data(step_count=3)
        if not ret:
            logger.error("Failed to retrieve weather forecast...")
            logger.error("Exiting...")
            sys.exit(1)


        logger.info("Success!")
        logger.info("Current weather data: %s", station.weather_data)

    except requests.exceptions.ConnectionError as cee:
        logger.error(cee)
        logger.error("Exiting...")
        sys.exit(1)


if __name__ == "__main__":
    main()
