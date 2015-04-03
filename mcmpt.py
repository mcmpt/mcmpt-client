#!/usr/bin/env python
import json
import os
import sys
import shutil
import time
import urllib2
versionS = "0.1"
versionI = 0

mcmptRepoURL = "https://raw.githubusercontent.com/mcmpt/mcmpt-repo/master/"
mcmptPath = os.path.expanduser("~") + "/mcmpt/"

def start():
    if len(sys.argv) == 1:
        helpM()
    elif sys.argv[1].lower() == "help":
        helpM()
    elif sys.argv[1].lower() == "update":
        updateM()
    elif sys.argv[1].lower() == "clean":
        cleanM()


def helpM():
    print("Minecraft Mod Package Toolkit version " + versionS + " (" + str(versionI) + ")")
    print("This is a command line toolkit for managing minecraft mods in an easy and simple way.")
    print("Commands:")
    print("  Help    : Shows this message.")
    print("  Update  : Updates the local cache of the repository.")
    print("  Clean   : Deletes the local cache of the repository. Run this command if mcmpt seems to be crashing.")


def updateM():
    print("Updating local repository catch.")
    if not installed():
        print("")
        print("This appears to be the first time you have run mcmpt.")
        print("A folder named \"mcmpt\" will be created in your home directory. ")
        print("This is way the important parts of mcmpt will be kept.")
        print("Do not try and modify these files as doing so may break mcmpt.")
        print("")
    else:
        print("Deleting old cache.")

    shutil.rmtree(mcmptPath)


    os.makedirs(mcmptPath);

    mcmptFileDict = {"updated" : time.time(),"versionMadeWith":versionI}
    mcmptFileJson = json.dumps(mcmptFileDict)
    mcmptFile = open(mcmptPath + "mcmpt.json",'w')
    mcmptFile.write(mcmptFileJson)
    mcmptFile.close();
    mcVersionsJson = webGetText(mcmptRepoURL + "mcVer.json")
    if not mcVersionsJson :
        print("Failed to download mcVer.json. This suggests the mcmpt repository or github is down.")
        sys.exit()

    print(mcVersionsJson)
    mcVersionsDict = json.loads(mcVersionsJson);
    print("Minecraft versions found:")
    for mcVer in mcVersionsDict:
        print(mcVer)
    mcVersionsFile = open(mcmptPath + "mcVer.json",'w')
    mcVersionsFile.write(mcVersionsJson)
    mcVersionsFile.close()



def cleanM():
    print("Deleting cache.")
    shutil.rmtree(mcmptPath)
    print("Cache deleted.")



def installed():
    if not os.path.isdir(mcmptPath):
        return False
    if not os.path.exists(mcmptPath + "mcmpt.json"):
        return False
    return True

def webGetText(url) :
    data = ""
    try :
        data = urllib2.urlopen(url)
    except urllib2.URLError as errorUrl:
        data = False
        print("Download for " + url + "failed. Reason:")
        print(errorUrl.reason)

    return data.read()


if __name__ == "__main__":
    start()