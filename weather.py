"""
Weather data classes definitions
"""

from dataclasses import dataclass
import datetime
from typing import Dict, Optional


@dataclass
class Coordinates:
    """Location coordinates"""

    latitude: Optional[float] = None
    longitude: Optional[float] = None


@dataclass
class Parameters:
    """System parameters"""

    type: Optional[int] = None  # Internal parameter
    id: Optional[int] = None  # Internal parameter
    message: Optional[str] = None  # Internal parameter
    country: Optional[str] = None  # Country code
    sunrise: Optional[datetime.datetime] = None  # Sunrise time
    sunset: Optional[datetime.datetime] = None  # Sunset time
    timezone: Optional[float] = None  # Shift in seconds from UTC
    city_id: Optional[int] = None  # City ID (deprecated)
    name: Optional[str] = None  # City name (deprecated)
    cod: Optional[int] = None  # Internal parameter


@dataclass
class Temperature:
    """Temperature type definition"""

    unit: Optional[
        int
    ] = None  # Temperature unit. Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit
    value: Optional[float] = None  # Temperature value.
    feels_like: Optional[
        float
    ] = None  # This temperature parameter accounts for the human perception of weather.
    mininimum: Optional[float] = None  # Minimum temperature at the moment.
    maximum: Optional[float] = None  # Maximum temperature at the moment.


@dataclass
class Wind:
    """Wind type definition"""

    speed: Optional[float] = None  # Wind speed. Default: meter/sec.
    deg: Optional[float] = None  # Wind direction, degrees(meteorological)
    gust: Optional[float] = None  # Wind gust.


@dataclass
class Weather:
    """Weather type definition based on https://openweathermap.org/weather-conditions"""

    condition_id: Optional[int] = None
    main: Optional[str] = None
    description: Optional[str] = None
    temperature: Optional[Temperature] = None
    visibility: Optional[float] = None  # visibility in meters
    pressure: Optional[float] = None  # Atmospheric pressure
    humidity: Optional[float] = None  # Humidity, %
    sea_level: Optional[float] = None  # Atmospheric pressure on the sea level, hPa
    grnd_level: Optional[float] = None  # Atmospheric pressure on the ground level, hPa
    wind: Optional[Wind] = None
    cloudiness: Optional[float] = None  # Cloudiness %
    rain_1h: Optional[float] = None  # Precipitation in mm/h.
    snow_1h: Optional[float] = None  # Precipitation in mm/h
    dt: Optional[datetime.datetime] = None  # Time of data calculation, Unix, UTC
    sys: Optional[Parameters] = None

    @staticmethod
    def from_dict(dict: Dict):
        """Parse weather data from dictionary.

        Args:
            dict (Dict): Dictionary containing open weather api response
        """
        return Weather(
            condition_id=dict["weather"][0]["id"],
            main=dict["weather"][0]["main"],
            description=dict["weather"][0]["description"],
            temperature=Temperature(
                unit=0,
                value=dict["main"]["temp"],
                feels_like=dict["main"]["feels_like"],
                mininimum=dict["main"]["temp_min"],
                maximum=dict["main"]["temp_max"],
            ),
            visibility=dict["visibility"],
            pressure=dict["main"]["pressure"],
            humidity=dict["main"]["humidity"],
            sea_level=dict["main"]["sea_level"],
            grnd_level=dict["main"]["grnd_level"],
            wind=Wind(
                speed=dict["wind"]["speed"],
                deg=dict["wind"]["deg"],
                gust=dict["wind"].get("gust"),
            ),
            cloudiness=dict["clouds"]["all"],
            rain_1h=dict.get("rain")["1h"] if "rain" in dict.keys() else None,
            snow_1h=dict.get("snow")["1h"] if "snow" in dict.keys() else None,
            dt=dict["dt"],
            sys=Parameters(
                type=dict["sys"]["type"],
                id=dict["sys"]["id"],
                country=dict["sys"]["country"],
                sunrise=dict["sys"]["sunrise"],
                sunset=dict["sys"]["sunset"],
                timezone=dict["timezone"],
                city_id=dict["id"],
                name=dict["name"],
                cod=dict["cod"],
            ),
        )
