
class Transicao:
    def __init__(self,simbolo,prox_estado):
        self.simbolo = simbolo
        self.prox_estado = prox_estado  #proximo estado ao ler o simbolo
    def __lt__(self, other):
        if len(self.prox_estado) == len(other.prox_estado):
            return self.prox_estado < other.prox_estado
        return len(self.prox_estado) < len(other.prox_estado)

class Estado:
    def __init__(self,estado):
        self.nome = estado    #estado atual
        self.transicoes = []    #lista de transicoes, cada transicao tem formato (letra,prox_estado)
    def juntaProximosEstadosComTransicoesIguais(self):
        dicionario = {}
        for transicao in self.transicoes:
            if not transicao.simbolo in dicionario:
                dicionario[transicao.simbolo] = []
            dicionario[transicao.simbolo].append(transicao)
        return dicionario
    
class Automato:
    def __init__(self,nome,Q,q0,F):
        self.nome = nome    #nome do automato
        self.estados = Q    #Q é uma lista de instancias da classe Estado (que contem transicao de cada estado), contem todos estados
        self.estado_inicial = q0    #q0 é o nome do estado inicial apenas, sem as transicoes
        self.estados_finais = F     #F é o nome dos estados finais apenas, sem as transicoes

    def aceita(self,palavra):
        estado_inicial = self.estado_inicial
        caminho = []
        n_estados = len(self.estados)
        estado_atual = self.__busca_estado(estado_inicial)
        caminho.append(estado_atual.nome)
        for letra in palavra:
            flag = 0    #nao achou transicao
            transicoes = estado_atual.transicoes
            for transicao in transicoes:    #procura em cada transicao se há uma transicao com essa letra
                if letra == transicao.simbolo:  #se acha uma transicao com essa letra adiciona ao caminho
                    caminho.append(transicao.simbolo)
                    estado_atual = self.__busca_estado(transicao.prox_estado)
                    caminho.append(estado_atual.nome)
                    flag = 1    #achou transicao
                    break
            if flag == 0:   #se não achou transicao fazer caminho ser vazio
                caminho = []
                break
        self.__imprime_resultado(caminho)

    def __imprime_resultado(self,caminho):
        tamanho = len(caminho)
        if tamanho == 0:  #se o caminho está vazio
            print('Palavra rejeitada')
        else:
            for estado_final in self.estados_finais:    #checa se o ultimo estado é final
                if estado_final == caminho[tamanho-1]:
                    for i in range(tamanho):
                        if i%2 == 0:                #se for estado
                            print(f"({caminho[i]})", end="")
                        else:                       #se for simbolo
                            print (f"--{caminho[i]}-->",end= "")
                    print("\nPalavra aceitada")
                    return
            print('Palavra rejeitada')

    def __busca_estado(self,nome_estado):   #retorna o estado a ser buscado
        for estado in self.estados:     #pega o estado com nome nome_estado
            if estado.nome == nome_estado:
                return estado
        return None

    def busca_estado(self, nome_estado):
        return self.__busca_estado(nome_estado)

    def lista_simbolos(self):
        simbolos = []
        for estado in self.estados:
            for transicao in estado.transicoes:
                if transicao.simbolo not in simbolos:
                    simbolos.append(transicao.simbolo)
        return simbolos
