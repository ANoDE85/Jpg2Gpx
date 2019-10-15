
import gpxpy
import gpxpy.gpx

import itertools
import os


def _add_track(gpx, segment_name, items):
    gpx_track = gpxpy.gpx.GPXTrack(segment_name)
    gpx.tracks.append(gpx_track)
    gpx_seg = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_seg)
    for fi in items:
        gpx_seg.points.append(gpxpy.gpx.GPXTrackPoint(
            latitude=fi.GPSInfo.coordinate.latitude,
            longitude=fi.GPSInfo.coordinate.longitude,
            elevation=fi.GPSInfo.coordinate.altitude,
            comment=os.path.basename(fi.Path)))


def write(output_name, input_files, group_by_date=False):
    gpx = gpxpy.gpx.GPX()

    if group_by_date:        
        for date, items in itertools.groupby(input_files, key=lambda item: item.GPSInfo.timestamp.date()):
            _add_track(gpx, str(date), items)
    else:
        _add_track(gpx, "Route", input_files)
    
    with open(output_name, "w+b") as gpx_file:
        gpx_file.write(gpx.to_xml().encode('utf-8'))
    
