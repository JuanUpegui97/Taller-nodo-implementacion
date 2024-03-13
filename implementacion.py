

class NodoDoble:

    #Constructor
    def __init__(self,img): 
        self.ligaIzq = None  # Atributo LigaIzq
        self.ligaDer = None  # Atributo LigaDer
        self.img= img  # Atributo img
        
    def asignaimg(self,img):
        self.img= img
    def asignaLigaIzq(self,x): 
        self.ligaIzq = x
    def asignaLigaDer(self,x):
        self.ligaDer = x
    def retornaLigaIzq(self): 
        return self.ligaIzq
    def retornaLigaDer(self): 
        return self.ligaDer
   
class LDL:
      
    def __init__(self): 
        self.primero = None  # Atributo: primer nodo de la lista
        self.ultimo = None  # Atributo: ultimo nodo de la lista

    def agregar_nodo(self, nodo):
        if self.primero is None:
            self.primero = nodo
            self.ultimo = nodo
        else:
            self.ultimo.ligaDer = nodo
            nodo.ligaIzq = self.ultimo
            self.ultimo = nodo


        

    def eliminarMenoresA(self,img): #Elimina todos los nodos cuyo imgsea menos al ingresado
        actual = self.primero
        while actual:
            if actual.img["ancho"] < img["ancho"] or actual.img["alto"] < img["alto"]:
                if actual == self.primero:
                    self.primero = actual.ligaDer
                    if self.primero:
                        self.primero.ligaIzq = None
                elif actual == self.ultimo:
                    self.ultimo = actual.ligaIzq
                    if self.ultimo:
                        self.ultimo.ligaDer = None
                else:
                    actual.ligaIzq.ligaDer = actual.ligaDer
                    actual.ligaDer.ligaIzq = actual.ligaIzq
            actual = actual.ligaDer



from PIL import Image
from easygui import diropenbox
import os
import json

class imageProcess:
    @staticmethod
    def invertir_colores(img_path):
        img = Image.open(img_path)
        img = img.convert("RGB")
        ancho, alto = img.size
        for x in range(ancho):
            for y in range(alto):
                r, g, b = img.getpixel((x, y))
                img.putpixel((x, y), (255-r, 255-g, 255-b))
        return img

    @staticmethod
    def procesar_imagenes(directorio, listas):
        cont_validas = 0
        cont_validas_no = 0
        imagenes_validas = []  # Lista para almacenar las rutas de las imágenes válidas

        for archivo in os.listdir(directorio):
            if archivo.endswith((".jpg", ".jpeg", ".png")):
                ruta_completa = os.path.join(directorio, archivo)
                imagen = Image.open(ruta_completa)
                ancho, alto = imagen.size

                if ancho >= 250 and alto >= 250:  # Verificar tamaño mínimo
                    imagen_invertida = imageProcess.invertir_colores(ruta_completa)
                    imagen_invertida.save(ruta_completa)
                    imagenes_validas.append({
                        "ruta_imagen": ruta_completa,
                        "ancho": ancho,
                        "alto": alto,
                        "status": "invertido"
                    })
                    cont_validas += 1
                else:
                    img_info = {"ancho": ancho, "alto": alto}
                    nodo = NodoDoble(img_info)  # Crear nodo con la información de la imagen
                    listas.agregar_nodo(nodo)   # Agregar nodo a la lista enlazada
                    cont_validas_no += 1

        # Eliminar nodos de la lista enlazada que no cumplen con el tamaño mínimo
        img_min_size = {"ancho": 250, "alto": 250}
        listas.eliminarMenoresA(img_min_size)

        return cont_validas, imagenes_validas, cont_validas_no

    @staticmethod
    def generar_json(imagenes_validas, directorio):
        json_filename = os.path.join(directorio, "imagenes_info.json")
        with open(json_filename, "w") as json_file:
            json.dump(imagenes_validas, json_file, indent=4)
        return json_filename

directorio = diropenbox(msg="Seleccione Archivo", title="Seleccione Archivo")
if directorio:
    listas = LDL()
    cont_validas, imagenes_validas, cont_validas_no = imageProcess.procesar_imagenes(directorio, listas)
    print("Imágenes procesadas y válidas:", cont_validas)
    print("Imágenes Eliminadas:", cont_validas_no)
    json_file = imageProcess.generar_json(imagenes_validas, directorio)
    print(f"JSON creado exitosamente: {json_file}")
else:
    print("No se ha seleccionado ninguna imagen")
