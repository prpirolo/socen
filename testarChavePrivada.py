import paramiko
import fDados

def test_ssh_connection(hostname, port, username, private_key_path, passphrase=None):
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

        # Fechar a conexão SSH
        client.close()
    except Exception as e:
        # Se ocorrer algum erro, imprimir mensagem de falha
        print("Falha ao conectar via SSH:", e)

# Importar as informações de conexão do arquivo fDados.py
try:
    retConfig = fDados.fConfig()

    sHost = retConfig["alianca"]["host_chave"]
    sPort = retConfig["alianca"]["port_chave"]
    sUser = retConfig["alianca"]["user_chave"]
    sFile = retConfig["alianca"]["file_chave"]
    sPwd = retConfig["alianca"]["pwd_chave"]

    # Testar a conexão SSH
    test_ssh_connection(sHost, sPort, sUser, sFile, sPwd)
except Exception as e:
    print("Erro ao carregar informações de conexão:", e)
