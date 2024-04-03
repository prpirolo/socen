import os
import json
import fDados

retorno = fDados.retAcesso()

print("host: " + retorno[0])
print("usuário: " + retorno[1])
print("senha: " + retorno[2])
print("NOTFIS: " + str(retorno[7]))
print("origem Notfis: " + retorno[8])
print("destino: " + retorno[9])
print("prefixoArq: " + retorno[10])

with open("dados.json", encoding="utf-8") as arq_json:
    dados = json.load(arq_json)

caminho = (dados["alianca"]["NOTFIS"]["destino"])
print(caminho)

arquivos = os.listdir(caminho)
print(arquivos)

for elemento in arquivos:

    arquivo = open(caminho + elemento,"r", encoding="utf-8")
    texto = arquivo.read()
    texto = texto.split()

    for palavra in texto:
       nf = palavra.find("NOTFI")
       if nf > 0:
            print(palavra[nf+5:nf+13] + " (" + elemento+")")

