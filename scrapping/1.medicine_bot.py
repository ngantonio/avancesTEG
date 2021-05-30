from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from pprint import pprint
import ssl
from time import sleep
from pprint import pprint
import json
import random

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

NUMBER_OF_PAGES = 164

# Recorrido de la tabla....
def medical(file):

  array_data = []

  med_id = 00000
  anterior_name = ''

  # el sitio web tiene para el momento 164 paginas de medicamentos, por cada pagina:
  #147 #138
  for k in range(1,NUMBER_OF_PAGES):
    sleep(random.randint(1, 3))

    # se construye la url de forma dinamica con el numero de pagina
    url = 'https://ve.ivademecum.com/medicamentos_page-'+ str(k)+'.html' 
    print("\nPAGINA: ",k, "\n")

    # se hace el request y se parsea con beautiful soup
    req =  Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page,'html.parser')

    # de todo el sitio web. me interesa solo obtener la tabla de medicamentos
    body = soup.find('table')

    # de esa tabla, obtengo el tr y el th (los headers) que representan las columnas
    rows = body.findAll("tr")[1:]
    headers = {}
    thead = soup.findAll("th")


    # para poder acceder a los datos se debe recorrer el objeto que devuelve BeautifulSoup
    for row in rows:

      # en cells, obtengo una columna de la tabla, que contiene los datos de un medicamento
      # cells contiene: (codigo (p0), medicamento(p1), accion terapeutica(p2), laboratorio (p3))
      cells= row.find_all("td")

      '''
        Este fragmento se construyó en base a prueba y error, pueden ocurrir casos en los que 
        una fila tenga un medicamento sin principio activo:
      ''' 
      if cells[1].text == "" or cells[2].text == "":
        continue                      #siguiente iteración
      
      # cada nombre de medicamento es a su vez un link que lleva a una pagina que tiene su información
      # aca se obtiene ese link.
      if cells[1].find('a'):
        link = cells[1].find('a').get('href')
        #if link == "https://ve.ivademecum.com/medicamento-gel-lubricante-calox-cod-B5C9F1AB7858C37D":
        #  continue
        
        # se invoca a exploreMedicinePage() que regresa un diccionario con los datos del medicamento actual
        dic = exploreMedicinePage(link,med_id)
        # se incrementa el indice del medicamento
        med_id = med_id+1

        array_data.append(dic)
        #json.dump(dic, file, indent=4,ensure_ascii=False)
        #file.write(", \n")
        print(dic)

  return array_data

    

def exploreMedicinePage(url,med_id):
  sleep(random.randint(1, 3))
  # se requiere hacer otra petición a la pagina que contiene la información completa del medicamento
  req =  Request(url, headers={'User-Agent': 'Mozilla/5.0'})
  page = urlopen(req).read()
  soup = BeautifulSoup(page,'html.parser')

  # Se obtiene el body de la pagina
  body = soup.find('body')

  # la data que se requiere se encuentra en varios elementos div con la clase panel-panel-default
  panels = body.find_all('div', class_="panel panel-default")
  # pprint(panels)

  # se declaran las variables de los datos que interesa obtener
  principio = ""
  accionT = ""
  composicion = ""
  presentacion = ""
  descripcion  = ""
  precauciones = ""
  contraindicaciones = ""
  dosificacion = ""
  reacciones = ""

  # se obtiene el nombre del medicamento
  name = body.find('h1').get_text()

  # for para iterar por todos los panel-default (elemento padre)
  tam = len(panels)

  for i in range(0, tam):
    '''
      muchos de los medicamentos presentan una estructura inconsistente en sus paginas, pero aun asi, manejable.
      para construir los siguientes casos, se estudió previamente el sitio web:
    '''

    # Panel 1: panel de descripcion, donde estan el principio activo y la acction Terapeutica
    if i == 0:
      # Las etiquetas strong contienen el titulo "principio activo" o "accion terapeutica"
      # si hay dos etiquetas, quiere decir que el medicamento tiene definidos ambos datos
      # si solo tiene una, es porque no tiene definido el principio activo
      array_strongs = panels[0].find_all('div', class_="panel-body")[0].find_all('strong')

      
      if len(array_strongs) == 2:
        principio = panels[0].find_all('div', class_="panel-body")[0].find_all('a')[0].get_text()

        # puede darse el caso de que tenga mas de un principio activo, en ese caso hay mas de una etiqueta a dentro
        array_tags_a = panels[0].find_all('div', class_="panel-body")[0].find_all('a')

        #######################################################

        # si tiene mas de un principio activo solo se toma el primero de ellos
        if len(array_tags_a) > 2:
          #pprint(panels[0].find_all('div', class_="panel-body")[0].find_all('a'))
          accionT = panels[0].find_all('div', class_="panel-body")[0].find_all('a')[len(array_tags_a)-1].get_text()      
        else:
          accionT = panels[0].find_all('div', class_="panel-body")[0].find_all('a')[1].get_text()
        ################################################
      else:
        accionT = panels[0].find_all('div', class_="panel-body")[0].find_all('a')[0].get_text()
    
    else:
      # En el resto de paneles se encuentran los otros datos del medicamento:

      # Se obtienen los titulos y se accede a ellos en caso de que esten definidos en el sitio (existan)
      title = panels[i].find_all('div', class_="panel-heading")[0].find('h3').get_text()

      if title == "Composición":
        composicion = panels[i].find_all('div', class_="panel-body")[0].get_text()
      if title == "Presentación":
        presentacion = panels[i].find_all('div', class_="panel-body")[0].get_text()
      if title == "Indicaciones":
        descripcion = panels[i].find_all('div', class_="panel-body")[0].get_text()
      if title == "Precauciones":
        precauciones = panels[i].find_all('div', class_="panel-body")[0].get_text()
      if title == "Contraindicaciones":
        contraindicaciones = panels[i].find_all('div', class_="panel-body")[0].get_text()
      if title == "Dosificación":
        dosificacion = panels[i].find_all('div', class_="panel-body")[0].get_text()
      if title == "Reacciones Adversas":
        reacciones = panels[i].find_all('div', class_="panel-body")[0].get_text()


  # Existe un div que contiene una serie de tags con el nombre de las patologias que ataca el medicamento
  patology_divs = body.find('div', class_= "panel panel-primary")
  #print(patology_divs)
  pathology = []

  # si existen, se recorren los tags y se extrae el nombre de la patologia
  # almacenandolos en un arreglo

  if patology_divs:
    patology_tags = patology_divs.find_all('a')  
    for i in range(0,len(patology_tags)):
      pathology.append(patology_divs.find_all('a')[i].get_text())
  else:
    # caso especifico con ese medicamento que rompe el algoritmo
    if name == "FARMORUBICIN":
      pathology.append('Cáncer')

  # se crea un diccionario para almacenar todos los campos 
  dicti = {}
  # se parsean los strings obtenidos para evitar que se cuele el caracter \n
  descripcion = descripcion.replace('\n','')
  composicion = composicion.replace('\n', '')
  presentacion = presentacion.replace('\n', '')
  contraindicaciones = contraindicaciones.replace('\n', '')
  reacciones = reacciones.replace('\n', '')
  dosificacion = dosificacion.replace('\n', '')
  precauciones = precauciones.replace('\n', '')

  dicti.update({"nombre": name})
  dicti.update({"principio_activo": principio})
  dicti.update({"accion_terapeutica": accionT})
  dicti.update({"composicion": composicion})
  dicti.update({"descripcion": descripcion})
  dicti.update({"presentacion": presentacion})
  dicti.update({"contraindicaciones": contraindicaciones})
  dicti.update({"patologia": pathology})
  dicti.update({'precauciones':precauciones})
  dicti.update({'dosificacion':dosificacion})
  dicti.update({"reacciones_adversas": reacciones})
  dicti.update({"id":med_id})
  #pprint(dicti)
  
  return dicti


if __name__ == "__main__":
  file = open('medical_data.json', 'w')
  array_data = medical(file)
  # se vacia en formato json en un archivo
  json.dump(array_data, file, indent=4,ensure_ascii=False)

