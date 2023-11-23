import regex as re
import requests
import codecs
import json

pattern = re.compile(r'([\p{IsHan}\p{IsBopo}\p{IsHira}\p{IsKatakana}]+)', re.UNICODE)

url = "http://127.0.0.1:5000/api/v1/generate"

def translate(str):
    prompt = "Translate the following Japanese visual novel script to English:\nJapanese:\n"
    data = {
        "prompt": prompt + str + "\nEnglish:",
        "temperature": "0.6",
        "top_p": "0.9"
        }
    return requests.post(url, json=data).json()['results'][0]['text']


out = ""

with open('AKBG_Chapter01.book', 'rb') as f:
    hexdata = f.read().hex()
    start = -1
    beforeLen = len(hexdata)
    q=0
    for i in range(len(hexdata)//2):
        if hexdata[i*2:i*2+2] != '00':
            if start == -1:
                start = i*2
        else:
            if start != -1:
                string = ''
                try:
                    string = codecs.decode(hexdata[start:i*2], "hex").decode('utf-8').replace("\n", "")
                    if pattern.search(string) != None:
                        trnhex = translate(string)
                        #trnhex = re.sub('[^A-Za-z0-9 ]+', '', trnhex)
                        print(trnhex)
                        tr = trnhex.encode("utf-8").hex()
                        size = len(hexdata[start:i*2])
                        if len(tr) > size:
                            print("oops")
                            #raise UnboundLocalError()
                        while(len(tr) < size):
                            tr += '00'
                        hexdata = hexdata[:start] + tr + hexdata[i*2:]
                        print(str(round(((i*2)/len(hexdata))*100,2))+'%')
                        if(round(((i*2)/len(hexdata))*100,2) > 25):
                            break
                        q+=1
                        if(q==4):
                            break
                except UnicodeDecodeError:
                    pass
                except UnboundLocalError:
                    pass
                start = -1
    out = hexdata

print("before:" + str(beforeLen))
print("after:" + str(len(out)))
with open('translation.book', 'wb') as hi:
    hi.write(bytes.fromhex(out))