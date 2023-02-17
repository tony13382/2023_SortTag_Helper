# load the libraries that we'll use  
from mutagen.mp3 import MP3  
from mutagen.easyid3 import EasyID3  
import mutagen.id3   
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
import glob  
import json 
from opencc import OpenCC
cc = OpenCC('s2t')

# 取得輔助字典庫
convertDict = {}
with open('data.json') as f:
    convertDict = json.load(f)

# 確認首文字對應英文
def checkWord(word):
    if word not in convertDict:
        inputWord = input( word + " | INPUT WORD: ") # 如果沒有資料可以輸入定義字首（長度不可大於 1 ）
        while(len(inputWord) > 1): # 太長需要重新輸入
            inputWord = input( word + " | INPUT WORD: ") 
        convertDict[word] = inputWord
    return convertDict[word] # 回傳文字

# 檔案清單取得(目前支援：FLAC)
filePathList = []
for targetPattern in [r"*.flac"]: 
    #,r"*.mp3"
    for path in glob.glob(targetPattern):
        filePathList.append(path)
        print(path,"add in list")

# 修改ID3 TAG（增加 SORT 標籤，簡體繁體轉換）
errorFileList = []
for filePath in filePathList:
    try:
        # 原先資料
        tags = mutagen.File(filePath)  
        tag_artist = tags["artist"][0]
        tag_album = tags["album"][0]
        tag_title = tags["title"][0]
        print(tag_artist,tag_album,tag_title)
        
        # 標籤資料定義
        tagToChange = ["artist","album","title"] #作用的原始標籤
        newTagData = {} #定義新寫入的標籤清單
        for tagItem in tagToChange:
            newTagData[tagItem+'sort'] =  checkWord(tags[tagItem][0][0]) + cc.convert(tags[tagItem][0]) #SORT 標籤
            newTagData[tagItem] = cc.convert(tags[tagItem][0]) # 簡繁轉換新名稱
        print(newTagData)

        # 檔案型態套用（副檔名判斷）
        if(".flac" in filePath):
            audio = FLAC(filePath)

        for tag in newTagData.items():
            audio[tag[0]] = tag[1] # 寫入新標籤
        
        audio.pprint()
        audio.save() #檔案寫入
        #-tags = mutagen.File(filePath)
        print("--------------------------------")

    except Exception as e:
        errorFileList.append({filePath:e}) # 錯誤紀錄報告

print("所有資料轉換完成")
if len(errorFileList) > 0: #如果有錯誤會輸出
    print("錯誤清單")
    for item in errorFileList:
        print(item)
    print("--------------------------------")

# 回存文字轉換資料
with open('data.json', 'w') as f:
    json.dump(convertDict, f)