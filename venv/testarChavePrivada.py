import paramiko
import fDados

def test_ssh_connection(hostname, username, private_key_path, passphrase=None):
    try:
        # Carregar a chave privada
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path, password=passphrase)

        # Criar cliente SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Conectar ao servidor SSH
        client.connect(hostname=hostname, username=username, pkey=private_key)

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

    sHost = retConfig["alianca"]["host"]
    sUser = retConfig["alianca"]["usuario"]
    chave_privada_path = retConfig["alianca"]["chave_privada_path"]
    senha_privada_path = retConfig["alianca"]["senha_privada_path"]

    # Testar a conexão SSH
    test_ssh_connection(sHost, sUser, chave_privada_path, senha_privada_path)
except Exception as e:
    print("Erro ao carregar informações de conexão:", e)
