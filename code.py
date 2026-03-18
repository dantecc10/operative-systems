class Archivo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.líneas = []
        try:
            f = open(nombre)
        except:
            print("Error al abrir el archivo.")
        else:
            for línea in f:
                self.líneas.append(línea)
            else:
                print("Ya generamos las líneas.")
        f.close()
            

from os import system
system("ls")