import json 

# 取得輔助字典庫
convertDict = {}
with open('data.json') as f:
    convertDict = json.load(f)

key = input("Key: ")
print("In DB Value:",convertDict[key])
if(input("Change Value? [y/n]") == 'y'):
    convertDict[key] = input("New Value: ")

# 回存文字轉換資料
with open('data.json', 'w') as f:
    json.dump(convertDict, f)