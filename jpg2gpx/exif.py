
import datetime
import logging
import piexif


def rational_to_float(rational_tuple):
    return rational_tuple[0] / rational_tuple[1]


def convert_coordinate(coordinate_ref, coord_tuple):
    degrees, minutes, seconds = tuple(map(rational_to_float, coord_tuple))
    coord_as_float = degrees + minutes / 60 + seconds / 3600
    if coordinate_ref in (b"S", b"W"):
        coord_as_float *= -1
    return coord_as_float


def convert_altitude(altitude_ref, altitude_tuple):
    altitude_as_float = rational_to_float(altitude_tuple)
    if altitude_ref == 1:
        altitude_as_float *= -1
    return altitude_as_float


def convert_timestamp(time_tuple):
    return (
        int(round(rational_to_float(time_tuple[0]), 0)),
        int(round(rational_to_float(time_tuple[1]), 0)),
        int(round(rational_to_float(time_tuple[2]), 0)))

def load_exif_info(file_path):
    try:
        return piexif.load(file_path)
    except Exception as e:
        logging.warning(f"Cannot load EXIF info from file '{file_path}': {str(e)}")


def load_gps_coordinate(exif_info):
    try:
        gps_info = exif_info["GPS"]
    except KeyError:
        return None

    try:
        longitude = convert_coordinate(
                    gps_info[piexif.GPSIFD.GPSLongitudeRef], 
                    gps_info[piexif.GPSIFD.GPSLongitude])
        latitude = convert_coordinate(
                gps_info[piexif.GPSIFD.GPSLatitudeRef],
                gps_info[piexif.GPSIFD.GPSLatitude])
    except KeyError:
        return None

    try:
        altitude = convert_altitude(
            gps_info[piexif.GPSIFD.GPSAltitudeRef],
            gps_info[piexif.GPSIFD.GPSAltitude])
    except KeyError:
        altitude = None
    
    return (longitude, latitude, altitude)


def load_gps_timestamp(exif_info):
    try:
        gps_info = exif_info["GPS"]
    except KeyError:
        return None
    
    try:
        date_string = gps_info[piexif.GPSIFD.GPSDateStamp]
        date_tuple = tuple((int(x) for x in date_string.split(b":")))
    except KeyError:
        return None
    
    try:
        time_tuple = gps_info[piexif.GPSIFD.GPSTimeStamp]
        time_tuple = convert_timestamp(time_tuple)
    except KeyError:
        time_tuple = (0,0,0)
    
    return datetime.datetime(
        date_tuple[0], date_tuple[1], date_tuple[2],
        time_tuple[0], time_tuple[1], time_tuple[2])


def load_exif_time(exif_info):
    try:
        time_string = exif_info["0th"][piexif.ImageIFD.DateTime].decode("ascii")
    except KeyError:
        return None
    try:
        return datetime.datetime.strptime(time_string, "%Y:%m:%d %H:%M:%S")
    except ValueError as e:
        logging.warning(f"Illegal Date/Time string in EXIF Data: {time_string}: {str(e)}")
    return None