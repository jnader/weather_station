"""
A useful library for handling weather data using Open Weather API.
"""

import attrs
import datetime
import logging
import requests
from typing import Optional
from weather import Weather


@attrs.define()
class WeatherStation:
    """
    Class handling weather station data, forecasts and everything that
    can be handled.
    """

    open_weather_api_key: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    logger: logging.Logger = None
    weather_data: Weather = Weather()

    def set_open_weather_api_key(self, open_weather_api_key: str) -> None:
        """Set Open Weather API key

        Args:
            open_weather_api_key (str): key as a string
        """
        self.logger.info("Setting API key")
        self.open_weather_api_key = open_weather_api_key

    def set_position(self, latitude: float, longitude: float) -> None:
        """Set weather station's position latitude/longitude.

        Args:
            latitude (float): Latitude of the station
            longitude (float): Longitude of the station
        """
        self.logger.info(f"Setting latitude to {latitude} and longitude {longitude}")
        self.latitude = latitude
        self.longitude = longitude

    def get_current_weather_data(
        self,
        latitude: float = None,
        longitude: float = None,
    ) -> bool:
        """Get current weather data for a given (or already defined) position.

        Args:
            latitude (float, optional): Latitude. Defaults to None.
            longitude (float, optional): Longitude. Defaults to None.

        Returns:
            bool: True if ok, False otherwise.
        """
        self.logger.info("Get current weather data")
        requested_latitude = latitude if latitude else self.latitude
        request_longitude = longitude if longitude else self.longitude

        api_call = f"https://api.openweathermap.org/data/2.5/weather?lat={requested_latitude}&lon={request_longitude}&appid={self.open_weather_api_key}"

        r = requests.get(api_call)
        if r.status_code != 200:
            self.logger.error(f"Status code: {r.status_code}")
            return False

        self.weather_data = Weather.from_dict(r.json())
        return True
