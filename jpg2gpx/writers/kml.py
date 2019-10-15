
import itertools
import os
import simplekml

def _add_points_to_folder(folder, items):
    for item in items:
        folder.newpoint(
            name=os.path.basename(item.Path),
            coords=[(item.GPSInfo.coordinate.longitude, item.GPSInfo.coordinate.latitude, item.GPSInfo.coordinate.altitude),]
        )

def write(output_name, input_files, group_by_date=False):
    kml = simplekml.Kml()
    doc = kml.newdocument(name="Route")
    if group_by_date:        
        for date, items in itertools.groupby(input_files, key=lambda item: item.GPSInfo.timestamp.date()):
            folder = doc.newfolder(name=str(date))
            _add_points_to_folder(folder, items)
    else:
        folder = doc.newfolder(name="All waypoints")
        _add_points_to_folder(folder, input_files)
        
    kml.save(output_name)