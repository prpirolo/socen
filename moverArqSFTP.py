import paramiko
import json
import fDados
import datetime as dt
import os


def test_ssh_connection(hostname, port, username, private_key_path, passphrase):
    try:
        # Carregar a chave privada
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path, password=passphrase)

        # Criar cliente SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Conectar ao servidor SSH
        client.connect(hostname=hostname, port=port, username=username, pkey=private_key, look_for_keys=False)

        # Se a conexão foi bem sucedida, imprimir mensagem de sucesso
        print("Conexão SSH bem-sucedida!")

        return client

    except Exception as e:
        # Se ocorrer algum erro, imprimir mensagem de falha
        print("Falha ao conectar via SSH:", e)
        return None


try:

    retConfig = fDados.fConfig()

    print("aqui...")
    totDias = retConfig["alianca"]["qtosDias"]
    sDestino = retConfig["alianca"]["SOCEN"]["destino"]
    sPrefixo = retConfig["alianca"]["SOCEN"]["prefixoArq"]
    sDestinoNOTFIS = retConfig["alianca"]["NOTFIS"]["destino"]
    sPrefixoNOTFIS = retConfig["alianca"]["NOTFIS"]["prefixoArq"]
    sOutBound = retConfig["alianca"]["outbound_chave"]
    sHost = retConfig["alianca"]["host_chave"]
    sPort = retConfig["alianca"]["port_chave"]
    sUser = retConfig["alianca"]["user_chave"]
    sFile = retConfig["alianca"]["file_chave"]
    sPwd = retConfig["alianca"]["pwd_chave"]

    # Testar a conexão SSH
    client = test_ssh_connection(sHost, sPort, sUser, sFile, sPwd)

    if client:

        print("Conectado...")

        sftp = client.open_sftp()
        arqs = sftp.listdir(sOutBound)

        # Verificar se a pasta de destino não está vazia
        if arqs:
            print("Foram encontrados arquivos na pasta de destino.")
            for arquivo in arqs:
                print(arquivo)
            # Adicione aqui qualquer ação que você queira realizar se houver arquivos na pasta de destino
        else:
            print("Nenhum arquivo encontrado na pasta de destino.")

        hoje = dt.datetime.today()
        datahora = hoje.strftime('%d/%m/%y %H:%M')
        arqLog = 'Log-' + str(hoje.strftime('%y%m%d')) + '.txt'

        with open(arqLog, 'a', encoding='utf-8-sig') as arqlog:
            arqlog.write(str(datahora) + 'h ')

        contDia = 0

        while contDia < totDias:
            dd = dt.timedelta(totDias - (contDia + 1))
            data = dt.datetime.now() - dd

            contDia += 1
            diames = data.strftime('%d%m')
            diamesano = data.strftime('%d%m%y')
            diabarrames = data.strftime('%d/%m')

            print(diamesano)

            nomeInicialArq = sPrefixo + str(diamesano)
            nomeInicialArqNOTFIS = sPrefixoNOTFIS + str(diamesano)

            arquivos = os.listdir(sDestino)
            arquivosNOTFIS = os.listdir(sDestinoNOTFIS)

            copiados = 0
            copiadosNOTFIS = 0
            totarqs = 0
            totarqsNOTFIS = 0

            for image in arqs:
                if nomeInicialArq in image:
                    copiado = 0
                    for elemento in arquivos:
                        if (image in elemento):
                            copiado = 1

                    if copiado == 0:
                        print("Arquivo " + image + " sendo copiado...")
                        sftp.get(sOutBound + image, sDestino + image)
                        copiados = copiados + 1
                        totarqs = totarqs + 1
                    else:
                        print("Arquivo " + image + " já copiado.")
                        totarqs = totarqs + 1

                if nomeInicialArqNOTFIS in image:
                    copiadoNOTFIS = 0
                    for elemento in arquivosNOTFIS:
                        if (image in elemento):
                            copiadoNOTFIS = 1

                    if copiadoNOTFIS == 0:
                        print("Arquivo " + image + " sendo copiado...")
                        sftp.get(sOutBound + image, sDestinoNOTFIS + image)
                        copiadosNOTFIS = copiadosNOTFIS + 1
                        totarqsNOTFIS = totarqsNOTFIS + 1
                    else:
                        print("Arquivo " + image + " já copiado.")
                        totarqsNOTFIS = totarqsNOTFIS + 1

            with open(arqLog, 'a', encoding='utf-8-sig') as arqlog:
                arqlog.write('[ (' + diabarrames + ') SOCEN ' + str(copiados) + '/' + str(totarqs))
                arqlog.write(' NOTFIS ' + str(copiadosNOTFIS) + '/' + str(totarqsNOTFIS) + ' ]')

        dd = dt.timedelta(totDias)
        data = dt.datetime.now() - dd

        diamesano = data.strftime('%d%m%y')
        dataremove = data.strftime('%d/%m/%y')

        nomeInicialArq = sPrefixo + str(diamesano)
        nomeInicialArqNOTFIS = sPrefixoNOTFIS + str(diamesano)

        removidos = 0
        removidosNOTFIS = 0

        for image in arqs:
            if nomeInicialArq in image:
                if removerArq:
                    removidos = removidos + 1
                    sftp.remove(sOrigem + image)

            if nomeInicialArqNOTFIS in image:
                if removerArq:
                    removidosNOTFIS = removidosNOTFIS + 1
                    sftp.remove(sOrigem + image)

        with open(arqLog, 'a', encoding='utf-8-sig') as arqlog:
            arqlog.write('- Foram removidos em ' + str(dataremove) + ' ')
            arqlog.write('- SOCEN ' + str(removidos) + " arqs ")
            arqlog.write('- NOTFIS ' + str(removidosNOTFIS) + ' arqs.' + chr(13))

        sftp.close()
        client.close()

except FileNotFoundError:
    erro = 'Arquivo dados.json não encontrado na pasta do programa Executável.'
    with open(arqLog, 'a', encoding='utf-8-sig') as arqlog:
        arqlog.write(str(dt.date.today()) + ' Erro: ' + erro + chr(13))
except PermissionError:
    erro = 'Usuário sem permissão para abrir arquivo dados.json.'
    with open(arqLog, 'a', encoding='utf-8-sig') as arqlog:
        arqlog.write(str(dt.date.today()) + ' Erro: ' + erro + chr(13))
except IOError:
    erro = 'Erro de E/S.'
    with open(arqLog, 'a', encoding='utf-8-sig') as arqlog:
        arqlog.write(str(dt.date.today()) + ' Erro: ' + erro + chr(13))
except json.JSONDecodeError:
    erro = 'Formato do arquivo dados.json inválido. Erro de decoder.'
    with open(arqLog, 'a', encoding='utf-8-sig') as arqlog:
        arqlog.write(str(dt.date.today()) + ' Erro: ' + erro + chr(13))
