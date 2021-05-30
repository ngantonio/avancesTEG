import json 

# Se eliminan los medicamentos repetidos de medical_data
def removeRepeatedMedicines():

  with open('medical_data.json') as file:
    medical_data = json.load(file)
  
  print("\nSe recuperaron "+str(len(medical_data))+ " medicamentos \n")

  anterior_name = ''
  non_repeated_medicines = []
  count = 0

  for medicine in medical_data:
    if(medicine['nombre'] == anterior_name):
      count = count+1
    else:
      non_repeated_medicines.append(medicine)
    anterior_name = medicine['nombre']

  file = open('medical_data.json', 'w')
  json.dump(non_repeated_medicines, file, indent=4,ensure_ascii=False)
  print("Se elminaron " + str(count) + " medicamentos repetidos")


# Se eliminan las medicinas sin principio activo de medical_data
def removeMedicinesWithoutSubstances():

  with open('medical_data.json') as file:
    medical_data = json.load(file)

  count = 0
  medicines_with_substances = []

  for medicine in medical_data:
    substance = medicine['principio_activo']

    # voy agrupando todas las medicinas que si tienen principio activo
    if substance != "":
      medicines_with_substances.append(medicine)
    else:
      count = count+1

  # sutituyo el archivo con el nuevo arreglo de JSON de medicamentos con principios activos
  file = open('medical_data.json', 'w')
  json.dump(medicines_with_substances, file, indent=4,ensure_ascii=False)
  print("Se eliminaron " + str(count)+ " medicamentos sin principio activo")


# Se eliminan los medicamentos sin patologia de medical_data
def removeMedicinesWithoutPathologies():

  with open('medical_data.json') as file:
    medical_data = json.load(file)
    count = 0

  medicines_with_pathologies = []

  for medicine in medical_data:
    pathologies = medicine['patologia']   

   # voy agrupando todas las medicinas que si tienen patologias
    if len(pathologies) != 0:
      medicines_with_pathologies.append(medicine)
    else:
      count = count+1

  # sutituyo el archivo con el nuevo arreglo de JSON de medicamentos con patologias
  file = open('medical_data.json', 'w')
  json.dump(medicines_with_pathologies, file, indent=4,ensure_ascii=False)
  print("Se elminaron " + str(count)+ " medicamentos sin patologias")



# Genera un archivo .txt con una lista con las patologias encontradas en la data de medicamentos
def getAllPathologies(medical_data):

  file_patholgies = open("./files/txt/all_pathologies.txt", 'w')
  list_pathologies = []

  for medicine in medical_data:
    pathologies = medicine['patologia']   
    
    for path in pathologies:
      if path not in list_pathologies:
        list_pathologies.append(path)
        file_patholgies.write(path+"\n")
 
  print("Hay " + str(len(list_pathologies))+ " Patologias ")

# Genera un archivo .txt con una lista con los principios activos encontrados en la data de medicamentos
def getAllSubstances(medical_data):

  substances = open("./files/txt/all_substances.txt", 'w')
  list_substances = []

  for medicine in medical_data:
    active = medicine['principio_activo']
    if active != "":
      if active not in list_substances:
        list_substances.append(active)
        substances.write(active+"\n")
  
  print("Hay " + str(len(list_substances))+ " Principios activos")
  
# Genera un archivo .txt con las acciones terapeuticas encontradas en la data de medicamentos
def getAllTherapeuticAction(medical_data):

  file_therapeutic_action = open("./files/txt/therapeutic_actions.txt", 'w')
  list_therapeutic_actions = []

  for medicine in medical_data:
    therapeutic_action = medicine['accion_terapeutica']   
   
    if therapeutic_action != "":
      if therapeutic_action not in list_therapeutic_actions:
        list_therapeutic_actions.append(therapeutic_action)
        file_therapeutic_action.write(therapeutic_action+"\n")
  
  print("Hay " + str(len(list_therapeutic_actions))+ " Acciones terapeuticas ")




def main():

  removeRepeatedMedicines()
  removeMedicinesWithoutSubstances()
  removeMedicinesWithoutPathologies()

  with open('medical_data.json') as file:
    medical_data = json.load(file)

  getAllSubstances(medical_data)
  getAllPathologies(medical_data)
  getAllTherapeuticAction(medical_data)

  print("\nLuego de la limpieza se tienen "+str(len(medical_data))+ " medicamentos \n")

  


if __name__ == "__main__":
  main()