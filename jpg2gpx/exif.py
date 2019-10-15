
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