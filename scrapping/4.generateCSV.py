import json
import csv

'''
  Este Script convierte cada set de datos en un archivo CSV preparado para insertarse en la base de datos
  incluyendo los CSV con las relaciones entre los indices
'''

def toCSVMedicines():
  # lista final de medicamentos 
  end_list = []
  # headers 
  headers = ['id','nombre','composicion','descripcion','presentacion',
              "contraindicaciones","precauciones", 
              "dosificacion"]
  end_list.append(headers)



  with open('medical_data.json') as file:
    medical_data = json.load(file)

  # para cada medicamento, se obtienen los campos necesarios para normalizar
  # al medicamento
  for medicine in medical_data:
    row_list = []
    row_list.append(medicine['id'])
    row_list.append(medicine['nombre'])

    if medicine['composicion'] == "":
      row_list.append("none")
    else:
      row_list.append(medicine['composicion'])

    if(medicine['descripcion']) == "":
      row_list.append("none")
    else:
      row_list.append(medicine['descripcion'])

    if medicine['presentacion'] == "":
      row_list.append("none")
    else:
      row_list.append(medicine['presentacion'])

    if medicine["contraindicaciones"] == "":
      row_list.append("none")
    else:
      row_list.append(medicine["contraindicaciones"])

    if medicine["precauciones"] == "":
      row_list.append("none")
    else:
      row_list.append(medicine["precauciones"])  
    
    if medicine["dosificacion"] == "":
      row_list.append("none")
    else:
      row_list.append(medicine["dosificacion"])

    end_list.append(row_list)
     
  # se convierte la lista a csv
  with open('./files/csv/medicines.csv', 'w', encoding='utf-8') as medicalcsv:     
    writer = csv.writer(medicalcsv, delimiter='|')
    writer.writerows(end_list)


def toCSVPathologies():

  final_list = []
  headers = ['id','nombre']  # headers 
  final_list.append(headers)

  with open('./files/indexed/pathologies.json') as file:
   pathologies_list = json.load(file)

  for pathology in pathologies_list:
    row_list = []
    row_list.append(pathology['id'])
    row_list.append(pathology['name'])
    
    final_list.append(row_list)
    
    # se convierte la lista a csv
  with open('./files/csv/pathologies.csv', 'w', encoding='utf-8') as pathologycsv:     
    writer = csv.writer(pathologycsv, delimiter='|')
    writer.writerows(final_list)


def toCSVActiveSusbstance():
  
  final_list = []
  headers = ['id','nombre']  # headers 
  final_list.append(headers)

  with open('./files/indexed/substances.json') as file:
    substances_list = json.load(file)

  for substance in substances_list:
    row_list = []
    row_list.append(substance['id'])
    row_list.append(substance['name'])
    
    final_list.append(row_list)
    
  # se convierte la lista a csv
  with open('./files/csv/substances.csv', 'w', encoding='utf-8') as substancecsv:     
    writer = csv.writer(substancecsv, delimiter='|')
    writer.writerows(final_list)


def toCSVPharmacies():
  final_list = []
  headers = ['lat','lng','id','nombre','ubicacion','rating','direccionCompleta']  # headers 
  final_list.append(headers)

  with open('./files/pharmacies_valencia.json') as file:
    pharmacies_list = json.load(file)

  for pharmacy in pharmacies_list:
    row_list = []
    row_list.append(pharmacy['coordinates']['lat'])
    row_list.append(pharmacy['coordinates']['lng'])
    row_list.append(pharmacy['id'])
    row_list.append(pharmacy['name'])
    row_list.append(pharmacy['location'])
    
    if pharmacy.get('rating'):
      row_list.append(pharmacy['rating'])
    else:
      row_list.append(0)

    row_list.append(pharmacy['completeAddress'])

    final_list.append(row_list)

  # se convierte la lista a csv
  with open('./files/csv/pharmacies_val.csv', 'w', encoding='utf-8') as pharmacycsv:     
    writer = csv.writer(pharmacycsv, delimiter='|')
    writer.writerows(final_list)

def toCSVRelationshipMedicineSusbstance():

  relationship_list = []
  headers = ['id_medicamento','id_principio']  # headers 
  relationship_list.append(headers)

  with open('./files/indexed/indexed_medical_data.json') as file:
    medical_data = json.load(file)

  for medicine in medical_data:
    row_list = []
    row_list.append(medicine['id'])
    row_list.append(medicine['principio_activo'])
    relationship_list.append(row_list)

  # se convierte la lista a csv
  with open('./files/csv/medicine-substance.csv', 'w', encoding='utf-8') as relationshipcsv:     
    writer = csv.writer(relationshipcsv, delimiter='|')
    writer.writerows(relationship_list)


def toCSVRelationshipMedicinePathology():
  relationship_list = []
  headers = ['id_medicamento','id_patologia']  # headers 
  relationship_list.append(headers)

  with open('./files/indexed/indexed_medical_data.json') as file:
    medical_data = json.load(file)

  for medicine in medical_data: 
    pathology_list = medicine['patologia']
    for pathology in pathology_list:
      row_list = []
      row_list.append(medicine['id'])
      row_list.append(pathology)
      relationship_list.append(row_list)
    
  # se convierte la lista a csv
  with open('./files//csv/medicine-pathology.csv', 'w', encoding='utf-8') as relationshipcsv:     
    writer = csv.writer(relationshipcsv, delimiter='|')
    writer.writerows(relationship_list)


def main():
  toCSVMedicines()
  toCSVPathologies()
  toCSVActiveSusbstance()
  toCSVRelationshipMedicineSusbstance()
  toCSVRelationshipMedicinePathology()
  #toCSVPharmacies()

if __name__ == "__main__":
  main()
  
