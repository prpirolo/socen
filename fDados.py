import json

def retAcesso():
    with open('dados.json', 'r', encoding='utf-8-sig') as acesso:
        dados = json.load(acesso)

    cliente = dados["alianca"]
    SOCEN = cliente["SOCEN"]
    origem = cliente["outbound_chave"]
    destino = SOCEN["destino"]
    prefixoArq = SOCEN["prefixoArq"]
    kHost = cliente["host_chave"]
    kPort = cliente["port_chave"]
    kUser = cliente["user_chave"]
    kFile = cliente["file_chave"]
    kPwd = cliente["pwd_chave"]

    return (SOCEN,origem,destino,prefixoArq,kHost, kPort, kUser, kFile, kPwd)

def fConfig():
        with open('dados.json', 'r', encoding='utf-8-sig') as arqJson:
            arqDados = json.load(arqJson)
        return (arqDados)