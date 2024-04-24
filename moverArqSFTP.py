import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import paramiko
import json
import fDados
import datetime as dt
import os


# Função para registrar mensagens de erro em um arquivo de log
def log_error(error_message):
    arqLog = 'Log-' + dt.datetime.today().strftime('%y%m%d') + '.txt'
    with open(arqLog, 'a', encoding='utf-8-sig') as arqlog:
        arqlog.write(str(dt.datetime.now().strftime('%d/%m/%y %H:%M')) + ' - ERRO: ' + error_message + '\n')


# Função para registrar mensagens de log
def log_message(message):
    arqLog = 'Log-' + dt.datetime.today().strftime('%y%m%d') + '.txt'
    with open(arqLog, 'a', encoding='utf-8-sig') as arqlog:
        arqlog.write(str(dt.datetime.now().strftime('%d/%m/%y %H:%M')) + ' - ' + message + '\n')


def test_ssh_connection(hostname, port, username, private_key_path, passphrase, password):
    try:
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path, password=passphrase)
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=hostname, port=port, username=username, pkey=private_key, look_for_keys=False)
        return client
    except Exception as e:
        log_error("Falha ao conectar via SSH: " + str(e))
        return None


try:
    log_message("Iniciando o serviço...")

    retConfig = fDados.fConfig()
    ambiente = "PRODUCAO"  # Definido manualmente para teste, pode ser modificado conforme necessário
    log_message("Ambiente definido: " + ambiente)

    # Recuperando configurações do arquivo de configuração
    totDias = retConfig["alianca"]["qtosDias"]
    removerArq = retConfig["alianca"]["removerArqOrigem"]
    sDestino = retConfig["alianca"]["SOCEN"]["destino"]
    sPrefixo = retConfig["alianca"]["SOCEN"]["prefixoArq"]
    sDestinoNOTFIS = retConfig["alianca"]["NOTFIS"]["destino"]
    sPrefixoNOTFIS = retConfig["alianca"]["NOTFIS"]["prefixoArq"]
    sOutBound = retConfig["alianca"]["outbound_chave"]
    sHost = retConfig["alianca"][ambiente]["host_chave"]
    sPort = retConfig["alianca"][ambiente]["port_chave"]
    sUser = retConfig["alianca"][ambiente]["user_chave"]
    sFile = retConfig["alianca"][ambiente]["file_chave"]
    sPwd = retConfig["alianca"][ambiente]["pwd_chave"]
    log_message("Variáveis de configuração definidas.")

    # Testar a conexão SSH
    client = test_ssh_connection(sHost, sPort, sUser, sFile, sPwd, sPwd)
    if client:
        log_message("Conexão SSH bem-sucedida.")
    else:
        log_message("Não foi possível estabelecer uma conexão SSH.")

    if client:
        log_message("Conectado...")

        sftp = client.open_sftp()
        arqs = sftp.listdir(sOutBound)

        # Verificar se a pasta de destino não está vazia
        if arqs:
            log_message("Foram encontrados arquivos na pasta de destino.")
            # Adicione aqui qualquer ação que você queira realizar se houver arquivos na pasta de destino
        else:
            log_message("Nenhum arquivo encontrado na pasta de destino.")

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
                        log_message("Arquivo " + image + " sendo copiado...")
                        sftp.get(sOutBound + image, sDestino + image)
                        copiados = copiados + 1
                        totarqs = totarqs + 1
                    else:
                        log_message("Arquivo " + image + " já copiado.")
                        totarqs = totarqs + 1

                if nomeInicialArqNOTFIS in image:
                    copiadoNOTFIS = 0
                    for elemento in arquivosNOTFIS:
                        if (image in elemento):
                            copiadoNOTFIS = 1

                    if copiadoNOTFIS == 0:
                        log_message("Arquivo " + image + " sendo copiado...")
                        sftp.get(sOutBound + image, sDestinoNOTFIS + image)
                        copiadosNOTFIS = copiadosNOTFIS + 1
                        totarqsNOTFIS = totarqsNOTFIS + 1
                    else:
                        log_message("Arquivo " + image + " já copiado.")
                        totarqsNOTFIS = totarqsNOTFIS + 1

            with open(arqLog, 'a', encoding='utf-8-sig') as arqlog:
                arqlog.write('[SOCEN ' + str(copiados) + '/' + str(totarqs))
                arqlog.write(' NOTFIS ' + str(copiadosNOTFIS) + '/' + str(totarqsNOTFIS) + '] ')

        dd = dt.timedelta(totDias)
        data = dt.datetime.now() - dd

        diamesano = data.strftime('%d%m%y')

        nomeInicialArq = sPrefixo + str(diamesano)
        nomeInicialArqNOTFIS = sPrefixoNOTFIS + str(diamesano)

        removidos = 0
        removidosNOTFIS = 0

        for image in arqs:
            if nomeInicialArq in image:
                if removerArq:
                    removidos = removidos + 1
                    sftp.remove(sOutBound + image)

            if nomeInicialArqNOTFIS in image:
                if removerArq:
                    removidosNOTFIS = removidosNOTFIS + 1
                    sftp.remove(sOutBound + image)

        with open(arqLog, 'a', encoding='utf-8-sig') as arqlog:
            arqlog.write('- Removidos SOCEN: ' + str(removidos))
            arqlog.write(' NOTFIS: ' + str(removidosNOTFIS) + '\n')

        sftp.close()
        client.close()

    log_message("Serviço finalizado com sucesso.")

except FileNotFoundError:
    log_error('Arquivo dados.json não encontrado na pasta do programa Executável.')
except PermissionError:
    log_error('Usuário sem permissão para abrir arquivo dados.json.')
except IOError:
    log_error('Erro de E/S.')
except json.JSONDecodeError:
    log_error('Formato do arquivo dados.json inválido. Erro de decoder.')
except Exception as e:
    log_error(str(e))
