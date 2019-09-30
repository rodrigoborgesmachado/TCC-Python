import file
import main_tweet
import filters
import json
import subprocess
from datetime import datetime

#Cria o arquivo json de saída
arq = file.File("teste.json")

inicio = datetime.now()

#instancia os filtros para a primeira consulta
filt = filters.Filters
filt.max_tweets = 20
filt.query_search = "europe refugees"

#efetua a consulta
imp1 = main_tweet.Tweets._searchTweets(filt)

#limpa a consulta para caso houver mais consultas
imp = []
filt.max_tweets = 20
filt.query_search = ""

#lista de buscas a se fazer
results = []
results.append("USERNAME:")

primeiro = True

#Se houver alguma busca a mais para ser feita no tweet, vai buscas
if len(results) > 0 :
    for js in imp1:
        for st in results: 
            filt.use_date = False
            filt.use_limit = False
            filt.use_place = False
            filt.use_geoLocales = False
            filt.query_search = ""
            filt.by_username = ""

            # se for busca por usuário coloca o filtro de usuário
            if st == "USERNAME:":
                filt.by_username = js[st]
            else :
                if st == "SINCE:" or st == "UNTIL:":
                    filt.date_since = js["SINCE:"]
                    filt.date_until = js["UNTIL:"]
                    filt.use_date = True
                else:
                    if st == "QUERYSEARCH:":
                        filt.query_search = js[st]
                    else :
                        if st == "NEAR:" :
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
arquivo_saida = "-t .json;.csv;.xml;.sql"
log = ""
try:
    saida = subprocess.check_call("API_Conector_Json.exe" + " -i " + arq.director  + " " + arquivo_saida + " " + log)
    fim = datetime.now()
    print ("Saida")
    print (saida)
    print ("")
    print ("Inicio: ")
    print (inicio)
    print ("")
    print ("Fim da requisição: ")
    print (fim_requisicao)
    print ("")
    print ("Fim para salvar arquivo: ")
    print (fim)
except Exception:                             
    print ("Erro ao chamar programa externo")
    fim = datetime.now()
    print ("Inicio: ")
    print (inicio)
    print ("")
    print ("Fim da requisição: ")
    print (fim_requisicao)
    print ("")
    print ("Fim para salvar arquivo: ")
    print (fim)