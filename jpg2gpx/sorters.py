
from . import model


def KeyFunc_ByExifDate(obj: model.ImageInfo) -> str:
    return ""


Sorters = {
    "exifdate" : KeyFunc_ByExifDate
}


SortModes = list(Sorters.keys())