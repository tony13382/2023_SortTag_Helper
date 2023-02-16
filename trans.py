import glob  
from opencc import OpenCC
cc = OpenCC('s2t')

fileList = []
fileList = glob.glob(r"*lrc")

setcodeType = input("Input encoding ( GB2312[g] / utf-8 [u] ): ")
if(setcodeType=="g" or setcodeType=="G"):
    setcodeType = "GB2312"
elif(setcodeType=="u" or setcodeType=="U"):
    setcodeType = "UTF-8"

for docPath in fileList:
    try:
        print('Encode Converting...',docPath)
        readContent = ""
        with open(docPath,"r",encoding = setcodeType) as inFile:
            readContent = inFile.read()
        with open(docPath,"w", encoding="UTF-8") as outFile:
            outFile.write(readContent)
    except Exception as e:
        print("Error")
        print(e)
    
    try:
        print('Translating...',docPath)
        newLrc = ''
        f = open(docPath, 'r')
        for line in f.readlines():
            newLrc = newLrc + cc.convert(line)
        f.close()
        print(newLrc)
        f = open(docPath, 'w+')
        f.write(newLrc)
        f.close()
    except Exception as e:
        print("Error")
        print(e)

    print('-------------------------')
    
    
    