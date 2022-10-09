from dataclasses import dataclass
from datetime import datetime


@dataclass
class GribParameter:
    """GRIB parameter"""
    level_type: str  # Level type
    level: int       # Level
    pname: str       # Parameter name
    sname: str       # Parameter short name
    code: int        # Code
    unit: str        # Unit


@dataclass
class GribMessage(GribParameter):
    """GRIB message model"""
    center: str           # Center that make GRIB data
    reftime: datetime     # Base time
    predict: int          # Offset in hours
    ensemble_member: int  # Ensemble's number
    values: list[float]   # Data array


@dataclass
class GribCoordinate:
    """GRIB coord"""
    lat: float  # Latitude
    lon: float  # Longitude


@dataclass
class GribKeyValue:
    """GRIB key value item"""
    key: str     # Grib key
    value: str   # Grib value


@dataclass
class GribGrid:

    """GRIB GRID descriptions"""
    first_grid_point: GribCoordinate = None        # First grid coordinate
    last_grid_point:  GribCoordinate = None        # Last grid coordinate
    lat_step:         float = 0                    # Step by latitude. Only for regular grid
    lon_step:         float = 0                    # Step by longitude. Only for regular grid
    lat_count:        int = 0                      # Latitudes count
    lon_count:        int = 0                      # Longitudes count
    coords:           list[GribCoordinate] = None  # Grid coordinates lat/lon
