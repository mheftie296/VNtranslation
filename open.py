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
            if start != -1: # end of non-blank section of hex data, may be text or code
                # TODO: somehow determine if text is safe to translate
                string = ''
                try:
                    # this next line will error if the hex is not utf-8 text
                    # TODO: remove everything else from the try-catch
                    string = codecs.decode(hexdata[start:i*2], "hex").decode('utf-8').replace("\n", "")
                    if pattern.search(string) != None: # check for Japanese text
                        trnhex = translate(string)
                        #trnhex = re.sub('[^A-Za-z0-9 ]+', '', trnhex)
                        print(trnhex)
                        tr = trnhex.encode("utf-8").hex()
                        size = len(hexdata[start:i*2])
                        if len(tr) > size:
                            print("oops")   #the translation is too long, the file size will change and the game will crash
                            #raise UnboundLocalError()  # do not insert too long translation
                            # TODO: remove existing padding in file for longer translations
                        while(len(tr) < size):
                            tr += '00'
                        hexdata = hexdata[:start] + tr + hexdata[i*2:]
                        print(str(round(((i*2)/len(hexdata))*100,2))+'%')  # percent completed
                        if(round(((i*2)/len(hexdata))*100,2) > 25):   # quit early at 25%
                            break
                        q+=1
                        if(q==4):   # quit early after 4 translations. TODO:remove after fixing game crashes
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