import file
import main_tweet
import filters
import json
import subprocess
import os
from datetime import datetime
import sys

print ("--------------------Iniciando")

current = os.getcwd() 
json_in = os.getcwd() + "\\entrada.json"
json_teste = os.getcwd() + "\\teste.json"

#Cria o arquivo json de saída
arq = file.File(json_teste)

inicio = datetime.now()
print ("Inicio: ")
print (inicio)
print ("")

#instancia os filtros para a primeira consulta
filt = filters.Filters

#coloca os filtros da busca dos twwets

fil = open(json_in, "r")

if fil.mode != 'r' :
    print("Não existe arquivo de entrada!")
    sys.exit()

reader = json.loads(fil.read())
arquivo_saida = "-t .json"
log = ""

for fill in reader:
    filt.use_limit= fill["use_limit"]
    filt.max_tweets = fill["max_tweets"]
    filt.query_search = fill["query_search"]
    filt.by_username = fill["by_username"]
    filt.use_date = fill["use_date"] 
    filt.date_since = datetime.strptime(fill["date_since"], '%Y/%m/%d')
    filt.date_until = datetime.strptime(fill["date_until"], '%Y/%m/%d')
    filt.top_tweets = fill["top_tweets"] 
    filt.use_place = fill["use_place"] 
    filt.place = fill["place"]
    filt.area = fill["area"]
    filt.use_geoLocales = fill["use_geoLocales"] 
    filt.geo = fill["geo"]
    arquivo_saida = "-t " + fill["arquivo_saida"]
    
    if fill["log"] == True:
        log = "-l"
print("Data inicial")
print(filt.date_since.strftime("%Y-%m-%d"))
print("Data final")
print(filt.date_until.strftime("%Y-%m-%d"))

fil.close()

#efetua a consulta
imp1 = main_tweet.Tweets._searchTweets(filt)

#limpa a consulta para caso houver mais consultas
imp = []
filt.query_search = ""

#lista de buscas a se fazer
results = []
results.append("USERNAME")

primeiro = True

buscarUsuarios = False

#Se houver alguma busca a mais para ser feita no tweet, vai buscas
if len(results) > 0  and buscarUsuarios:
    for js in imp1:
        for st in results: 
            filt.use_date = False
            filt.use_limit = True
            filt.use_place = False
            filt.use_geoLocales = False
            filt.query_search = ""
            filt.by_username = ""

            # se for busca por usuário coloca o filtro de usuário
            if st == "USERNAME":
                filt.by_username = js[st]
            else :
                if st == "SINCE" or st == "UNTIL":
                    filt.date_since = js["SINCE"]
                    filt.date_until = js["UNTIL"]
                    filt.use_date = True
                else:
                    if st == "QUERYSEARCH":
                        filt.query_search = js[st]
                    else :
                        if st == "NEAR" :
                            filt.place = js[st]                 
                            filt.use_place = True

            filt.top_tweets = True
            if primeiro == True :
                imp=main_tweet.Tweets._searchTweets(filt)
                primeiro = False
            else:
                imp+=main_tweet.Tweets._searchTweets(filt)

imp1+=imp
arq._writeOnFile(json.dumps(imp1))
fim_requisicao = datetime.now()
saida = 0
print ("")
print ("Fim da requisição: ")
print (fim_requisicao)

try:
    saida = subprocess.check_call( current + "\\API_Conector_Json.exe" + " -i \"" + arq.director  + "\" " + arquivo_saida + " " + log)
except Exception:                             
    print ("Erro ao chamar programa externo")

fim = datetime.now()
print ("Saida")
print (saida)
print ("")
print ("Fim para salvar arquivo: ")
print (fim)
print ("")
print ("Saida: " + current + "\\OUT")
print ("")
print ("--------------------Finalizando")
print ("")
