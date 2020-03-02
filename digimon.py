from bs4 import BeautifulSoup
import requests
import json
import csv
import xlsxwriter
import pymongo as mp

url = 'http://digidb.io/digimon-list/'
html = requests.get(url)
a = BeautifulSoup(html.content, 'html.parser')

nama_field = a.find_all('th')
# print(nama_field)

img = []
tbody = a.find('tbody')
tr = tbody.find_all('tr')
t_d = tbody.find_all('td')
for i in tbody.find_all('img'):
    img.append(i['src'])
# print(img)
# td = []
list_data = []
for i in tr:
    tampung = i.find_all('td')
    td=[]
    for j in tampung:
        td.append(j.text.replace('\xa0',''))
    list_data.append(td)

table_field = []
for k in nama_field:
    table_field.append(k.text)
table_field.insert(1, 'Image')
# print(table_field)

for s in range(len(list_data)):
    list_data[s].insert(1, img[s])
# print(list_data)

dict_data = []
for i in list_data:
    asd = dict(zip(table_field, i))
    dict_data.append(asd)

print(dict_data)

#TO EXCEL
book = xlsxwriter.Workbook('digimon.xlsx')
sheet = book.add_worksheet('Sheet 1')
row = 0
for ID, Image, Digimon, Stage, Type, Attribute, Memory, Equip, HP, SP, Atk, Def, Int, Spd in list_data:
    sheet.write(row, 0, 'ID')
    sheet.write(row, 1, 'Image')
    sheet.write(row, 2, 'Digimon')
    sheet.write(row, 3, 'Stage')
    sheet.write(row, 4, 'Type')
    sheet.write(row, 5, 'Attribute')
    sheet.write(row, 6, 'Memory')
    sheet.write(row, 7, 'Equip Slots')
    sheet.write(row, 8, 'HP')
    sheet.write(row, 9, 'SP')
    sheet.write(row, 10, 'Atk')
    sheet.write(row, 11, 'Def')
    sheet.write(row, 12, 'Int')
    sheet.write(row, 13, 'Spd')
row = 1
for ID, Image, Digimon, Stage, Type, Attribute, Memory, Equip, HP, SP, Atk, Def, Int, Spd in list_data:
    sheet.write(row, 0, ID)
    sheet.write(row, 1, Image)
    sheet.write(row, 2, Digimon)
    sheet.write(row, 3, Stage)
    sheet.write(row, 4, Type)
    sheet.write(row, 5, Attribute)
    sheet.write(row, 6, Memory)
    sheet.write(row, 7, Equip)
    sheet.write(row, 8, HP)
    sheet.write(row, 9, SP)
    sheet.write(row, 10, Atk)
    sheet.write(row, 11, Def)
    sheet.write(row, 12, Int)
    sheet.write(row, 13, Spd)
    row += 1
book.close()

#TO JSON
with open('Digimon.json', 'w') as myjson:
    json.dump(dict_data, myjson)

#TO CSV
with open('Digimon.csv', 'a', newline='') as mycsv:
    writer = csv.DictWriter(mycsv, delimiter = ',',fieldnames=table_field)
    writer.writerows(dict_data)

#TO MONGODB
urldb = 'mongodb://localhost:27017'
mongoku = mp.MongoClient(urldb)
mydb = mongoku['digimon'] 
mycolls = mydb['digimon']

mymongo = mycolls.insert_many(dict_data)