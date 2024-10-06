from datetime import datetime
from zoneinfo import ZoneInfo
import shutil
import os


def checkTokenFolderExists(tokenAddress):
    if not os.path.exists(tokenAddress):
        print(f"Creating directory for token {tokenAddress}...")
        os.makedirs(tokenAddress)
    else:
        print(f"Found directory for token {tokenAddress}!")


def getCurrentISOTime():
    now = datetime.now(ZoneInfo("UTC"))

    # using UTC because it's standard
    return now.replace(microsecond=0).isoformat()


def duplicateFile(source, destination):
    if not os.path.exists(source):
        return f"File {source} does not exist!"

    shutil.copy2(source, destination)
    print(f"Successfully copied {source} to {destination}!")
