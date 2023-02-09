# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 13:36:05 2023

@author: Gabriela
"""
import nltk
from nltk.tokenize import wordpunct_tokenize
from nltk.tokenize import WhitespaceTokenizer


"Def comandos de una letra"
#simple_commands={"M":"to move forward","R":"to turn right","C":"to drop a chip", "B":"to place a balloon","c":"to pickup a chip","b":"to grab a balloon", "P":"to pop a balloon"}
#simple_commands_keys=simple_commands.keys()
"Comandos simples con parametros"
simple_comands_withPa={"J":"to jump forward n steps. It may jump over obstacles, but the final positionshould not have an obstacle","G":"to go to position (x,y). Position (x,y) should not have an obstacle."}
simple_comands_withPa_keys=simple_comands_withPa.keys()
"Simbolos y palabras importantes"
keyW={"VARS":"declaracion de variables", "PROCS":"procedure declaration", "[": "open procedure definition", ";":"semicolon","]":"close procedure definition", "ROBOT_R":"Inicialización","|":"The parameters are specified by a list of names separated by commas preceded and followed by the symbol", "[|":"procedure definitions and parameters"}
keyW_keys=keyW.keys()
"comandos de un parametro"
"comandos que son palabras con 2 parametros"
complex_commands={"move":"mover","turn":"voltear","face":"face"}
complex_commands_keys=complex_commands.keys()
complex_commands_2={"assignTo": "assign the value of the number to the variable","goTo":"The robot should go to position (x, y)", "put":"The Robot should put n X’s","pick":"The robot should pick n X’s.","moveToThe":"The robot should move n positions to the front, to the left, the right or back and end up facing the same direction as it started","moveInDir":"The robot should face O and then move n steps","jumpToThe:":"jump to the point", "jumpInDir:":"jump in dir","nop":" The robot does not do anything"}
complex_commands_2_keys=complex_commands_2.keys()
"control structure"
contrl_str=["if","then","else","while","repeat"]
"conditions"
conditions=["facing","canPut","canPick","canMoveInDir","canJumpInDir","canMoveToThe","canJumpToThe","not"]
"INICIALIZADOR"
inicializador="ROBOT_R"
otros=[",",":",]
objetos=["chips","balloons",]  ###QUE ES PUTCB
direcciones=["north", "south", "east","west"] 
orientaciones=["front","right", "left", "back"]

variables={}
funiones_creadas={}

"lista con todas las listas anteriores"
lista=[simple_comands_withPa_keys,keyW_keys,complex_commands_2_keys,complex_commands_keys,contrl_str,conditions,otros,direcciones,objetos, variables]
listaGrande=[]

for i in lista:
    for j in i:
        listaGrande.append(j)
        

def cargarArchivo(Archivo):
    archivo=open(Archivo)
    archivo=archivo.read()
    return archivo
    
    
def generar_tokens(archivo):
    tokens=wordpunct_tokenize(archivo)
    for i in range(len(tokens)):
        if tokens[i]=="[|":
            tokens[i]="|"
            tokens.insert(i,"[")
            


    return tokens
    

def guaradar_variables(tokens):
    for i in range(len(tokens)):
        if tokens[i]=="VARS":
            for j in range(1,10):
                if tokens[i+j]!=";":
                    if  tokens[i+j]!=",":
                        variables[tokens[i+j]]=None
                else:
                    break
        if tokens[i]=="PROCS":
            break
def guardar_funciones(tokens):
    for i in range(len(tokens)-1):
        if tokens[i]  not in listaGrande and (tokens[i+1]=="["):
            funiones_creadas[tokens[i]]=None
            
def contar_corechetes(tokens):
    abrir=0
    cerrar=0
    rta=True
    for i in tokens:
        if i=="[":
            abrir+=1
        elif i=="]":
            cerrar+=1
        if abrir != cerrar:
            rta=False
        return rta  
def contar_parentesis(tokens):
    abrir=0
    cerrar=0
    rta=True
    for i in tokens:
        if i=="(":
            abrir+=1
        elif i==")":
            cerrar+=1
        if abrir != cerrar:
            rta=False
        return rta  
def contar_palos(tokens):
    cont=0
    rta=True
    for i in tokens:
        if i=="|":
           
            cont+=1
   
    if (cont%2) !=0:
        rta=False
    return rta
def inializacion(tokens):
    correcto=True
    if tokens[0]!="ROBOT_R":
        correcto=False
    if tokens[1]!="VARS":   
        correcto=False
    for i in range(len(tokens)):
        if tokens[i]=="PROCS":
            if tokens[i-1]!=";":
                correcto=False
    return correcto
def verificar_funciones(tokens):
    correcto=True
    encontro=False
    for i in(range(len(tokens))):
        if tokens[i] in funiones_creadas:
            if tokens[i+1]!="[" and tokens[i+2]!="|":
                correcto=False
                break
            if tokens[i+2]=="|":
                for j in range(1,10):
                    if tokens[i+j]=="|":
                        encontro=True
                        poscion_palito=i+j
                        
                      
        if tokens[i]=="]":
            break
            
    if encontro==False:
        correcto==False
    for i in range(poscion_palito, len(tokens)):
        if tokens[poscion_palito+1] not in complex_commands or tokens[poscion_palito+1] not in complex_commands_2:
            correcto=False
            verificar_commands(tokens,poscion_palito+1)
    return correcto
                    
def verificar_commands(tokens, posicion):
    correcto=True
    if tokens[posicion+1]==":":
        if tokens[posicion] =="assignTo":
                variables[tokens[posicion+4]]=tokens[posicion+2]
                if [tokens[posicion+5]]!=";":
                    correcto=False

        elif tokens[posicion] =="turn":
            if tokens[posicion]+1 not in orientaciones:
                correcto=False
                
        elif tokens[posicion] =="move":
            if tokens[posicion]+1 not in variables and (tokens[posicion]+1).isdigit()==False :
                correcto=False
                print(correcto)


    else:
        correcto:False
    return correcto
        



           
            
            
 
        
archivo=cargarArchivo("robot_prueba.txt")
tokens=generar_tokens(archivo)
print(tokens)
print("----------")
guaradar_variables(tokens)
guardar_funciones(tokens)
#print(contar_corechetes(tokens), contar_parentesis(tokens), contar_palos(tokens))
verificar_funciones(tokens)
print(variables)