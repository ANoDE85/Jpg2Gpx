
import datetime
import os

from . import exif
from . import model


def KeyFunc_GPSDate(obj: model.ImageInfo) -> datetime.datetime:
    if obj.GPSInfo is None or obj.GPSInfo.timestamp is None:
        return KeyFunc_ExifTime(obj)
    return obj.GPSInfo.timestamp

def KeyFunc_ExifTime(obj: model.ImageInfo) -> datetime.datetime:
    try:
        if obj.ExifInfo is None:
            raise ValueError("No EXIF data found")
        stamp = exif.load_exif_time(obj.ExifInfo)
        if stamp is None:
            raise ValueError("No EXIF timestamp found")
        return stamp
    except ValueError:
        raise ValueError(f"Cannot use ExifTime sort mode: File '{obj.Path}' -> {str(e)}")

def KeyFunc_FileName(obj: model.ImageInfo) -> str:
    return os.path.basename(obj.Path).lower()


def __LoadKeyFuncs():
    sorters = {}
    for name, item in globals().items():
        if name.startswith("KeyFunc_") and callable(item):
            sorters[name[len("KeyFunc_"):].lower()] = item
    return sorters


Sorters = __LoadKeyFuncs()

SortModes = list(Sorters.keys())