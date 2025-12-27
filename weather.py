"""
Weather data classes definitions
"""

from dataclasses import dataclass
import datetime
from typing import Dict, Optional


@dataclass
class Coordinates:
    """Location coordinates"""

    latitude: Optional[float] = None  # Latitude
    longitude: Optional[float] = None  # Longitude

    @staticmethod
    def from_dict(dict: Dict = None):
        if not dict:
            return None

        return Coordinates(
            latitude=dict.get("lat", None), longitude=dict.get("lon", None)
        )


@dataclass
class City:
    """City type definition"""

    id: Optional[int] = None  # City ID
    name: Optional[str] = None  # City name
    coord: Optional[Coordinates] = None  # City latitude/longitude
    country: Optional[str] = None  # Country code
    population: Optional[int] = None  # Population
    timezone: Optional[int] = None  # Timezone in Unix UTC
    sunrise: Optional[int] = None  # Sunrise time in Unix UTC
    sunset: Optional[int] = None  # Sunset time in Unix UTC

    @staticmethod
    def from_dict(dict: Dict = None):
        if not dict:
            return None
        if "population" in dict.keys():
            return City(
                id=dict.get("id", None),
                name=dict.get("name", None),
                coord=Coordinates.from_dict(dict.get("coord", None)),
                country=dict.get("country", None),
                population=dict.get("population", None),
                timezone=dict.get("timezone", None),
                sunrise=dict.get("sunrise", None),
                sunset=dict.get("sunset", None),
            )
        return City(
            id=dict.get("id", None),
            name=dict.get("name", None),
            coord=Coordinates.from_dict(dict.get("coord", None)),
            country=dict.get("sys", None).get("country", None),
            sunrise=dict.get("sys", None).get("sunrise", None),
            sunset=dict.get("sys", None).get("sunset", None),
            timezone=dict.get("timezone", None),
        )


@dataclass
class WeatherCondition:
    """Weather conditions as described in https://openweathermap.org/weather-conditions"""

    id: int = 0  # Weather condition ID
    group: Optional[str] = ""  # Weather condition group
    description: Optional[str] = ""  # Weather condition description
    icon: Optional[str] = ""  # Weather condition icon

    @staticmethod
    def from_dict(dict: Dict = None):
        return WeatherCondition(
            id=dict.get("id", 0),
            group=dict.get("main", ""),
            description=dict.get("description", ""),
            icon=dict.get("icon", ""),
        )


@dataclass
class Parameters:
    """System parameters"""

    type: Optional[int] = None  # Internal parameter
    id: Optional[int] = None  # Internal parameter
    message: Optional[str] = None  # Internal parameter
    pod: Optional[str] = None  # Part of day ('n' or 'd')

    @staticmethod
    def from_dict(dict: Dict = None):
        return Parameters(
            type=dict.get("type", None),
            id=dict.get("id", None),
            message=dict.get("message", None),
            pod=dict.get("pod", None),
        )


@dataclass
class WeatherMainData:
    """Weather main data"""

    temp: Optional[float] = None  # Temperature value.
    feels_like: Optional[
        float
    ] = None  # This temperature parameter accounts for the human perception of weather.
    mininimum_temperature: Optional[float] = None  # Minimum temperature at the moment.
    maximum_temperature: Optional[float] = None  # Maximum temperature at the moment.
    pressure: Optional[float] = None  # Atmospheric pressure on the sea level, hPa
    humidity: Optional[float] = None  # Humidity, %
    sea_level: Optional[float] = None  # Atmospheric pressure on the sea level, hPa
    grnd_level: Optional[float] = None  # Atmospheric pressure on the ground level, hPa
    temp_kf: Optional[float] = None # Internal parameter

    @staticmethod
    def from_dict(dict: Dict = None):
        return WeatherMainData(
            temp=dict.get("temp", None),
            feels_like=dict.get("feels_like", None),
            mininimum_temperature=dict.get("temp_min", None),
            maximum_temperature=dict.get("temp_max", None),
            pressure=dict.get("pressure", None),
            humidity=dict.get("humidity", None),
            sea_level=dict.get("sea_level", None),
            grnd_level=dict.get("grnd_level", None),
            temp_kf=dict.get("temp_kf", None),
        )


@dataclass
class Wind:
    """Wind type definition"""

    speed: Optional[float] = None  # Wind speed. Default: meter/sec.
    deg: Optional[float] = None  # Wind direction, degrees(meteorological)
    gust: Optional[float] = None  # Wind gust.

    @staticmethod
    def from_dict(dict: Dict = None):
        return Wind(
            speed=dict.get("speed", None),
            deg=dict.get("deg", None),
            gust=dict.get("gust", None),
        )


@dataclass
class Cloud:
    """Cloud type definition"""

    all: Optional[int] = None

    @staticmethod
    def from_dict(dict: Dict = None):
        return Cloud(all=dict.get("all", None))


@dataclass
class Precipitation:
    """Precipitation type definition"""

    value: Optional[float] = None


@dataclass
class Weather:
    """Weather type definition based on https://openweathermap.org/current"""

    weather_condition: Optional[WeatherCondition] = None
    base: Optional[str] = None
    weather_data: Optional[WeatherMainData] = None
    visibility: Optional[float] = None  # visibility in meters
    wind: Optional[Wind] = None
    clouds: Optional[Cloud] = None  # Clouds data
    rain: Optional[Precipitation] = None  # Precipitation in mm/h.
    snow: Optional[Precipitation] = None  # Precipitation in mm/h
    dt: Optional[int] = None  # Time of data calculation, Unix, UTC
    sys: Optional[Parameters] = None
    pop: Optional[float] = None  # Propoability of precipitation
    city: Optional[City] = None  # City information

    @staticmethod
    def from_dict(dict: Dict = None):
        """Parse weather data from dictionary.

        Args:
            dict (Dict): Dictionary containing open weather api response
        """
        return Weather(
            weather_condition=WeatherCondition.from_dict(dict.get("weather", None)[0]),
            base=dict.get("base", None),
            weather_data=WeatherMainData.from_dict(dict.get("main", None)),
            wind=Wind.from_dict(dict.get("wind", None)),
            visibility=dict.get("visibility", None),
            clouds=Cloud.from_dict(dict.get("clouds", None)),
            rain=Precipitation(dict.get("rain", None)),
            snow=Precipitation(dict.get("snow", None)),
            dt=dict["dt"],
            sys=Parameters.from_dict(dict.get("sys", None)),
            city=City.from_dict(dict),
        )
