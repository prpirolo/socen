from PySimpleGUI import PySimpleGUI as sg
import json

#Carrega as informações do dados.json
try:
    with open('dados.json', 'r', encoding='utf-8-sig') as dadosJson:
        dados = json.load(dadosJson)

    cliente = dados["alianca"]
    host = cliente["host"]
    usuario = cliente["usuario"]
    senha = cliente["senha"]
    qtosDias = cliente["qtosDias"]
    removerArq = cliente["removerArqOrigem"]
    origem = cliente["origem"]
    SOCEN = cliente["SOCEN"]
    destino = SOCEN["destino"]
    prefixoArq = SOCEN["prefixoArq"]
    NOTFIS = cliente["NOTFIS"]
    destino_NOTFIS = NOTFIS["destino"]
    prefixoArq_NOTFIS = NOTFIS["prefixoArq"]

    if removerArq == 0:
        removerArqOrigem = 'false'
    else:
        removerArqOrigem = 'true'

except FileNotFoundError:
    print('Arquivo não encontrado.')
except IOError:
    print('Erro I/O')



#Layout
sg.theme('Reddit')
layout = [
    [sg.Text('             Host: '), sg.Input(key='iHost', size=(50,1), default_text=host)],
    [sg.Text('         Usuário: '), sg.Input(key='iUsuario', size=(30,1), default_text=usuario)],
    [sg.Text('           Senha: '), sg.Input(key='iSenha', size=(30,1), default_text=senha)],
    [sg.Text(' Quantos dias: '), sg.Input(key='iDias', size=(5,1), default_text=qtosDias)],
    [sg.Text('  Remover Arq: '), sg.Input(key='iRemove', size=(10,1), default_text=removerArqOrigem)],
    [sg.Text(' SFTP Origem: '), sg.Input(key='iOrigem', size=(50,1), default_text=origem)],
    [sg.Text()],
    [sg.Text('***  S O C E N  ***')],
    [sg.Text('Pasta Destino: '), sg.Input(key='iDestino', size=(50,1), default_text=destino)],
    [sg.Text('    Prefixo Arq: '), sg.Input(key='iPrefixo', size=(25,1), default_text=prefixoArq)],
    [sg.Text()],
    [sg.Text('***  N O T F I S  ***')],
    [sg.Text('Pasta Destino: '), sg.Input(key='iDestinoNOTFIS', size=(50,1), default_text=destino_NOTFIS)],
    [sg.Text('    Prefixo Arq: '), sg.Input(key='iPrefixoNOTFIS', size=(25,1), default_text=prefixoArq_NOTFIS)],
    [sg.Text()],
    [sg.Button('Gravar')],
    [sg.Text()]
]

#Janela
janela = sg.Window('Arquivo de Configuração', layout)

#Ler os eventos
while True:
    eventos, valores = janela.read()
    if eventos == sg.WINDOW_CLOSED:
        break
    if eventos == 'Gravar':
        #Gravar arquivo
        with open('dados.json', 'w', encoding='utf-8-sig') as arqJSon:
            arqJSon.writelines('{'+chr(13))
            arqJSon.writelines('  "alianca":'+chr(13))
            arqJSon.writelines('    {'+chr(13))
            arqJSon.writelines('      "host": "'+str(valores['iHost'])+'",'+chr(13))
            arqJSon.writelines('      "usuario": "'+str(valores['iUsuario'])+'",'+chr(13))
            arqJSon.writelines('      "senha": "'+str(valores['iSenha'])+'",'+chr(13))
            arqJSon.writelines('      "qtosDias": '+str(valores['iDias'])+','+chr(13))
            arqJSon.writelines('      "removerArqOrigem": '+str(valores['iRemove'])+','+chr(13))
            arqJSon.writelines('      "origem": "'+str(valores['iOrigem'])+'",'+chr(13))
            arqJSon.writelines('      "SOCEN":'+chr(13))
            arqJSon.writelines('        {'+chr(13))
            arqJSon.writelines('          "destino": "'+str(valores['iDestino'])+'",'+chr(13))
            arqJSon.writelines('          "prefixoArq": "'+str(valores['iPrefixo'])+'"'+chr(13))
            arqJSon.writelines('        },'+chr(13))
            arqJSon.writelines('      "NOTFIS":'+chr(13))
            arqJSon.writelines('        {'+chr(13))
            arqJSon.writelines('          "destino": "'+str(valores['iDestinoNOTFIS'])+'",'+chr(13))
            arqJSon.writelines('          "prefixoArq": "'+str(valores['iPrefixoNOTFIS'])+'"'+chr(13))
            arqJSon.writelines('        }'+chr(13))
            arqJSon.writelines('    }'+chr(13))
            arqJSon.writelines('}'+chr(13))
        break
