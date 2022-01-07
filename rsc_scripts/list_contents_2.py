import os
from PIL import Image, ExifTags

img_folder = r"C:\python_test_images"
img_contents = os.listdir(img_folder)

for x in img_contents:
    full_path = os.path.join(img_folder, x)
    pil_img = Image.open(full_path)
    exif = {ExifTags.TAGS[k]: v for k, v in pil_img.getexif().items() if k in ExifTags.TAGS}

    print(exif)

    gps_all = {}

    try:
        for key in exif['GPSInfo'].keys():
            print("GPS code: {}".format(key))
            decoded_value = ExifTags.GPSTAGS.get(key)
            print("Label: {}".format(decoded_value))
            gps_all[decoded_value] = exif['GPSInfo'][key]
            print(exif['GPSInfo'][key])

        long_ref = gps_all.get('GPSLongitudeRef')
        lat_ref = gps_all.get('GPSLatitudeRef')

        long = gps_all.get('GPSLongitude')
        lat = gps_all.get('GPSLatitude')

        print(long_ref)
        print(lat_ref)

        print(long)
        print(lat)

    except:
        print("No GPS metadata is associated with this image: ")
        print(full_path)
        pass