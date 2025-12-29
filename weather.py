"""
Weather data classes definitions
"""

from dataclasses import dataclass
import datetime
from typing import Dict, Iterable, Optional


@dataclass
class Coordinates:
    """Location coordinates"""

    latitude: Optional[float] = None  # Latitude
    longitude: Optional[float] = None  # Longitude

    @staticmethod
    def from_dict(data: Dict = None):
        """Initialize Coordinates from dictionary

        Args:
            data (Dict, optional): Dictionary containing coordinates. Defaults to None.

        Returns:
            Coordinates: Coordinates object
        """
        if not data:
            return None

        return Coordinates(
            latitude=data.get("lat", None), longitude=data.get("lon", None)
        )


@dataclass
class City:
    """City type definition"""

    city_id: Optional[int] = None  # City ID
    name: Optional[str] = None  # City name
    coord: Optional[Coordinates] = None  # City latitude/longitude
    country: Optional[str] = None  # Country code
    population: Optional[int] = None  # Population
    timezone: Optional[int] = None  # Timezone in Unix UTC
    sunrise: Optional[int] = None  # Sunrise time in Unix UTC
    sunset: Optional[int] = None  # Sunset time in Unix UTC

    @staticmethod
    def from_dict(data: Dict = None):
        """initialize City from dictionary

        Args:
            data (Dict, optional): Dictionary containing city. Defaults to None.

        Returns:
            City: City object
        """
        if not data:
            return None
        if "population" in data.keys():
            return City(
                city_id=data.get("id", None),
                name=data.get("name", None),
                coord=Coordinates.from_dict(data.get("coord", None)),
                country=data.get("country", None),
                population=data.get("population", None),
                timezone=data.get("timezone", None),
                sunrise=data.get("sunrise", None),
                sunset=data.get("sunset", None),
            )
        return City(
            city_id=data.get("id", None),
            name=data.get("name", None),
            coord=Coordinates.from_dict(data.get("coord", None)),
            country=data.get("sys", None).get("country", None),
            sunrise=data.get("sys", None).get("sunrise", None),
            sunset=data.get("sys", None).get("sunset", None),
            timezone=data.get("timezone", None),
        )


@dataclass
class WeatherCondition:
    """Weather conditions as described in https://openweathermap.org/weather-conditions"""

    condition_id: int = 0  # Weather condition ID
    group: Optional[str] = ""  # Weather condition group
    description: Optional[str] = ""  # Weather condition description
    icon: Optional[str] = ""  # Weather condition icon

    @staticmethod
    def from_dict(data: Dict = None):
        """Initialize WeatherCondition from dictionary.

        Args:
            data (Dict, optional): Dictionary containing WeatherCondition. Defaults to None.

        Returns:
            WeatherCondition: WeatherCondition object
        """
        return WeatherCondition(
            condition_id=data.get("id", 0),
            group=data.get("main", ""),
            description=data.get("description", ""),
            icon=data.get("icon", ""),
        )


@dataclass
class Parameters:
    """System parameters"""

    type: Optional[int] = None  # Internal parameter
    identifier: Optional[int] = None  # Internal parameter
    message: Optional[str] = None  # Internal parameter
    pod: Optional[str] = None  # Part of day ('n' or 'd')

    @staticmethod
    def from_dict(data: Dict = None):
        """Initialize Parameters from dictionary

        Args:
            data (Dict, optional): Dictionary containing Parameters. Defaults to None.

        Returns:
            Parameters: Parameters object
        """
        return Parameters(
            type=data.get("type", None),
            identifier=data.get("id", None),
            message=data.get("message", None),
            pod=data.get("pod", None),
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
    temp_kf: Optional[float] = None  # Internal parameter

    @staticmethod
    def from_dict(data: Dict = None):
        """Initialize WeatherMainData from dictionary

        Args:
            data (Dict, optional): Dictionary containing WeatherMainData. Defaults to None.

        Returns:
            WeatherMainData: WeatherMainData object
        """
        return WeatherMainData(
            temp=data.get("temp", None),
            feels_like=data.get("feels_like", None),
            mininimum_temperature=data.get("temp_min", None),
            maximum_temperature=data.get("temp_max", None),
            pressure=data.get("pressure", None),
            humidity=data.get("humidity", None),
            sea_level=data.get("sea_level", None),
            grnd_level=data.get("grnd_level", None),
            temp_kf=data.get("temp_kf", None),
        )


@dataclass
class Wind:
    """Wind type definition"""

    speed: Optional[float] = None  # Wind speed. Default: meter/sec.
    deg: Optional[float] = None  # Wind direction, degrees(meteorological)
    gust: Optional[float] = None  # Wind gust.

    @staticmethod
    def from_dict(data: Dict = None):
        """Initialize Wind from dictionary.

        Args:
            data (Dict, optional): Dictionary containing Wind information. Defaults to None.

        Returns:
            Wind: Wind object
        """
        return Wind(
            speed=data.get("speed", None),
            deg=data.get("deg", None),
            gust=data.get("gust", None),
        )


@dataclass
class Cloud:
    """Cloud type definition"""

    all: Optional[int] = None

    @staticmethod
    def from_dict(data: Dict = None):
        """Initialize cloudiness from dictionary

        Args:
            data (Dict, optional): Dictionary containing cloudiness information. Defaults to None.

        Returns:
            Cloud: Cloud object
        """
        return Cloud(all=data.get("all", None))


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
    timestamp: Optional[int] = None  # Time of data calculation, Unix, UTC
    sys: Optional[Parameters] = None
    pop: Optional[float] = None  # Propoability of precipitation
    city: Optional[City] = None  # City information

    @staticmethod
    def from_dict(data: Dict = None):
        """Parse weather data from dictionary.

        Args:
            data (Dict): Dictionary containing open weather api response
        """
        return Weather(
            weather_condition=WeatherCondition.from_dict(data.get("weather", None)[0]),
            base=data.get("base", None),
            weather_data=WeatherMainData.from_dict(data.get("main", None)),
            wind=Wind.from_dict(data.get("wind", None)),
            visibility=data.get("visibility", None),
            clouds=Cloud.from_dict(data.get("clouds", None)),
            rain=Precipitation(data.get("rain", None)),
            snow=Precipitation(data.get("snow", None)),
            timestamp=data.get("dt"),
            sys=Parameters.from_dict(data.get("sys", None)),
            city=City.from_dict(data),
        )


        )
