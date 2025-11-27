#Variables librerias globales
from os import read
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
nltk.download("stopwords")
data_path="data.txt"
stop_words=set(stopwords.words("spanish"))
"""
Funciones de limpieza de datos
Seccion 2.2 punto 1
"""
def read_data(data_path:str)->dict[int,str]:
    dicc={}
    with open(data_path,"r",encoding="utf-8") as f:
        for idx,line in enumerate(f):
            dicc[idx]=line.strip()
    return dicc
def extraer_alfabeticos(diccionario:dict[int,str])->dict[int,list[str]]:
    diccionario_filtrado={}
    for document in diccionario:
        diccionario_filtrado[document]=re.findall(r'[a-záéíóúñ]+',diccionario[document].lower())
    return diccionario_filtrado
def remover_acentos_string(palabra:str)->str:
    return palabra.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
def quitar_acentos(diccionario:dict[int,list[str]])->dict[int,list[str]]:
    diccionario_sin_acentos={}
    for documento in diccionario:
        diccionario_sin_acentos[documento]=[remover_acentos_string(palabra) for palabra in diccionario[documento]]
    return diccionario_sin_acentos
def remover_palabras_vacias(diccionario:dict[int,list[str]],stop_words:set[str])->dict[int,list[str]]:
    diccionario_filtrado={}
    for documento in diccionario:
        diccionario_filtrado[documento]=[palabra for palabra in diccionario[documento] if palabra not in stop_words and
                                                                                                2<len(palabra)<21]
    return diccionario_filtrado 
def guardar_resultado(diccionario:dict[int,list[str]],nombre:str):
    with open(nombre,"w",encoding="utf-8") as file:
        for elementos in diccionario.values():
            file.write(f"{" ".join(elementos)}\n")
"""
Seccion 2.2 punto 2
"""
######################################
def juntar_topicos(diccionario:dict[int,str],diccionario_labels:dict[int,str])->dict[str,list[str]]:
    diccionario_vocabulario={}
    for keys,items in diccionario.items():
        diccionario_vocabulario[diccionario_labels[keys]]=diccionario_vocabulario.get(diccionario_labels[keys],"")+items
    for keys in diccionario_vocabulario:
        diccionario_vocabulario[keys]=diccionario_vocabulario[keys].split()
    return diccionario_vocabulario
def get_frecuencias(diccionario_completo:dict[str,list[str]])->dict[str,dict[str,int]]:
    diccionario_por_topico={}
    for keys,items in diccionario_completo.items():
        diccionario_frecuencias={}
        for palabra in items:
            diccionario_frecuencias[palabra]=diccionario_frecuencias.get(palabra,0)+1
        diccionario_por_topico[keys]=diccionario_frecuencias
    return diccionario_por_topico
def sort_frecuencias(diccionario_completo:dict[str,dict[str,int]])->dict[str,list[tuple[int,str]]]:
    diccionario_topico={}
    for keys,items in diccionario_completo.items():
        diccionario_topico[keys]=sorted([(frequency,word) for word,frequency in items.items()],reverse=True)
    return diccionario_topico
def write_txt(diccionario:dict[str,list[tuple[int,str]]],cantidad:int):
    n=cantidad//2
    with open("keywords.txt","w") as f:
        for keys,items in diccionario.items():
            palabras_mas_frecuente=items[:cantidad]
            print(palabras_mas_frecuente)
            i=0
            while(i<n):
                f.write(f"{palabras_mas_frecuente[i]} {palabras_mas_frecuente[i+1]} {palabras_mas_frecuente[cantidad-1-i]} {palabras_mas_frecuente[cantidad-i-2]}\n")
                i+=2
        
"""
Seccion 2.2 punto 1
Llamada de funciones de limpieza de datos
"""
documentos=read_data(data_path)
 
documentos_limpios=extraer_alfabeticos(documentos)
documento_sin_palabras_vacias=remover_palabras_vacias(documentos_limpios,stop_words)
documentos_sin_acentos=quitar_acentos(documento_sin_palabras_vacias)
guardar_resultado(documentos_sin_acentos,"data_processed.txt")
"""
2.2 punto 2
"""
data_processed="data_processed.txt"
labels="labels.txt"
diccionario_procesado=read_data(data_processed)
diccionario_labels=read_data(labels)
diccionario_labels={idx:items for idx,items in diccionario_labels.items() }
diccionario_topicos=juntar_topicos(diccionario_procesado,diccionario_labels)
diccionario_frecuencias=get_frecuencias(diccionario_topicos)
diccionario_frecuencias_ordenadas=sort_frecuencias(diccionario_frecuencias)
write_txt(diccionario_frecuencias_ordenadas,60)
