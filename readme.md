
# Trabajo realizado hasta ahora para el TEG. - Gabriel Oliveira

En en el siguiente repo hay varios archivos que he creado con base a la idea principal que tengo para la investigación del TEG y el desarrollo del mismo. 

Importante: todo acá estpa sujeto a cambios y discusión


## Investigación

- En archivo archivo **TEG-GabrielOliveira-BasesTeoricas.docx/pdf** se encuentra toda la investigación que he realizado hasta ahora sobre los distintos temas que toca mi TEG: Crowdsourcing, Bases de datos de grafos y web scrapping. dependiendo de lo que considere puede resumirse y dejar solo lo necesario o dejarse como está.

- Algo importante a destacar es que en la seccion de Bases de datos de grafos, hablo de forma genérica sobre todos los modelos sobre los cuales este tipo de bases de datos pueden implementarse, asi como la representación en memoria en las que se implementa, es decir, hay varios gestores de bases de datos de grafos que las implementan usando un modelo en especifico y una representación en memoria especifica. NEO4j, por ejemplo las implementa en memoria utilizando listas enlazadas con apuntadores directos y su modelo es el Grafo de propiedaddes etiquetadas.

- No se si está de acuerdo, pero en el capitulo 4 deberia de haber una sección en el que hable de NEO4J, y donde explique cuales son las propiedades que cumple, de todo lo investigado, ya que es el SGBD que voy a utilizar y su lenguaje de consultas.

## Desarrollo

- La idea principal que tengo hasta ahora, consiste en un buscador, *buscador.png*, en el cual hay tres campos de búsqueda. El usuario puede escribir el nombre del medicamento o principio activo y mediante auto completado podrá seleccionarlo, además de dos listas desplegables: una para el estado en el cual quiere buscar el medicamento y otra para la ciudad o municipio (si quiere ser mas especifico). 


En lugar del estado y ciudad, la ubicación actual del usuario tambien podría tomarse para hacer la consulta. Por ejemplo, NEO4J tiene un tipo de dato geoespacial para almacenar coordenadas, y permite hacer consultas en las que el mismo calcula la distancia entre pares de coordenadas ordenandolas incluso.

No he experimentado lo suficiente con esto pero si he investigado al respecto, en teoria a NEO4J puedo hacerle una consulta mendiante su lenguaje de consultas del tipo: *de todas las farmacias que tengas almacenadas, dame todas aquellas cercanas a esta coordenada que te estoy pasando*... y el regresa los registros que cumplen la condición, ordenadas desde la más cerca a la mas lejana. Habría que ver como esto puede aprovecharse para la agrupacion de medicamentos, las farmacias deben insertarse con sus coordenadas.

- Esta vista debe tener tambien un boton que despliegue **un modal que le permita a las personas introducir la información de localización de un medicamento en alguna farmacia en la base de datos** ya que la base de todo es que los propios usuarios sean los que generen la inforamción actualizada. La idea es que el usuario pueda seleccionar la farmacia mediante google maps en un radio determinado (si se quiere en forma dinamica) o si solo se quieren demostrar algunos casos, puede generarse un archivo con la información de las farmacias del estado carabobo.

- Esta consulta debería ir a un backend que se conecte a Neo4J (la base de datos de grafos) y regrese los medicamentos relacionados al principio activo y sus farmacias **(farmacias agrupadas por medicamentos)**, como se muestra en *(resultados.png)*. Nada esto está implementado aún.    

### Para lograr eso lo primero que hice fue obtener la data que necesitaba de medicamentos, los siguientes archivos se encuentran en el directorio /scrapping, el proceso se explica a continuación.  

- https://ve.ivademecum.com/medicamentos_page-1.html es un sitio web que expone una base de datos con toda esta información, asi que, utilizando web scrapping y luego de estudiar el sitio, diseñé un pequeño algoritmo en python que utliza beautiful soup (un parseador html que no solo genera las consultas html sino que puede mapear los resultado con las estructuras de datos de python), que se encarga de ir por cada una de las paginas obteniendo esta información de una tabla html, el algotirmo va generando un archivo .json con los datos que creí necesarios recuperar de cada medicamento.

hay 4 scripts numerados y que deben ser ejecutados en orden:

- 1.medicine_bot.py : es el *web cralwer* que, al terminar de ejecutarse, genera un archivo llamado **medical_data.json** el cual contiene un arreglo de JSON (arreglo de objetos de JSON) donde cada objeto es un medicamento obtenido del sitio web. Es legible a simple vista.

*Advertencia: el script anterior tarda más de dos horas en ejecutarse, por la cantidad de peticiones que tienen que hacerse y para evitar que el servidor de origen las bloquee, si se ejecuta y no se termina, se borrará la data que existe incialmente en medical_data.json*

*Ya el archivo medical_data.json esta lleno de datos y sin ejecutar el script anterior, pueden ejecutarse los siguientes*

- 2.describe.py : es un script en el que se recorre el archivo medical_data.json, con el fin de actualizar el mismo archivo, eliminando medicamentos repetidos y sin principío activo, además genera archivos .txt con una lista de todos los principios activos, patologias y acciones terapeuticas. Los archivos se generan en el directorio /files/txt

- 3.indexed.py: es un script que genera un archivo .json para los principios activos y las patologías asociandoles un ID a cada uno, además, genera un nuevo archivo llamado **indexed_medical_data.json** donde se sustituyen las apariciones de los principios activos y patologías por su ID. *Los archivos se generan en el directorio /files/indexed*

- 4.generate.csv : es un script que genera archivos .CSV para todos los datos y sus relaciones entre si. *Los archivos se generan en el directorio /files/csv*

  - un csv para patologias.
  - un csv para principios activos.
  - un csv para medicamentos.
  - un csv para las relaciones entre patologias y medicamentos (relacionados por su ID).
  - un csv para las relaciones entre principios activos y medicamentos (relacionados por su ID).

 estos archivos son la forma de insertar todos esos datos en la base de datos procesándolos por lotes.


***En cuanto pueda y tenga el tiempo, porfa revise estos archivos y me da su opinión para seguir con los capitulos y fases que restan para el TEG, cualquier consideración me será util, y tambien la ayuda que pueda brindarme para redactar el capitulo 4, hasta ahora no se  como empezar a redactarlo o como debo estructurarlo***
