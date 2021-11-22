from carregaAF import *
from classes import *

# test_1: testa lendo um arquivo com um automato AFN, transformando em AFD e salvando em um arquivo
def test_1(filename):
    Q = []
    F = []
    automato = Automato(None,Q,None,F)
    carregaAF(filename, automato)   
    AFD = AFNparaAFD(automato)
    salvaAFD(filename + "-AFD.TXT", AFD)

# test_2: testa lendo um arquivo com um automato AFD
def test2(filename):
    Q = []
    F = []
    automato = Automato(None,Q,None,F)
    carregaAF(filename, automato)
    automato.aceita("bb")

# test_3: testa lendo um arquivo com um automato AFN, transforma em AFD e imprime: os estados, transições e estados finais
def test3(filename):
    Q = []
    F = []
    automato = Automato(None,Q,None,F)
    carregaAF(filename, automato)
    AFD = AFNparaAFD(automato)
    for estado in AFD.estados:
        print('estado: ', estado.nome)
        for transicao in estado.transicoes:
            print('transicao: ', transicao.simbolo, transicao.prox_estado)
    for estados_finais in AFD.estados_finais:
        print('estado final: ', estados_finais.nome)

if __name__ == "__main__":
    test_1("testAFN.TXT")
    #test2()