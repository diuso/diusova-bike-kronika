import sys
import piexif
from fractions import Fraction

def deg_to_dms_rational(deg):
    """
    Convert decimal degrees to EXIF-usable rationals for DMS (degrees, minutes, seconds).
    """
    frac = Fraction(deg).limit_denominator()
    deg_abs = abs(deg)
    degrees = int(deg_abs)
    minutes = int((deg_abs - degrees) * 60)
    seconds = round((deg_abs - degrees - minutes/60) * 3600, 6)

    return [
        (degrees, 1),
        (minutes, 1),
        (int(seconds * 1000000), 1000000)
    ]

def set_gps_location(file_path, lat, lng, output_file):
    # Load EXIF data
    exif_dict = piexif.load(file_path)

    # Latitude
    lat_ref = 'N' if lat >= 0 else 'S'
    exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef] = lat_ref.encode()
    exif_dict['GPS'][piexif.GPSIFD.GPSLatitude] = deg_to_dms_rational(lat)

    # Longitude
    lng_ref = 'E' if lng >= 0 else 'W'
    exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef] = lng_ref.encode()
    exif_dict['GPS'][piexif.GPSIFD.GPSLongitude] = deg_to_dms_rational(lng)

    # Dump back to file
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, file_path, output_file)

    print(f"✅ GPS updated: {lat}, {lng} → saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python geotag.py <input.jpg> <output.jpg> <latitude> <longitude>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    latitude = float(sys.argv[3])
    longitude = float(sys.argv[4])

    set_gps_location(input_file, latitude, longitude, output_file)
