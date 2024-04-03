# Comando para gerar arquivo .exe
# no terminal digite:
# pyinstaller --onefile moverArqSFTP.py
#
# arquivo dados.json deve acompanhar o executável
# qtosDias = quantidade de dias a verificar e transferir da pasta origem, contados de hoje para trás
# removerArqOrigem = se estiver como true remove arquivos da pasta origem e false não remove arquivos da pasta origem
import datetime
import json

import paramiko
import datetime as dt
import fDados
import os

# Importa os dados de acesso da função fDados.py

try:
    retConfig = fDados.fConfig()

    sHost           = retConfig["alianca"]["host"]
    sUser           = retConfig["alianca"]["usuario"]
    sSenha          = retConfig["alianca"]["senha"]
    totDias         = retConfig["alianca"]["qtosDias"]
    removerArq      = retConfig["alianca"]["removerArqOrigem"]
    sOrigem         = retConfig["alianca"]["origem"]
    sDestino        = retConfig["alianca"]["SOCEN"]["destino"]
    sPrefixo        = retConfig["alianca"]["SOCEN"]["prefixoArq"]
    sDestinoNOTFIS  = retConfig["alianca"]["NOTFIS"]["destino"]
    sPrefixoNOTFIS  = retConfig["alianca"]["NOTFIS"]["prefixoArq"]



    client = paramiko.SSHClient()
    #sKey = client.
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #client.connect(hostname=sHost,username=sUser,password=sSenha,allow_agent=False,look_for_keys=False)
    client.connect(hostname=sHost,username=sUser,pkey=sKey,allow_agent=False,look_for_keys=False)
    sftp = client.open_sftp()
    arqs = sftp.listdir(sOrigem)  # Carregar os arquivos do servidor SFTP do cliente

    hoje = dt.datetime.today()
    datahora = hoje.strftime('%d/%m/%y %H:%M')
    arqLog = 'Log-'+str(hoje.strftime('%y%m%d'))+'.txt'

    with open(arqLog, 'a', encoding='utf-8-sig') as arqlog:
        arqlog.write(str(datahora) + 'h ')

    contDia = 0

    while contDia < totDias:
        dd = dt.timedelta(totDias - (contDia+1))
        data = dt.datetime.now() - dd

        contDia += 1
        diames = data.strftime('%d%m')
        diamesano = data.strftime('%d%m%y')
        diabarrames = data.strftime('%d/%m')

        print(diamesano)

        nomeInicialArq = sPrefixo + str(diamesano)
        nomeInicialArqNOTFIS = sPrefixoNOTFIS + str(diamesano)

        # pasta destino do arquivo
        arquivos = os.listdir(sDestino)
        arquivosNOTFIS = os.listdir(sDestinoNOTFIS)

        copiados = 0
        copiadosNOTFIS = 0
        totarqs = 0
        totarqsNOTFIS = 0

        for image in arqs:
            if nomeInicialArq in image:
                # print(image)
                copiado = 0
                for elemento in arquivos:
                    if(image in elemento):  # Se arquivo origem (SFTP) estiver dentro do arquivo destino (nosso servidor)
                        copiado = 1

                if copiado == 0:
                    print("Arquivo "+image+" sendo copiado...")
                    sftp.get(sOrigem + image, sDestino + image)
                    copiados = copiados + 1
                    totarqs = totarqs + 1
                else:
                    print("Arquivo "+image+" já copiado.")
                    totarqs = totarqs + 1

            if nomeInicialArqNOTFIS in image:
                # print(image)
                copiadoNOTFIS = 0
                for elemento in arquivosNOTFIS:
                    if (image in elemento):  # Se arquivo origem (SFTP) estiver dentro do arquivo destino (nosso servidor)
                        copiadoNOTFIS = 1

                if copiadoNOTFIS == 0:
                    print("Arquivo " + image + " sendo copiado...")
                    sftp.get(sOrigem + image, sDestinoNOTFIS + image)
                    copiadosNOTFIS = copiadosNOTFIS + 1
                    totarqsNOTFIS = totarqsNOTFIS + 1
                else:
                    print("Arquivo " + image + " já copiado.")
                    totarqsNOTFIS = totarqsNOTFIS + 1

        with open(arqLog, 'a', encoding='utf-8-sig') as arqlog:
            arqlog.write('[ ('+diabarrames+') SOCEN '+str(copiados)+'/'+str(totarqs))
            arqlog.write(' NOTFIS '+str(copiadosNOTFIS)+'/'+str(totarqsNOTFIS)+' ]')

    # Remover os arquivos da pasta origem que estão a mais de (var totDias + 1 dia) anteriores a data atual

    dd = dt.timedelta(totDias)
    data = dt.datetime.now() - dd

    diamesano = data.strftime('%d%m%y')
    dataremove = data.strftime('%d/%m/%y')

    nomeInicialArq = sPrefixo + str(diamesano)
    nomeInicialArqNOTFIS = sPrefixoNOTFIS + str(diamesano)

    # Alimenta a variável com os arquivos da pasta -> não processados
    # print(nomeInicialArq)

    removidos = 0
    removidosNOTFIS = 0

    for image in arqs:
        if nomeInicialArq in image:
            if removerArq:
                removidos = removidos + 1
                # Remover um arquivo SOCEN da pasta origem
                sftp.remove(sOrigem+image)

        if nomeInicialArqNOTFIS in image:
            if removerArq:
                removidosNOTFIS = removidosNOTFIS + 1
                # Remover um arquivo NOTFIS da pasta origem
                sftp.remove(sOrigem + image)

    with open(arqLog, 'a', encoding='utf-8-sig') as arqlog:
        arqlog.write('- Foram removidos em '+str(dataremove)+' ')
        arqlog.write('- SOCEN '+str(removidos)+" arqs ")
        arqlog.write('- NOTFIS '+str(removidosNOTFIS)+' arqs.'+chr(13))

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
