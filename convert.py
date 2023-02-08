# load the libraries that we'll use  
from mutagen.mp3 import MP3  
from mutagen.easyid3 import EasyID3  
import mutagen.id3  
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER  
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
import glob  
import json 

# 取得輔助字典庫
convertDict = {}
with open('data.json') as f:
    convertDict = json.load(f)

# 確認首文字對應英文
def checkWord(word):
  if word not in convertDict:
    convertDict[word] = input( word + " | INPUT WORD: ")
  return convertDict[word]

# 檔案清單取得(FLAC MP3)
fileList = []
for targetPattern in [r"*.flrc",r"*.mp3"]:
    fileList.append(glob.glob(targetPattern))

# 修改ID3 TAG
for fileName in fileList:
    # 原先資料
    tags = mutagen.File(fileName)  
    tag_artist = tags["artist"][0]
    tag_album = tags["album"][0]
    tag_title = tags["title"][0]
    print(tag_artist,tag_album,tag_title)
    # SORT 標籤資料定義
    artistsort = checkWord(tag_artist[0]) + tag_artist
    albumsort = checkWord(tag_album[0]) + tag_album
    titlesort = checkWord(tag_title[0]) + tag_title
    print(artistsort,albumsort,titlesort)
    # 檔案型態套用
    if(".flac" in fileName):
        audio = FLAC(fileName)
    if(".mp3" in fileName):
        audio = MP3(fileName)
    # 修改標籤
    audio["artistsort"] = artistsort
    audio["albumsort"] = albumsort
    audio["titlesort"] = titlesort
    audio.pprint()
    audio.save() 
    tags = mutagen.File(fileName)
    print("--------------------------------")
print("所有資料轉換完成")

# 回存文字轉換資料
with open('data.json', 'w') as f:
    json.dump(convertDict, f)