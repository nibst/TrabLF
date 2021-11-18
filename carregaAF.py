import re

from classes import *


def carregaAF(automato:Automato):
    file = open("automato.txt",mode="r")
    linha = file.readline()
    #pegar nome e estados inicial e finais do automato
    header = linha.split('=',1)     #faz 1 split com o '=' como delimitador, fica uma lista [nomeautomato, resto_da_linha]
    automato.nome = header[0]
    estados = re.search('\(([^)]+)', header[1]).group(1) #pega tudo que está dentro dos parenteses (exemplo header[1] = "=(q0,{q1,q3})", então fica = "q0,{q1,q3}")
    '''
    separar o estado inicial dos estados finais e pegar o estado inicial, 
    com o exemplo de cima ficaria uma lista [q0,{q1,q3}] e daí eu pego apenas o primeiro da lista
    '''
    estado_inicial = (estados.split(',',1))[0]
    estados_finais = re.search('\{([^}]+)',estados).group(1) #processo similiar ao de parenteses só que com chaves {}
    estados_finais = estados_finais.split(',')
    for i in range(len(estados_finais)):
          automato.estados_finais.append(Estado(estados_finais[i]))
    automato.estado_inicial = Estado(estado_inicial)
    #colocarei os estados no campo estados do automato quando for checar as transicoes
    carregaTransicoes(file,automato)
    file.close()

def carregaTransicoes(file,automato):
    #TODO