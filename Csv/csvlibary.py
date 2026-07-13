#13-07-2026
import requests
import json
import csv
from pathlib import Path
folder_path = "C:/Users/prade/OneDrive/Indexer Drona/School Trial Data/SKSD VIVEKANANDA SCHOOL/CSV/"
files=['schoolbranchacademicfee.csv','Studenttable.csv','studentpayablefee.csv','studentstudyrecord.csv']

for file in files:
    if Path(folder_path + file).is_file():
        print("File Exist")
    else:
        print("File Not Exist")

#read csv file using 
with open(folder_path+files[0],'r') as readcsvfile:
    reader=csv.reader(readcsvfile)
    header=next(reader)
    student_data=[]
    for row in reader:
        student={}
        for data,head in zip(row,header):
            student[head]=data.strip() if data else "Empty" 
        student_data.append(student)
    with open('d:/Github/Remote_Github/Python-Pratice-Project/Csv/'+files[0][:-4]+'.json','w') as jsonfile:
        json.dump(student_data,jsonfile)
        jsonfile.close()

#write csv file using write methods
with open('d:/Github/Remote_Github/Python-Pratice-Project/Csv/'+files[0][:-4]+'.json','r') as readjsonfile:
    students=json.load(readjsonfile)
    headers=list(students[0].keys())
    student_details=[list(student.values()) for student in students]
    with open('d:/Github/Remote_Github/Python-Pratice-Project/Csv/'+files[0],'w') as writecsvfile:
        writer=csv.writer(writecsvfile,delimiter="\t")
        writer.writerow(headers)
        for data in student_details:
            writer.writerow(data)
        #writer.writerows(student_details)

#read csv file using dict method
with open(folder_path+files[1],'r') as readcsvfile:
    reader=csv.DictReader(readcsvfile)
    students=[]
    for student in reader:
        students.append(student)
    with open('d:/Github/Remote_Github/Python-Pratice-Project/Csv/'+files[1][:-4]+'.json','w') as writejsonfile:
        json.dump(students,writejsonfile)

#write csv file using dict method
with open('d:/Github/Remote_Github/Python-Pratice-Project/Csv/'+files[1][:-4]+'.json','r') as readjsonfile:
    reader=json.load(readjsonfile)
    headers=list(reader[0].keys())
    with open('d:/Github/Remote_Github/Python-Pratice-Project/Csv/'+files[1],'w') as writecsvfile:
        writer=csv.DictWriter(writecsvfile,fieldnames=headers)
        writer.writeheader()
        writer.writerows(reader)