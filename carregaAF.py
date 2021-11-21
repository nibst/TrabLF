import re
from classes import *
import functools

def carregaAF(filename, automato:Automato):
    file = open(filename,mode="r")
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

    automato.estados_finais = estados_finais
    automato.estado_inicial = estado_inicial
    #colocarei os estados no campo estados do automato quando for checar as transicoes
    carregaTransicoes(file,automato)
    file.close()

def carregaTransicoes(file,automato):
    linha = file.readline()
    while linha:
        if linha and (linha.find(':') == -1) :   #enquanto nao achar o char ':' e enquanto não acabar o automato
            estado_atual = linha.rstrip()
            estado_atual = Estado(estado_atual)
            linha = file.readline()
        if linha and (linha.find(':') != -1):   #se não chegou no fim do arquivo e são transições
            linha = linha.rstrip()
            transicao = linha.split(':')
            transicao = Transicao(transicao[0],transicao[1])
            estado_atual.transicoes.append(transicao)
            linha = file.readline()
        if (not linha) or (linha.find(':') == -1):   #se a próxima linha for um estado ou acabar o arquivo então colocar estado atual no automato
            automato.estados.append(estado_atual)


def AFNparaAFD(automato:Automato):
    # passo 1: Cria uma tabela de transição para AFD
    tabela_de_transicao = {}
    simbolos = automato.lista_simbolos()
    estado_inicial = automato.estado_inicial

    # passo 2: adiciona o estado inicial na tabela de transição
    q0 = Estado(estado_inicial)
    q0.transicoes = automato.busca_estado(estado_inicial).juntaProximosEstadosComTransicoesIguais()
    conjunto_de_estados = tuple([q0.nome])
    tabela_de_transicao[conjunto_de_estados] = q0.transicoes

    # repete os passos 3-4 até que não haja mais transições
    for estado in automato.estados:
        if estado.nome == estado_inicial:
            continue

        # passo 3: adiciona o estado atual na tabela de transição
        qn = Estado(estado.nome)
        qn.transicoes = estado.juntaProximosEstadosComTransicoesIguais()
        # busca na tabela de transição o conjunto formado contendo o estado atual
        conjunto_de_estados = buscaNaTabelaDeTransicao(tabela_de_transicao, qn.nome)
        conjunto_de_estados_sem_estado_atual = tuple(filter(lambda x: x != qn.nome, conjunto_de_estados)) # retira o estado atual pois ele ja foi inserido na tabela de transição anteriormente (passo 3)
        for linha in tabela_de_transicao:
            # ordena o conjunto da linha e do conjunto de estados sem o estado atual
            # pois [a,b] != [b,a]
            if sorted(linha) == sorted(conjunto_de_estados_sem_estado_atual):
                for simbolo in simbolos: # para cada simbolo da lista de simbolos do Automato
                    conjunto_de_estados_do_simbolo = tabela_de_transicao[linha].get(simbolo, None)
                    if conjunto_de_estados_do_simbolo is not None:
                        if not qn.transicoes.get(simbolo):
                            qn.transicoes[simbolo] = []
                        novas_transicoes = filtra_estados_com_transicoes_diferentes(qn.transicoes[simbolo], conjunto_de_estados_do_simbolo)
                        qn.transicoes[simbolo] = sorted(qn.transicoes[simbolo] + novas_transicoes) # expande um conjunto de estados com transições diferentes
                break # dá break no for, pois já encontrou o conjunto de estados que é igual o conjunto de estados sem o estado atual
        tabela_de_transicao[conjunto_de_estados] = qn.transicoes
    return tabela_de_transicao

def filtra_estados_com_transicoes_diferentes(transicoes, conjunto_de_estados):
    filtrado = []
    tupla_transicoes_prox_estado = tuple(map(lambda x: x.prox_estado, transicoes))
    for estado in conjunto_de_estados:
        if not estado.prox_estado in tupla_transicoes_prox_estado:
            filtrado.append(estado)
    return filtrado
    #return list(filter(lambda state: not state.prox_estado in tuple(map(lambda x: x.prox_estado, transicoes)), conjunto_de_estados))

# mapeia uma lista de instancias de Transições para uma tupla de estados
def mapeia_estados_transicoes_prox_estado(estado_transicoes):
    return tuple(map(lambda estado_transicao: list(map(lambda transicao: transicao.prox_estado, estado_transicao)), estado_transicoes))

def buscaNaTabelaDeTransicao(tabela_de_transicao, estado_buscado):
    for estado_transicoes in tabela_de_transicao.values():
        estados_transicoes_prox_estado = mapeia_estados_transicoes_prox_estado(estado_transicoes.values())
        for conjunto_de_estados in estados_transicoes_prox_estado:
            if estado_buscado in conjunto_de_estados:
                return tuple(conjunto_de_estados)
    return None

def tuplaParaString(tupla):
    return functools.reduce(lambda acc, valor: acc + str(valor), tuple(tupla), "")

# recebe um array de chaves e retorna uma string com os estados separados por virgula
def estados_para_string(array_de_chaves, estados_finais):
    estados = list( map(tuplaParaString, 
                    list(   filter(lambda key: tuple(filter(lambda estados: estados in key, estados_finais)), 
                            array_de_chaves))))
    return ', '.join(estados)

def salvaAFD(filename, afd, automato):
    estados_finais_string = estados_para_string(afd.keys(), automato.estados_finais)

    file = open(filename, mode="w")
    file.write(automato.nome + "=" + "(" + automato.estado_inicial + ",{" + str(estados_finais_string) + "})\n")
    
    for estado_nome, estado in afd.items():
#        print('Estado Nome: ',estado_nome)
        file.write(tuplaParaString(estado_nome))
        file.write("\n")
        for key, value in estado.items():
#            print('Entrada: ', key)
#            print('Transicao: ', end="\t")
            file.write(key + ":" + tuplaParaString(map(lambda x: x.prox_estado, value)) + "\n")
#            for trans in value:
#                print(trans.prox_estado, end=" ")
#            print("\n")
#        print("===============================================")
    file.close()