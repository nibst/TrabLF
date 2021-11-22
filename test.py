from carregaAF import *
from classes import *

# test_1: testa lendo um arquivo com um automato AFN, transformando em AFD e salvando em um arquivo
def test_1():
    Q = []
    F = []
    automato = Automato(None,Q,None,F)
    carregaAF("testAFN.TXT", automato)   
    AFD = AFNparaAFD2(automato)
    for estado in AFD.estados:
        print('estado: ', estado.nome)
        for transicao in estado.transicoes:
            print('transicao: ', transicao.simbolo, transicao.prox_estado)
    for estados_finais in AFD.estados_finais:
        print('estado final: ', estados_finais.nome)
    #salvaAFD("testAFN-AFD.TXT", AFD, automato)

# test_2: testa lendo um arquivo com um automato AFD
def test2():
    Q = []
    F = []
    automato = Automato(None,Q,None,F)
    carregaAF("testAFN-AFD.TXT", automato)
    automato.aceita("bb")

if __name__ == "__main__":
    test_1()
    #test2()