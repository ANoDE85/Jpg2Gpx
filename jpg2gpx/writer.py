
import gpxpy
import gpxpy.gpx

import os

def write_gpx_file(output_name, input_files):
    gpx = gpxpy.gpx.GPX()
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    gpx_seg = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_seg)
    for fi in input_files:
        gpx_seg.points.append(gpxpy.gpx.GPXTrackPoint(
            latitude=fi.GPSInfo.coordinate.latitude,
            longitude=fi.GPSInfo.coordinate.longitude,
            elevation=fi.GPSInfo.coordinate.altitude,
            comment=os.path.basename(fi.Path)))
    
    with open(output_name, "w+b") as gpx_file:
        gpx_file.write(gpx.to_xml().encode('utf-8'))
        
