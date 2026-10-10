from PIL import Image
import argparse
import os
import subprocess
import sys

folder = "assets"


def handles(name):
    # The one rule for which files in assets/ get copies made: every file
    # directly in the folder except Markdown notes. The workflow's list step
    # applies the same rule before it calls this script.
    return not name.endswith(".md")


def names_from_list(list_file):
    # Read repo-relative paths, one per line, such as assets/US-NYC-1.jpg.
    # Every line is checked before any image is touched, so a bad list
    # changes nothing.
    with open(list_file, encoding="utf-8") as f:
        lines = [line.rstrip("\r\n") for line in f]
    names = []
    bad = []
    for path in lines:
        if not path:
            continue
        name = path[len(folder) + 1:]
        if (not path.startswith(folder + "/") or not name or "/" in name
                or not handles(name) or not os.path.isfile(path)):
            bad.append(path)
        elif name not in names:
            names.append(name)
    if bad:
        print("not resizing anything, because these listed paths are not "
              "files directly in " + folder + "/ that this script resizes:")
        for path in bad:
            print("  " + path)
        sys.exit(2)
    return names


parser = argparse.ArgumentParser(
    description="Make the small, medium and large copies of the images in "
                "assets/. With no option it does every image in the folder.")
parser.add_argument(
    "--files-from", metavar="LIST",
    help="only resize the images named in this file, one path such as "
         "assets/US-NYC-1.jpg per line; an empty file resizes nothing")
args = parser.parse_args()

if args.files_from is None:
    print("resizing images in the folder")
    names = [i for i in os.listdir(folder) if handles(i)]
else:
    names = names_from_list(args.files_from)
    print("resizing %d listed image(s)" % len(names))

for i in names:
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

if args.files_from is None:
    os.system("cd assets-small && git add . && cd .. && cd assets-medium && git add . && cd .. && cd assets-large && git add .")
elif names:
    # Stage only the copies made for the listed images, so a commit of the
    # staged files never carries anything else.
    subprocess.run(["git", "add", "--"]
                   + [d + "/" + i for i in names
                      for d in ("assets-small", "assets-medium", "assets-large")],
                   check=True)
