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


def AfnParaAfd(automato:Automato):

    # passo 1: Cria uma tabela de transição para AFD
    TabelaDeTransicao = {}
    simbolos = automato.lista_simbolos()
    estado_inicial = automato.estado_inicial

    # passo 2: adiciona o estado inicial na tabela de transição
    q0 = Estado(estado_inicial)
    q0.transicoes = automato.busca_estado(estado_inicial).juntaProximosEstadosComTransicoesIguais()
    conjunto_de_estados = tuple([q0.nome])
    TabelaDeTransicao[conjunto_de_estados] = q0.transicoes

    # repete os passos 3-4 até que não haja mais transições
    for estado in automato.estados:
        if estado.nome == estado_inicial:
            continue

        # passo 3: adiciona o estado atual na tabela de transição
        qn = Estado(estado.nome)
        qn.transicoes = estado.juntaProximosEstadosComTransicoesIguais()
        # busca na tabela de transição o conjunto formado contendo o estado atual
        conjunto_de_estados = buscaNaTabelaDeTransicao(TabelaDeTransicao, qn.nome)
        conjunto_de_estados_sem_estado_atual = tuple(filter(lambda x: x != qn.nome, conjunto_de_estados))
        for linha in TabelaDeTransicao:
            if sorted(linha) == sorted(conjunto_de_estados_sem_estado_atual):
                for simbolo in simbolos:
                    conj = TabelaDeTransicao[linha].get(simbolo, None)
                    if conj is not None:
                        if not qn.transicoes.get(simbolo):
                            qn.transicoes[simbolo] = []
                        entradas = list(filter(lambda state: not state.prox_estado in tuple(map(lambda x: x.prox_estado, qn.transicoes[simbolo])), conj))
                        qn.transicoes[simbolo] = sorted(qn.transicoes[simbolo] + entradas)
                break
        TabelaDeTransicao[conjunto_de_estados] = qn.transicoes
    return TabelaDeTransicao
    
def buscaNaTabelaDeTransicao(TabelaDeTransicao, estado_buscado):
    for estadoTransicoes in TabelaDeTransicao.values():
        estadoTransicoesProxEstado = list(map(lambda x: list(map(lambda y: y.prox_estado,x)), estadoTransicoes.values()))
        for conjunto_de_estados in estadoTransicoesProxEstado:
            if estado_buscado in conjunto_de_estados:
                return tuple(conjunto_de_estados)
    return None

def salvaAFD(filename, afd, automato):
    estados_finais = ','.join(list(map(lambda estado: str(functools.reduce(lambda a, b: a + str(b), estado, "")), 
    list(filter(lambda key: tuple(filter(lambda estados: estados in key, automato.estados_finais)), afd.keys())))))

    file = open(filename, mode="w")
    file.write(automato.nome + "=" + "(" + automato.estado_inicial + ",{" + str(estados_finais) + "})\n")
    
    for estadoNome, estado in afd.items():
#        print('Estado Nome: ',estadoNome)
        file.write(functools.reduce(lambda acc, x: acc + str(x), tuple(estadoNome), ""))
        file.write("\n")
        for key, value in estado.items():
#            print('Entrada: ', key)
#            print('Transicao: ', end="\t")
            file.write(key + ":" + functools.reduce(lambda acc, x: acc + str(x), tuple(map(lambda x: x.prox_estado, value)), "") + "\n")
#            for trans in value:
#                print(trans.prox_estado, end=" ")
#            print("\n")
#        print("===============================================")
    file.close()