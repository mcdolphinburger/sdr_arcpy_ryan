import os

img_folder = r"C:\Users\ryans\Pictures\iCloud Photos\Downloads"

img_contents = os.listdir(img_folder)

for x in img_contents:
    print(x)
    full_path = os.path.join(img_folder, x)
    print(full_path) 