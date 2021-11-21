from carregaAF import *
from classes import *

# test_1: testa lendo um arquivo com um automato AFN, transformando em AFD e salvando em um arquivo
def test_1():
    Q = []
    F = []
    automato = Automato(None,Q,None,F)
    carregaAF("testAFN.TXT", automato)   
    AFD = AFNparaAFD(automato)
    salvaAFD("testAFN-AFD.TXT", AFD, automato)

# test_2: testa lendo um arquivo com um automato AFD
def test2():
    Q = []
    F = []
    automato = Automato(None,Q,None,F)
    carregaAF("testAFN-AFD.TXT", automato)
    automato.aceita("bb")

if __name__ == "__main__":
    test_1()
    test2()