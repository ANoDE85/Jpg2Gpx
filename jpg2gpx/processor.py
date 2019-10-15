
import os

from . import model
from . import sorters
from . import writer


SortModes = sorters.SortModes


class Processor(object):
    def __init__(self):
        pass

    @staticmethod
    def __is_jpeg(f):
        return os.path.splitext(f)[1].lower() in (".jpg", ".jpeg")

    def process(self, input_dir, recoursive, sort_mode, output_name):
        input_files = self._load_file_list(input_dir, recoursive)
        input_files.sort(key = sorters.Sorters[sort_mode])
        writer.write_gpx_file(output_name, input_files)
        

    def _load_file_list(self, input_dir, recoursive):
        file_list = []
        if not recoursive:
            file_list = [model.ImageInfo(os.path.join(input_dir,f)) for f in os.listdir(input_dir) if Processor.__is_jpeg(f)]
        else:
            for root, _, files in os.walk(input_dir):
                file_list.extend((model.ImageInfo(os.path.join(root, f)) for f in files if Processor.__is_jpeg(f)))
        return list(filter(self._check_valid_gps_coordinates, file_list))

    def _check_valid_gps_coordinates(self, image_info):
        if image_info.GPSCoordinates is None:
            print(f"File '{image_info.Path}' does not contain valid GPS coordinates (EXIF info missing or no GPS data)")
            return False
        return True