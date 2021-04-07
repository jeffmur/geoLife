import glob
import os
import subprocess
import time
import sys

dataIn = "/home/jeffmur/dev/privamov/data/user_by_month/"
dataOut = "/home/jeffmur/dev/privamov/data/gps_0.5_all/"
pyfile = "gen_user_all.py"

src_glob = glob.glob(dataIn + "*")
dst_glob = glob.glob(dataOut + "*")

# For verification compare src and dst blob
src = sorted(src_glob, key=lambda i: int(os.path.splitext(os.path.basename(i))[0]))
dst = sorted(dst_glob, key=lambda i: int(os.path.splitext(os.path.basename(i))[0]))

srcArr = []

for path in src:
    s = path.split("/")[7]
    srcArr.append(int(s))

i = 0
missCount = 0
missed = []
for path in dst:
    d = int((path.split("/")[7])[:-4])
    diff = 0
    if d != srcArr[i]:
        print(f"Missed: i:{i} : dst: {srcArr[i]}")
        i += 1
        missCount += 1
        missed.append(src[i - 1])
    else:
        print(f"i:{i} src: {srcArr[i]} - dst: {d}")

    i += 1

print(f"Missed: {missCount}")
print(missed)


if len(missed) == 0:
    print("Process Completed!!")
    exit()

for i in range(len(missed)):
    ## Thread each missing file
    batchFiles = str(missed[i])

    # # Create Child Process on new session
    cmdChild = ["gnome-terminal", "-x", "bash", "-c", f"./{pyfile} {batchFiles}"]
    subprocess.run(cmdChild)
    time.sleep(2)
