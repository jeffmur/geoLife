import glob
import os
import subprocess
import time
import sys

dataIn = "/home/jeffmur/data/geoLife/split_by_month_output/"
dataOut = "/home/jeffmur/dev/testgeo/data/gps_0.186411_month/"
pyfile = "gen_user_month.py"

src_glob = glob.glob(dataIn + "*")

# For verification compare src and dst blob
src = sorted(src_glob, key=lambda i: int(os.path.splitext(os.path.basename(i))[0]))


def walkDirs(DataDirectory, size):
    # Get static ref of all users sorted by userID
    temp = glob.glob(DataDirectory + "*")
    all_users = sorted(
        temp, key=lambda i: int(os.path.splitext(os.path.basename(i))[0])
    )

    monthPerUser = []

    for base, dirs, files in os.walk(DataDirectory):
        # print('Searching in : ', base)
        c = 0
        for Files in files:
            c += 1

        if base != DataDirectory:
            baseName = int(base.split("/")[size])
            monthPerUser.append([baseName, c])

    # Sorted by UserID
    monthPerUser.sort(key=lambda x: x[0])

    for i in range(len(monthPerUser)):
        monthPerUser[i] = [i, monthPerUser[i][0], monthPerUser[i][1]]

    return monthPerUser


inn = walkDirs(dataIn, 6)
out = walkDirs(dataOut, 7)


s = 0
missCount = 0
missed = []
for i in range(0, len(out)):

    if inn[s] != out[i]:
        checkItem = inn[s]
        print(f"Missed USER src: {checkItem} ")  #: dst: {out[i][1]}")
        missCount += 1
        # print(src[checkItem[0]])
        missed.append(src[checkItem[0]])

    s += 1

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
