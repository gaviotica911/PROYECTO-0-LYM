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
#simple_comands_withPa={"J":"to jump forward n steps. It may jump over obstacles, but the final positionshould not have an obstacle","G":"to go to position (x,y). Position (x,y) should not have an obstacle."}
#simple_comands_withPa_keys=simple_comands_withPa.keys()
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
objetos=["Chips","Balloons",]  ###QUE ES PUTCB
direcciones=["north", "south", "east","west"] 
orientaciones=["front","right", "left", "back"]

variables={}
funiones_creadas={}

"lista con todas las listas anteriores"
lista=[keyW_keys,complex_commands_2_keys,complex_commands_keys,contrl_str,conditions,otros,direcciones,objetos, variables]
listaGrande=[]

for i in lista:
    for j in i:
        listaGrande.append(j)
        
#Función para cargar el archivo.

def cargarArchivo(Archivo):
    archivo=open(Archivo)
    archivo=archivo.read()
    return archivo
    
#Función que dado un ejemplo, lo divide en tokens.
   
def generar_tokens(archivo):
    tokens=wordpunct_tokenize(archivo)
    return tokens
    
#Función para guardar las variables.

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

#Función para guardar las funciones.

def guardar_funciones(tokens):
    for i in range(len(tokens)-1):
        if tokens[i]  not in listaGrande and (tokens[i+1]=="[") and tokens[i].isdigit()==False:
            funiones_creadas[tokens[i]]=None

#Función para contar los corchetes del programa. 
          
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

#Función para contar los parentesis del programa.

def contar_palos(tokens):
    cont=0
    rta=True
    for i in tokens:
        if i=="|":
           
            cont+=1
    
    if (cont%2) !=0:
        rta=False
    
    return rta

#Función para verificar el esqueleto de inicio del programa.

def inializacion(tokens):
    correcto=True
    if tokens[0]!="ROBOT_R":
        correcto=False
    if tokens[1]!="VARS":
        for i in range(len(tokens)):
            if tokens[i]=="PROCS":
                if tokens[i-1]!="ROBOT_R" :
                    correcto=False
    else:
        for i in range(len(tokens)):
            if tokens[i]=="PROCS":
                encontro=False
            
    if encontro==False:
        correcto==False

    return correcto

#Función para verificar las funciones.

def verificar_funciones(tokens,posicion):
    correcto=True
    encontro=False
    poscion_palito=0
    if tokens[posicion+1]!="[" and tokens[posicion+2]!="|" :
        correcto=False
    if tokens[posicion+2]=="|":
        for j in range(1,10):
            if tokens[posicion+j]=="|":
                encontro=True
                poscion_palito= posicion+j                                
            if encontro==False:
                correcto==False
            if correcto:
                if (tokens[poscion_palito+1]  in complex_commands ) or tokens[poscion_palito+1] in complex_commands_2 :
                    verificar= verificar_commands(tokens,poscion_palito+1)
                    if verificar ==False:
                        correcto=False
                            
    return correcto

#Función para verificar la estructura de los comandos, como lo son los parametros.
                    
def verificar_commands(tokens, posicion):
    correcto=True
    if tokens[posicion+1]==":":
        if tokens[posicion] =="assignTo":
                if tokens[posicion+2].isdigit()==False:
                    correcto=False
                else:
                    variables[tokens[posicion+4]]=tokens[posicion+2]
                if tokens[posicion+5]!=";":
                    correcto=False  
        elif tokens[posicion] =="turn":
            if tokens[posicion+2] not in orientaciones:
                correcto=False
        elif tokens[posicion] =="move":
            if tokens[posicion+2] not in variables and (tokens[posicion+2]).isdigit()==False :
                correcto=False
        elif tokens[posicion] =="face" or tokens[posicion] =="facing":
            if tokens[posicion+2] not in direcciones:
                correcto=False
        elif tokens[posicion] == "put" or tokens[posicion] == "pick" or tokens[posicion] == "canPut" or tokens[posicion] == "canPick":
            if (tokens [posicion + 2]).isdigit() == False and tokens[posicion  +4 ] not in objetos:
                correcto = False
        elif tokens[posicion] == "moveToThe" or tokens[posicion] == "jumpToThe" or tokens[posicion] == "canMoveToThe" or tokens[posicion] == "canJumpToThe":
            if (tokens [posicion + 2]).isdigit() == False and tokens[ posicion +4 ] not in orientaciones:
                correcto = False
        elif tokens[posicion] == "moveInDir" or tokens[posicion] == "jumpInDir" or tokens[posicion] == "canMoveInDir" or tokens[posicion] == "canJumpInDir":
            x=(tokens [posicion + 2]).isdigit()
            #print(tokens[posicion], (tokens [posicion + 2]),tokens[ posicion +4 ] ,x)
            if  x== False: 
                correcto = False
            if tokens[ posicion +4 ] not in direcciones:
                 correcto = False
            #print(correcto)
        elif tokens[posicion] == "not":
                if tokens[posicion + 2] not in conditions:
                    correcto = False
        elif tokens[posicion] == "nop":
            if tokens[posicion + 2] != "":
                correcto = False

    else:
        correcto:False
    
    return correcto


#Función para verificar la estructura de los condicionales if.

def verficicar_condicional(tokens,posicion):
    correcto=True
    if tokens[posicion+1]!=":":
        correcto=False
    if tokens[posicion+2] in conditions: 
        vc=verificar_commands(tokens,(posicion+2))
        if vc==False:
            correcto=False
    else:
        correcto=False
    if correcto:
        for i in range(1,10):
            if tokens[posicion+i]=="then":
                if tokens[posicion+i]=="then"and tokens[posicion+i+1]==":" and tokens[posicion+i+2]=="[":

                    vc=verificar_commands(tokens,(posicion+i+3))
                    if vc==False:
                        correcto=False                        
                else:  
                    correcto=False
                if tokens[posicion+i]=="else" :        
                    if tokens[posicion+i]=="else" and tokens[posicion+i+1]==":":
                        vc=verificar_commands(tokens,(posicion+i+3))
                        if vc==False:
                            correcto=False                        
                    else:  
                        correcto=False
    
    return correcto 


#Función para verificar la estructura de los loops con while.

def verficicar_loop(tokens,posicion):
    correcto=True
    if tokens[posicion+1]!=":":
        correcto=False
    if tokens[posicion+2] in conditions: 
        vc=verificar_commands(tokens,(posicion+2))
        if vc==False:
            correcto=False

    else:
        correcto=False
    if correcto:
        for i in range(1,10):
            if tokens[posicion+i]=="do":
                if tokens[posicion+i]=="do"and tokens[posicion+i+1]==":" and tokens[posicion+i+2]=="[":  
                    vc=verificar_commands(tokens,(posicion+i+3))
                    if vc==False:
                        correcto=False  
                
                    if correcto :
                         break   
                
                else:
                    correcto=False

              

              
    return correcto 

#Función para verificar la estructura Repeat Times con for.

def verficicar_RepeatTimes(tokens,posicion):
    correcto=True
    if tokens[posicion+1]!=":":
        correcto=False
    if tokens[posicion+2].isdigit()==False and tokens[posicion+3]!="[": 
        correcto=False
    if tokens[posicion+4] in complex_commands_2_keys or tokens[posicion+4] in complex_commands_keys:
        vc=verificar_commands(tokens,(posicion+2))
        if vc==False:
            correcto=False
    else:
        correcto=False  
    return correcto 

def verificar_funciones(tokens,posicion):
    correcto=True
    
    if tokens[posicion+2].isdigit()==False:
        correcto=False
    #Función para verificar si todo el programa es funcional.

    return correcto
def verificar_todo(tokens):
    correcto=True
    termino=True
    palos=None 
    corechetes=None
    while correcto and termino:
        if inializacion(tokens)==False:
            print("error al iniar")
            correcto=False  
        palos=contar_palos(tokens)   
        corechetes=contar_corechetes(tokens)
        if palos ==False or  corechetes ==False:
            correcto=False
            print("error de parentesis, parentesis o palos")
        guardar_funciones(tokens)
        
        guaradar_variables(tokens)
        for i in range(len(tokens)):
            if tokens[i] in conditions or tokens[i] in complex_commands_2_keys or tokens[i] in complex_commands_keys:
                comandos=verificar_commands(tokens, i)
                if comandos!=True:
                    print("error", i, "comandos")
                    correcto=False                    
            if tokens[i] =="if": 
                if verficicar_condicional(tokens,i)!=True:
                    print("error", i, "if")
                    correcto=False
            if tokens[i] =="repeat": 
                if verficicar_RepeatTimes(tokens,i)!=True:
                    print("error", i, "repeat")
                    correcto=False
            if tokens[i] =="while": 
                if verficicar_loop(tokens,i)!=True:
                    print("error", i, "while")
                    correcto=False
            if tokens[i] in funiones_creadas and tokens[i+1]!=":":
                verificar=verificar_crear_funciones(tokens,i)
                if verificar==False:
                    print("Error en la funcion, linea", tokens[i], i)
            if tokens[i] in funiones_creadas and tokens[i+1]==":":
                verificar=verificar_funciones(tokens,i)
                if verificar==False:
                    print("Error en la funcion invocada, linea", tokens[i], i)


        termino=False

    if correcto:
        print("SI, el programa es correcto")
    else:
        print("NO, el programa es incorrecto")
    
            

      
archivo=cargarArchivo("PruebaCompleja.txt")
tokens=generar_tokens(archivo)
print(tokens)
print("----------")
guaradar_variables(tokens)
guardar_funciones(tokens)
print(verificar_todo(tokens))


#print(contar_corechetes(tokens), contar_parentesis(tokens), contar_palos(tokens))
