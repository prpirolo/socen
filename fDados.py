import json

def retAcesso():
    with open('dados.json', 'r', encoding='utf-8-sig') as acesso:
        dados = json.load(acesso)

    cliente = dados["alianca"]
    host = cliente["host"]
    usuario = cliente["usuario"]
    senha = cliente["senha"]
    SOCEN = cliente["SOCEN"]
    origem = cliente["origem"]
    destino = SOCEN["destino"]
    prefixoArq = SOCEN["prefixoArq"]

    return (host,usuario,senha,SOCEN,origem,destino,prefixoArq)

def fConfig():
        with open('dados.json', 'r', encoding='utf-8-sig') as arqJson:
            arqDados = json.load(arqJson)
        return (arqDados)