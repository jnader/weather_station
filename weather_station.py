"""
A useful library for handling weather data using Open Weather API.
"""

import datetime
import logging
from typing import Iterable, Optional

import attrs
import requests
from weather import City, Weather


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
    weather_data: Iterable[Weather] = []

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

        api_call = "https://api.openweathermap.org/data/2.5/weather?"
        api_call += f"lat={requested_latitude}&lon={request_longitude}"
        api_call += f"&appid={self.open_weather_api_key}"

        response = requests.get(api_call)
        if response.status_code != 200:
            self.logger.error(f"Status code: {response.status_code}")
            return False

        self.weather_data.append(Weather.from_dict(response.json()))
        return True

    def get_5_day_3_hour_forecast_data(
        self, latitude: float = None, longitude: float = None, step_count: int = 15
    ) -> bool:
        """Get 5 day weather forecast with 3-hour step.

        Args:
            latitude (float, optional): Latitude. Defaults to None.
            longitude (float, optional): Longitude. Defaults to None.
            step_count (int, optional): Steps count. Defaults to 96.

        Returns:
            bool: True if ok, False otherwise
        """
        self.logger.info(f"Get {step_count} 3-hour forecast")
        requested_latitude = latitude if latitude else self.latitude
        request_longitude = longitude if longitude else self.longitude

        api_call = "https://api.openweathermap.org/data/2.5/forecast?"
        api_call += f"lat={requested_latitude}&lon={request_longitude}"
        api_call += f"&appid={self.open_weather_api_key}"
        if step_count:
            api_call += f"&cnt={step_count}"

        response = requests.get(api_call)
        if response.status_code != 200:
            self.logger.error(f"Status code: {response.status_code}")
            return False

        data = response.json()
        city = City.from_dict(data.get("city"))
        for list_row in data["list"]:
            row = Weather.from_dict(list_row)
            row.city = city
            self.weather_data.append(row)
        return True
