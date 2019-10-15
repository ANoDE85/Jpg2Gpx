
import dataclasses
import logging
import piexif

from . import exif

@dataclasses.dataclass
class GPSCoordinate:
    longitude: float
    latitude: float
    altitude: float


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
            try:
                self.__m_exif_info = piexif.load(self.__m_path)
            except Exception as e:
                logging.warning(f"Cannot load EXIF info from file '{self.Path}': {str(e)}")
                pass
        return self.__m_exif_info

    @property
    def GPSCoordinates(self):
        if self.__m_gps_info is None:
            self.__m_gps_info = self._load_gps_info()
        return self.__m_gps_info

    def _load_gps_info(self):
        if self.ExifInfo is None:
            return None
        try:
            gps_info = self.ExifInfo["GPS"]
            longitude=exif.convert_coordinate(
                    gps_info[piexif.GPSIFD.GPSLongitudeRef], 
                    gps_info[piexif.GPSIFD.GPSLongitude])
            latitude=exif.convert_coordinate(
                    gps_info[piexif.GPSIFD.GPSLatitudeRef],
                    gps_info[piexif.GPSIFD.GPSLatitude])
            try:
                altitude = exif.convert_altitude(
                    gps_info[piexif.GPSIFD.GPSAltitudeRef],
                    gps_info[piexif.GPSIFD.GPSAltitude],
                )
            except KeyError:
                altitude = None
            return GPSCoordinate(
                longitude=longitude, 
                latitude=latitude, 
                altitude=altitude)
        except KeyError:
            return None

        
        
