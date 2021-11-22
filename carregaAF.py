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

# geraLinha gera a linha da tabela de transições do estado atual
# contendo todas as transições do estado tuplado
def geraLinha(automato, tuplaDeEstados):
    simbolos = automato.lista_simbolos() # pega os simbolos do automato
    linha = []
    for estado in tuplaDeEstados: # para cada estado da tupla
        estadoBuscado = automato.busca_estado(estado)
        for simbolo in simbolos: # para cada simbolo do automato
            linha = linha + estadoTransicoesPorSimbolo(estadoBuscado, simbolo) # concatena as transições
    junta_transicoes = gera_novas_transicoes(linha) # junta as transições com simbolos iguais
    return junta_transicoes

def estadoTransicoesPorSimbolo(estado, simbolo): 
    transicoes = []
    # monta um array de transições para o simbolo passado
    for transicao in estado.transicoes:
        if transicao.simbolo == simbolo:
            transicoes.append(transicao)
    return transicoes

# recebe um array de transições, junta os de simbolos iguais e retorna um array de Transição contendo tuplas no seu proximo estado
def gera_novas_transicoes(transicoes):
    novas_transicoes = {}
    # gera um dicionario no formato {simbolo: (estado1, estado2)}
    for transicao in transicoes:
        if not transicao.simbolo in novas_transicoes: # se o simbolo não estiver contido no dicionario de novas transições
            novas_transicoes[transicao.simbolo] = tuple() # insere o simbolo como chave e uma tupla vazia como valor
        if not transicao.prox_estado in novas_transicoes[transicao.simbolo]: # só insere se o proximo estado não estiver contido no dicionario de novas transições
            novas_transicoes[transicao.simbolo] = novas_transicoes[transicao.simbolo] + (transicao.prox_estado,)
    outras_novas = []
    # gera um array de Transicao contendo todas as transições
    for transicao in novas_transicoes.items():
        outras_novas.append(Transicao(transicao[0], tuple(sorted(set(transicao[1])))))
    # retorna array de Transicaos
    return outras_novas

def junta_transicoes_por_estado(estado_transicoes):
    transicoes = {}
    # gera um dicionario no formato {simbolo: (estado1, estado2)}
    for transicao in estado_transicoes:
        if not transicao.simbolo in transicoes:
            transicoes[transicao.simbolo] = tuple()
        transicoes[transicao.simbolo] = tuple(sorted(set(transicoes[transicao.simbolo] + transicao.prox_estado)))
    # retorna um array dos valores do dicionario
    return transicoes.values()

# filtra estados não inseridos no AFD com base na tabela de transições gerada
def filtra_estados_nao_inseridos_contidos_na_tabela_de_transicao(T, Q, lista_estados_nao_inseridos):
    filtrado = []
    junta_transicoes = junta_transicoes_por_estado(T.transicoes) # junta as transições por estado
    for transicao in junta_transicoes: # para cada transição
        transicao_limpa = tuple(sorted(set(transicao))) # remove os estados repetidos
        # se não estiver no conjunto Q, nem na "lista de estados nao inseridos" e nem no conjunto filtrado
        if not transicao_limpa in Q and not transicao_limpa in lista_estados_nao_inseridos and not transicao_limpa in filtrado: 
            filtrado.append(transicao_limpa) # adiciona na lista de estados filtrados
    return filtrado

def AFNparaAFD(automato):
    # passo 1:
    # Q será chamado de Q'
    Q = []
    # Q_text guarda os estados do automato em formato de texto
    Q_text = []
    T = []
    # F guarda os Estados Finais
    F = []
    estados_nao_inseridos = []
    estado_inicial = (automato.estado_inicial,)

    # passo 2: adiciona o estado inicial na tabela de transição
    q0 = Estado(estado_inicial)
    q0.transicoes = geraLinha(automato, estado_inicial)
    Q.append(q0)
    Q_text.append(estado_inicial)
    T = q0.transicoes

    # monta um array contendo os estados não inseridos em Q'
    estados_nao_inseridos = filtra_estados_nao_inseridos_contidos_na_tabela_de_transicao(q0, Q_text, [])

    # passo 3: para cada estado em Q' encontra o possivel conjunto de estados de cada entrada
    # usando a função de transição da NFA. Insere os estados encontrados até que não tenha novos estados.
    while len(estados_nao_inseridos) > 0:
        # pega o primeiro estado não inserido na tabela de transição de Q'
        novo_estado = tuple(sorted(set(estados_nao_inseridos[0])))
        # cria um novo estado com este estado não inserido
        qn = Estado(novo_estado)
        # cria transições para este novo estado
        qn.transicoes = geraLinha(automato, novo_estado)
        # insere o novo estado na tabela de transição de Q'
        Q.append(qn)
        Q_text.append(novo_estado)
        # insere as transições do novo estado na tabela de transição de T
        T = T + qn.transicoes
        # atualiza a lista de estados não inseridos
        estados_nao_inseridos = estados_nao_inseridos[1:] + filtra_estados_nao_inseridos_contidos_na_tabela_de_transicao(qn, Q_text, estados_nao_inseridos)

    # passo 4: Os estados finais serão os estados que possuem estados finais de AFN
    for estadoTuplado in Q: # estadoTuplado é uma tupla de estados
        for estado in estadoTuplado.nome: # como o nome do estado é uma tupla, é usado para percorrer os estados da tupla e verificar se pertencem a um estado final.
            if estado in automato.estados_finais: # se o estado pertence ao conjunto de estados finais do AFN
                F.append(estadoTuplado) # adiciona o estado na lista de estados finais do AFD
    return Automato(automato.nome, Q, estado_inicial, F)

def tuplaParaString(tupla): # recebe uma tupla de estados e retorna uma string (q1, q2) -> q1q2
    return functools.reduce(lambda acc, valor: acc + str(valor), tuple(tupla), "")

def salvaAFD(filename, automato): # salva o automato em um arquivo
    file = open(filename, mode="w")
    estados_finais_string = ','.join(list(map(lambda estado_final: str(tuplaParaString(estado_final.nome)), automato.estados_finais)))
    file.write(automato.nome + "=" + "(" + tuplaParaString(automato.estado_inicial) + ",{" + str(estados_finais_string) + "})\n")

    for estado in automato.estados:
        file.write(tuplaParaString(estado.nome))
        file.write("\n")
        for transicao in estado.transicoes:
            file.write(transicao.simbolo + ":" + tuplaParaString(transicao.prox_estado))
            file.write("\n")
    file.close()