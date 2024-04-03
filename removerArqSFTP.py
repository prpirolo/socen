import datetime
import json

import paramiko
import datetime as dt
import fDados
import os

# Importa os dados de acesso da função fDados.py

try:
    retConfig = fDados.fConfig()

    sHost = retConfig["alianca"]["host"]
    sUser = retConfig["alianca"]["usuario"]
    sSenha = retConfig["alianca"]["senha"]
    totDias = retConfig["alianca"]["qtosDias"]
    removerArq = retConfig["alianca"]["removerArqOrigem"]
    sOrigem = retConfig["alianca"]["origem"]
    sDestino = retConfig["alianca"]["SOCEN"]["destino"]
    sPrefixo = retConfig["alianca"]["SOCEN"]["prefixoArq"]
    sDestinoNOTFIS = retConfig["alianca"]["NOTFIS"]["destino"]
    sPrefixoNOTFIS = retConfig["alianca"]["NOTFIS"]["prefixoArq"]

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=sHost, username=sUser, password=sSenha, allow_agent=False, look_for_keys=False)

    sftp = client.open_sftp()
    arqs = sftp.listdir(sOrigem)
    print(arqs)

    hoje = dt.datetime.today()
    datahora = hoje.strftime('%d/%m/%y %H:%M')
    arqLog = 'Log-'+str(hoje.strftime('%y%m%d'))+'.txt'

    dd = dt.timedelta(totDias)
    data = dt.datetime.now() - dd

    diamesano = data.strftime('%d%m%y')
    dataremove = data.strftime('%d/%m/%y')

    nomeInicialArq = sPrefixo + str(diamesano)

    # Alimenta a variável com os arquivos da pasta -> não processados
    print(nomeInicialArq)

    removidos = 0

    for image in arqs:
        if nomeInicialArq in image:
            print(sOrigem+image)

            # Gravar um arquivo na pasta origem
            #sftp.put('OS.txt', 'to/OS.txt')

            if removerArq:
                removidos = removidos + 1
                # Remover um arquivo da pasta origem
                sftp.remove(sOrigem+image)

    with open(arqLog, 'a', encoding='utf-8-sig') as arqlog:
        arqlog.write('- removidos '+str(removidos)+' arquivos em '+str(dataremove)+chr(13))

    sftp.close()
    client.close()

except FileNotFoundError:
    erro = 'Arquivo dados.json não encontrado na pasta do programa Executável.'
    with open(arqLog, 'a', encoding='utf-8-sig') as arqlog:
        arqlog.write(str(datetime.date.today())+' Erro: '+erro+chr(13))
except PermissionError:
    erro = 'Usuário sem pemissão para abrir aquivo dados.json.'
    with open(arqLog, 'a', encoding='utf-8-sig') as arqlog:
        arqlog.write(str(datetime.date.today())+' Erro: '+erro+chr(13))
except IOError:
    erro = 'Erro de E/S.'
    with open(arqLog, 'a', encoding='utf-8-sig') as arqlog:
        arqlog.write(str(datetime.date.today())+' Erro: '+erro+chr(13))
except json.JSONDecodeError:
    erro = 'Formato do arquivo dados.json inválido. Erro de decoder.'
    with open(arqLog, 'a', encoding='utf-8-sig') as arqlog:
        arqlog.write(str(datetime.date.today())+' Erro: '+erro+chr(13))
