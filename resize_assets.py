from PIL import Image
import os

print("resizing images in the folder")
folder = "assets"
for i in os.listdir(folder):
    if not i.endswith(".md"):
        file = folder + "/" + i
        
        ## Create small image
        im = Image.open(file)
        im.thumbnail((640, 480))
        im.save("assets-small/" + i, "JPEG")
        im.close()
        ## Create medium image
        im = Image.open(file)
        im.thumbnail((1920, 1280))
        im.save("assets-medium/" + i, "JPEG")
        im.close()
        ## Create large image
        im = Image.open(file)
        im.resize((2400, 1600))
        im.save("assets-large/" + i, "JPEG")
        im.close()

os.system("cd assets-small && git add . && cd .. && cd assets-medium && git add . && cd .. && cd assets-large && git add .")
