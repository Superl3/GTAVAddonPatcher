import os
import shutil
import xml.etree.ElementTree as elemTree
from winreg import *

def getFile(path, name, depth, maxDepth=3):

    retPath = ""
    retName = ""
    if depth > maxDepth:
        return "", ""

    inner_file_list = os.listdir(path)
    isModPath = False
    for inner_file in inner_file_list:
        innerPath = path + '\\' + inner_file
        if inner_file.endswith(".rpf") == True:
            isModPath = True
            break
        elif os.path.isdir(innerPath) == True:
            x, y = getFile(innerPath, inner_file, depth+1)
            if x != "" or y != "":
                retPath = x
                retName = y
    if isModPath == True:
        return path, name
    return retPath, retName
    
def getFileList():

    car_mod_list = []
    fileList = list(os.listdir())
    fileList.sort()
    for folder in fileList:
        curPath = folder
        if os.path.isdir(curPath) == False:
            continue
        curPath, curName = getFile(curPath, folder, 0)
        if curPath == "" or curName == "":
            continue
        car_mod_list.append((curPath,curName))
    return car_mod_list

def getModPath():

    path = ""

    varSubkey = "SOFTWARE\\Rockstar Games\\Grand Theft Auto V"
    varReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    try:
        varKey = OpenKey(varReg, varSubkey)
        for x in range(1024):
            try:
                keyname = EnnumKey(varKey, x)
                varSubkey2 = "%s\\%s" % (varSubkey, keyname)
                varKey2 = OpenKey(varReg, varSubkey2)
                try:
                    for y in range(1024):
                        n, p, _ = EnumValue(varKey2, y)
                        if "InstallFolder" in n:
                            path = p
                except:
                    pass
                CloseKey(varKey2)
            except:
                pass
        CloseKey(varKey)
        CloseKey(varReg)
        return p + "\\mods\\update\\x64\\dlcpacks"
    except:
        return ""

def getInstallList(carList):
    print("Available Mod List ::\n")
    for idx, car in enumerate(carList):
        print ("'" + car[1] + "' --- (" + str(idx+1) + ")")
    n = int(input("press number you want to install, (0 means all) : "))
    install_list = []
    if n == 0:
        install_list = carList
    else:
        install_list.append(carList[n-1])
    return install_list

def modifyXml(filePath, txtList):
    tree = elemTree.parse(filePath)
    root = tree.getroot()
    root[0] [len(list(root[0]))-1].tail = "\n\t\t"
    for idx, txt in enumerate(txtList):
        newItem = elemTree.Element("Item")
        newItem.text = txt
        newItem.tail = "\n\t"
        if idx != len(txtList)-1:
            newItem.tail += "\t"
        root[0].append(newItem)
    tree.write(filePath)


def doInstall(carList, modPath):
    addXml = []
    addTxt = ""
    for car in carList:
        carPath = modPath + '\\' + car[1]
        if os.path.isdir(carPath) == True:
            print ("'" + car + "' is already exist in modlist, skipped")
            pass
        os.mkdir(carPath)
        shutil.copytree(car[0], carPath)
        addXml.append("dlcpacks:\\" + car[1] + "\\")
        addTxt += "\t<Item>dlcpacks:\\" + car[1] + "\\</Item>\n"
    xmlFilePath = modPath + "\\dlclist.xml"

    if os.path.exists(txtFilePath) == False:
        print("modlist.xml is not exist on modlist folder.")
        print("you should manually copy these lines:\n")
        print(addTxt)
    else:
        modifyXml(xmlFilePath, addTxt)
        print("modify modlist.xml done, copy modlist.xml to your update.rpf.")
        os.open(modPath)


carList = getFileList()
print(carList)
pass
modPath = getModPath()
if modPath == "":
    print("cannot find GTAV registery, program exit")
else:
    carList = getFileList()
    install_list = getInstallList(carList)
    doInstall(install_list, modPath)