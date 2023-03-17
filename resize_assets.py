from PIL import Image
import os

print("resizing images in the folder")
folder = "assets"
for i in os.listdir(folder):
    if not i.endswith(".md"):
        file = folder + "/" + i
        im = Image.open(file)
        ## Create small image
        im = im.resize((640, 480))
        im.save("assets-small/" + i, "JPEG")
        ## Create medium image
        im = im.resize((1920, 1280))
        im.save("assets-medium/" + i, "JPEG")
        ## Create large image
        im = im.resize((2400, 1600))
        im.save("assets-large/" + i, "JPEG")

os.system("cd assets-small && git add . && cd .. && cd assets-medium && git add . && cd .. && cd assets-large && git add .")
