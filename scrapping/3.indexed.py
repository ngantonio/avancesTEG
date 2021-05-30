import json

"""
  Este script indexa cada set de datos: medicamentos, principios activos, patologias
  y al mismo tiempo construye un nuevo set de datos de medicamento sustituyendo los principios activos 
  y patologias por sus respectivos indices
"""

def indexed_medicines():
  
  index_medicine = 100000
  with open('medical_data_1.json') as file:
    medical_data = json.load(file)

  file = open('indexed_medical_data.json', 'w')

  indexed_medical_data = []

  #print(type(medical_data[0]))

  for medicine in medical_data:
    medicine.update({"id": index_medicine})
    index_medicine = index_medicine+1
    indexed_medical_data.append(medicine)
 
  json.dump(indexed_medical_data, file, indent=4,ensure_ascii=False)
  #file.write(", \n")


def indexActiveSubstance():

  index_substances = 20000
  dic = {}
  list_dic = []
  file = open('./files/indexed/substances.json', 'w')
  substances = open('./files/txt/all_substances.txt')
  
  for line in substances:
    dic = {}
    line = line.replace('\n', '')
    dic.update({"id":index_substances})
    dic.update({"name":line})
    list_dic.append(dic)
    index_substances = index_substances+1

  json.dump(list_dic, file, indent=4,ensure_ascii=False)


def indexPathologies():

  index_path = 30000
  dic = {}
  list_dic = []
  file = open('./files/indexed/pathologies.json', 'w')
  substances = open('./files/txt/all_pathologies.txt')
  
  for line in substances:
    dic = {}
    line = line.replace('\n', '')
    dic.update({"id":index_path})
    dic.update({"name":line})
    list_dic.append(dic)
    index_path = index_path+1

  json.dump(list_dic, file, indent=4,ensure_ascii=False)


def sustituteSubstancesForIndex():

  list_medicines = []

  with open('./medical_data.json') as file_medical:
    medical_data = json.load(file_medical)

  with open('./files/indexed/substances.json') as file_substances:
    substances = json.load(file_substances)

  file = open('./files/indexed/indexed_medical_data.json', 'w')

  for substance in substances:
    for medicine in medical_data:
      if substance['name'] == medicine['principio_activo']:
        medicine['principio_activo'] =  substance['id']
        list_medicines.append(medicine)

  json.dump(list_medicines, file, indent=4,ensure_ascii=False)


def sustitutePathologiesForIndex():

  new_medical_data = []
 
  with open('./files/indexed/indexed_medical_data.json') as file_medical:
    medical_data = json.load(file_medical)
  
  with open('./files/indexed/pathologies.json') as file_substances:
    json_pathologies = json.load(file_substances)
  
  file = open('./files/indexed_medical_data.json', 'w')

  for medicine in medical_data:
    pathologies_list = medicine['patologia']
    new_pathologies_list = []

    for path in pathologies_list:

      for jsonpath in json_pathologies:

        if path == jsonpath['name']:
          new_pathologies_list.append(jsonpath['id'])
          break

      medicine['patologia']= new_pathologies_list
    new_medical_data.append(medicine)

  json.dump(new_medical_data,file, indent=4,ensure_ascii=False)

def main():
  indexActiveSubstance()
  indexPathologies()
  sustituteSubstancesForIndex()
  sustitutePathologiesForIndex()

if __name__ == "__main__":
  main()