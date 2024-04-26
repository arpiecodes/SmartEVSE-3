#this script will be run by platformio.ini from its native directory
import os, sys, gzip, shutil

#check for the two files we need to be able to keep updating the firmware by the /update endpoint:
if not os.path.isfile("data/update2.html"):
    print("Missing file: data/update2.html")
    sys.exit(1)
if not os.path.isfile("data/app.js"):
    print("Missing file: data/app.js")
    sys.exit(2)
if os.path.isdir("pack.tmp"):
    shutil.rmtree('pack.tmp')
try:
    shutil.copytree('data', 'pack.tmp/data')
    # now gzip the stuff except zones.csv since this file is not served by mongoose but directly accessed:
    for file in os.listdir("pack.tmp/data"):
        filename = os.fsdecode(file)
        if not filename == "zones.csv":
            with open('pack.tmp/data/' + filename, 'rb') as f_in, gzip.open('pack.tmp/data/' + filename + '.gz', 'wb') as f_out:
                f_out.writelines(f_in)
                os.remove('pack.tmp/data/' + filename)
            continue
        else:
            continue

    os.system('cd pack.tmp; python ../pack.py data/* >../src/packed_fs.c')
except Exception as e:
    print(f"An error occurred: {str(e)}")
    sys.exit(100)
if shutil.rmtree("pack.tmp"):
    print("Failed to clean up temporary files")
    sys.exit(9)
