
import dataclasses
import datetime
import logging
import piexif

from . import exif

@dataclasses.dataclass
class GPSCoordinate:
    longitude: float
    latitude: float
    altitude: float

@dataclasses.dataclass
class GPSInfo:
    coordinate: GPSCoordinate
    timestamp: datetime.datetime


class ImageInfo:
    def __init__(self, path):
        self.__m_path = path
        self.__m_exif_info = None
        self.__m_gps_info = None

    @property
    def Path(self):
        return self.__m_path

    @property
    def ExifInfo(self):
        if self.__m_exif_info is None:
            self.__m_exif_info = exif.load_exif_info(self.__m_path)
        return self.__m_exif_info

    @property
    def GPSInfo(self):
        if self.__m_gps_info is None:
            self.__m_gps_info = self._load_gps_info()
        return self.__m_gps_info
        
    def _load_gps_info(self):
        if self.ExifInfo is None:
            return None

        coord_tuple = exif.load_gps_coordinate(self.ExifInfo)
        if coord_tuple is None:
            return None
        lon, lat, alt = coord_tuple
        coordinate = GPSCoordinate(
            longitude=lon,
            latitude=lat,
            altitude=alt)

        timestamp = exif.load_gps_timestamp(self.ExifInfo)

        return GPSInfo(
            coordinate=coordinate,
            timestamp=timestamp)

        
        
