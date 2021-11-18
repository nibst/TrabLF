
class Transicao:
    def __init__(self,simbolo,prox_estado):
        self.simbolo = simbolo
        self.prox_estado = prox_estado  #proximo estado ao ler o simbolo
class Estado:
    def __init__(self,estado):
        self.estado = estado    #estado atual
        self.transicoes = []    #lista de transicoes, cada transicao tem formato (letra,prox_estado)
class Automato:
    def __init__(self,nome,Q,q0,F):
        self.nome = nome    #nome do automato
        self.estados = Q    #Q é uma lista de instancias da classe Estado, contem todos estados
        self.estado_inicial = q0    #q0 é uma instancia da classe Estado,então ja tem as transicoes incluso
        self.estados_finais = F     #F é uma lista de instancias da classe Estado, então ja tem as transicoes de cada estado
