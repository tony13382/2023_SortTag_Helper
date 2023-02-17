import glob  
from opencc import OpenCC
cc = OpenCC('s2t')

fileList = []
fileList = glob.glob(r"*lrc") # 取得ＬＲＣ檔案
errFileList = []

# 編碼設定
setcodeType = ""
setcodeType = input("Input encoding ( QQ音樂預設-GB2312[g] / utf-8 [u] ): ")
if(setcodeType=="g" or setcodeType=="G"):
    setcodeType = "GB2312"
elif(setcodeType=="u" or setcodeType=="U" or setcodeType ==""):
    setcodeType = "UTF-8"

# 轉換
for docPath in fileList:
    try:
        print('Encode Converting...',docPath)
        readContent = ""
        with open(docPath,"r",encoding = setcodeType) as inFile:
            readContent = inFile.read()  # 讀取檔案
        with open(docPath,"w", encoding="UTF-8") as outFile:
            outFile.write(readContent)  # 寫入文件
        
    except Exception as e:
        print("Error")
        print(e)
        errFileList.append(docPath)
    
    try:
        print('Translating...',docPath)
        newLrc = ''
        f = open(docPath, 'r', encoding="UTF-8")
        for line in f.readlines():
            newLrc = newLrc + cc.convert(line)  #讀取歌詞 
        f.close()
        print(newLrc[0:20])

        # 儲存檔案
        savePath = cc.convert(docPath)[0:cc.convert(docPath).find(" - ")] + "/" + cc.convert(docPath)
        f = open(savePath, 'w+', encoding="UTF-8")
        f.write(newLrc)
        f.close()
    except Exception as e:
        print("Error")
        print(e)
        errFileList.append(docPath)

    print('--------------------------------')

print('翻譯檔案完成 ',len(fileList)-len(errFileList))

# 錯誤檔案輸出
if len(errFileList) > 0:
    print('Fail List:')
    print(errFileList)