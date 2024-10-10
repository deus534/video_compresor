
path = 'main.py'
print('-----------INICIO ARCHIVO--------------')


#Lee por bloques
TAM_BLOQUE = 1
with open(path, 'rb') as archivo:
    while True:
        byte = archivo.read(TAM_BLOQUE)
        if not byte:
            break
        char = byte.decode('utf-8', errors='replace')
        print(char,end='')




print('-----------FIN ARCHIVO--------------')
