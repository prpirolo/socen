import os
import json
import fDados
import datetime as dt

dados = fDados.fConfig()

caminho = (dados["alianca"]["SOCEN"]["destino"])
sPrefixo = (dados['alianca']['SOCEN']['prefixoArq'])
#print('Destino: '+caminho+' Prefixo: '+sPrefixo)

arquivos = os.listdir(caminho)

totDias = (dados["alianca"]["qtosDias"])
contDia = 0
totOS = 0

while contDia < totDias:
    dd = dt.timedelta(totDias - (contDia + 1))
    data = dt.datetime.now() - dd

    contDia += 1
    diamesano = data.strftime("%d%m%y")
    mes = data.strftime("%m")
    ano2 = data.strftime("%y")
    print(chr(13)+str(data))
    totarqs = 0

    nomeInicialArq = sPrefixo + str(diamesano)

    for elemento in arquivos:

        if nomeInicialArq in elemento:

            arquivo = open(caminho + elemento,"r", encoding="utf-8")
            texto = arquivo.read()
            texto = texto.split()

            for palavra in texto:
                os = palavra.find("3ALC")
                if os > 0:
                    print(palavra[os:os+11] + " (" + elemento+")")
                    totarqs = totarqs + 1
                    totOS = totOS + 1

print()
print("Total de OS: "+str(totOS))
