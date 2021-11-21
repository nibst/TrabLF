from carregaAF import *
from classes import *
def main():
    Q = []
    F = []
    automato = Automato(None,Q,None,F)
    carregaAF("AFD.TXT", automato)
    w = input("Escolha uma palavra: ")
    automato.aceita("")
main()