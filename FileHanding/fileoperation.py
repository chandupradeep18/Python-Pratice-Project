#14-07-2026
import requests
import csv
import json
import os
os.chdir('D:/Github/Remote_Github/Python-Pratice-Project/FileHanding/')
#how to read file
f=open('demofile.txt','r')
#print(f.read())
#print(f.readline())
#print(f.readlines())
f.close()
print(f.closed)

with open('demofile.txt','r') as file:
    data=file
    print(data.readable())
    #print(data.readline())
    print(file.tell())
    file.seek(0)
    #print(data.readlines())
    print(file.tell())
    print(f.closed)

#write or create a File
with open('demofiles.txt','w+') as file:
    print(file.writable())
    file.write('Hi every one')
    lines=['1','2','3','4','5','6','9','7','8']
    file.write('\n')
    file.writelines(lines)
    file.seek(0)
    print(file.read())
    file.close()
    print(file.closed)

#append data to file
with open('demofiless.txt','a+') as file:
    print(file.writable())
    #file.write('\n')
    file.write('Hi every one')
    lines=['1','2','3','4','5','6','9','7','8']
    file.write('\n')
    file.writelines(lines)
    print(file.tell())
    file.seek(0)
    print(file.tell())
    print(file.read())