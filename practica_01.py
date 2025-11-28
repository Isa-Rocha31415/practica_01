#Variables librerias globales
from os import read
import re
import pandas as pd
import nltk
import math 
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
        diccionario_vocabulario[diccionario_labels[keys]]=diccionario_vocabulario.get(diccionario_labels[keys],"")+items+" "
    for keys in diccionario_vocabulario:
        diccionario_vocabulario[keys]=diccionario_vocabulario[keys].split()
    return diccionario_vocabulario
def get_frecuencias(diccionario_completo:dict[str,list[str]])->dict[str,dict[str,int]]:
    diccionario_por_topico={}
    for keys,items in diccionario_completo.items():
        diccionario_por_topico[keys]=frecuencias(items)
    return diccionario_por_topico
def frecuencias(palabras:list[str])->dict[str,int]:
    diccionario_frecuencias={}
    for palabra in palabras:
        diccionario_frecuencias[palabra]=diccionario_frecuencias.get(palabra,0)+1
    return diccionario_frecuencias
def sort_frecuencias(diccionario_completo:dict[str,dict[str,int]])->dict[str,list[tuple[int,str]]]:
    diccionario_topico={}
    for keys,items in diccionario_completo.items():
        diccionario_topico[keys]=sorted([(frequency,word) for word,frequency in items.items()],reverse=True)
    return diccionario_topico
def write_txt(diccionario:dict[str,list[tuple[int,str]]],cantidad:int):
    n=cantidad//2
    with open("keywords.txt","w") as f:
        labels=[]
        for keys,items in diccionario.items():
            palabras_mas_frecuente=items[:cantidad]
            i=0
            while(i<n):
                f.write(f"{palabras_mas_frecuente[i][1]} {palabras_mas_frecuente[i+1][1]} {palabras_mas_frecuente[cantidad-1-i][1]} {palabras_mas_frecuente[cantidad-i-2][1]}\n")
                i+=2
                labels.append(keys)
        with open("labels_kw.txt","w",encoding="utf-8") as file:
            for label in labels:
                file.write(f"{label}\n")
"""
Sección 2.3 punto 1 
DEclarion de funciones
"""
def tf(diccionario:dict[int,str],vocabulario:set[str])->dict[int,dict[int,int]]:
    diccionario_tf={}
    #ordenar vocabulario y guardarlo en un diccionario 
    vocab_list=sorted(list(vocabulario))
    diccionario_vocabulario={palabra:idx for idx,palabra in enumerate(vocab_list)}
    #Dividir el string en lista de palabras 
    diccionario_spliteado={indice:concepto.split() for indice,concepto in diccionario.items()}
    #Busca la freceuncia de las palabras del vocabulario en cada conecpto 
    for key,palabras in diccionario_spliteado.items():
        diccionario_frecuencias={}
        for palabra in palabras:
            idx=diccionario_vocabulario[palabra]
            diccionario_frecuencias[idx]=diccionario_frecuencias.get(idx,0)+1 
        diccionario_tf[key]=diccionario_frecuencias
    return diccionario_tf
def idf(diccionario:dict[int,str],vocabulario:set[str])->dict[int,float]:
    diccionario_idf={}
    #ordenar vocabulario y guardarlo en un diccioanrio 
    vocab_list=sorted(list(vocabulario))
    diccionario_vocabulario={palabra:idx for idx,palabra in enumerate(vocab_list)}
    #Dividir el string en lsita d epalabras 
    diccionario_spliteado={indice:concepto.split() for indice,concepto in diccionario.items()}
    n=len(diccionario_spliteado)
    #buscar la frecuencia de cadapalabra por documento, es decir, en cuantos documentos aparacio 
    frecuencias_documento={i:0 for i in range(len(vocab_list))}
    for palabras in diccionario_spliteado.values():
        palabras_unicas=set(palabras)
        for palabra in palabras_unicas:
            idx=diccionario_vocabulario[palabra]
            frecuencias_documento[idx]+=1 
    diccionario_idf={palabra:math.log(n/frecuencia) for palabra,frecuencia in frecuencias_documento.items()}
    return diccionario_idf
    
def getVocabulary(diccionario:dict[int,str])->set[str]:
    diccionario_div={}
    for keys,values in diccionario.items():
        diccionario_div[keys]=values.split()
    conjunto=set()
    for keys,values in diccionario_div.items():
        conjunto=conjunto.union(set(values))
    return conjunto 
def TF_IDF(tf:dict[int,dict[int,int]],idf:dict[int,float])->dict[int,dict[int,float]]:
    TFIDF_d={i:{} for i in tf}
    for documento,frecuencia in tf.items():
        TFIDF_d[documento]={palabra:freq*idf[palabra] for palabra,freq in frecuencia.items() }
    return TFIDF_d 
def norm_l2(vector:dict[int,float])->float:
    return (sum(v**2 for v in vector.values()))**0.5
def vector_normal(vector:dict[int,float])->dict[int,float]:
    norma=norm_l2(vector)
    return {indice:v/norma for indice,v in vector.items()}
def normalizar(tfidf:dict[int,dict[int,float]])->dict[int,dict[int,float]]:
    return {indice:vector_normal(documento) for indice,documento in tfidf.items()}
"""
Seccion 2.3 punto 2 
funciones 
"""
def tfidf_keywords(ruta_keywords:str,vocabulario:set[str],idf:dict[int,float])->dict[int,dict[int,float]]:
    lista_vocabulario=sorted(list(vocabulario))
    diccionario_vocabulario={palabra:idx for idx,palabra in enumerate(lista_vocabulario)}
    vectores={}
    with open(ruta_keywords,"r",encoding="utf-8") as f:
        for idx,linea in enumerate(f):
            palabras=linea.strip().split() 
            tfidf={diccionario_vocabulario[palabra]:idf[diccionario_vocabulario[palabra]] for palabra in palabras}
            tfidf_normalizado=vector_normal(tfidf)
            vectores[idx]=tfidf_normalizado
    return vectores 

"""
Seccion 2.3 punto 3
Funciones 
"""
def similitud_coseno(u1:dict[int,float],u2:dict[int,float])->float:
    keys=set(u1).intersection(set(u2))
    d=sum( u1[k]*u2[k] for k in keys )
    return 1-d 
def tuplas_documentos_coseno(documentos:dict[int,dict[int,float]],tuplas:dict[int,dict[int,float]]):
    distancias_={}
    for tupla,vector2 in tuplas.items():
        distancias={}
        for documento,vector1 in documentos.items():
            d=similitud_coseno(vector1,vector2)
            distancias[documento]=d
        distancias_[tupla]=distancias
    return distancias_
def ordernar_tuplas(distancias_por_tuplas:dict[int,dict[int,float]])->dict[int,list[tuple[float,int]]]:
    guardar_resultado={}
    for tupla,distancias in distancias_por_tuplas.items():
        lista=sorted([(distancia, documento) for documento,distancia in distancias.items() ])
        guardar_resultado[tupla]=lista 
    return guardar_resultado 
"""
Seccion 2.3 punto 4

"""
def escribir(distancias_tuplas:dict[int,list[tuple[float,int]]],cantidad:int):
    with open("labels.txt","r",encoding="utf-8") as file:
        labels_documentos=[f.strip() for f in file]
    with open("labels_kw.txt","r",encoding="utf-8") as file:
        labels_tuplas=[ f.strip() for f in file]
    with open("keywords.txt","r",encoding="utf-8") as file:
        tuplas_texto=[f.strip() for f in file]
    with open("results.txt","w",encoding="utf-8") as file:
        texto=""
        for tupla,distancias in distancias_tuplas.items():
            distancias_cercanas=[documento for _,documento in  distancias[:cantidad]]
            topicos_documento=[labels_documentos[documento] for documento in distancias_cercanas]
            texto=f"{tuplas_texto[tupla]}; {labels_tuplas[tupla]}; {distancias_cercanas}; {topicos_documento}\n"
            file.write(texto)
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
diccionario_topicos=juntar_topicos(diccionario_procesado,diccionario_labels)
diccionario_frecuencias=get_frecuencias(diccionario_topicos)
diccionario_frecuencias_ordenadas=sort_frecuencias(diccionario_frecuencias)
write_txt(diccionario_frecuencias_ordenadas,60)

"""
Sección 2.3 punto 1 
llamada de funciones 
"""
#VOy a utilizar los diccionarios de la svariables 103 y 102
vocabulario=getVocabulary(diccionario_procesado)
diccionario_tf=tf(diccionario_procesado,vocabulario)
diccionario_idf=idf(diccionario_procesado,vocabulario)
diccionario_vectores_TFIDF=TF_IDF(diccionario_tf,diccionario_idf)
diccionario_vectores_TFIDF_normalizado=normalizar(diccionario_vectores_TFIDF)
#print(diccionario_vectores_TFIDF_normalizado)
"""
Sección 2.3 punto 2
llamada de funciones 
"""
matriz_tfidf_tuplas=tfidf_keywords("keywords.txt",vocabulario,diccionario_idf)
print(matriz_tfidf_tuplas)
"""
Seccion 2.3 punto 3
llamadas  
"""
diccionario_tuplas_distancias=tuplas_documentos_coseno(diccionario_vectores_TFIDF_normalizado,matriz_tfidf_tuplas)
diccionario_tuplas_cercanas=ordernar_tuplas(diccionario_tuplas_distancias)
escribir(diccionario_tuplas_cercanas,5)
