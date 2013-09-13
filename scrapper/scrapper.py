#!/usr/bin/env python
# coding=utf8

#import scraperwiki
import json
import pycurl
import urllib
import StringIO
import lxml.html
import csv

# armo una lista con los torneos que voy a scrappear
tournaments = ["Apertura 90","Clausura 91","Apertura 91","Clausura 92","Apertura 92","Clausura 93","Apertura 93","Clausura 94","Apertura 94","Clausura 95","Apertura 95","Clausura 96","Apertura 96","Clausura 97","Apertura 97","Clausura 98","Apertura 98","Clausura 99","Apertura 99","Clausura 00","Apertura 00","Clausura 01","Apertura 01","Clausura 02","Apertura 02","Clausura 03","Apertura 03","Clausura 04","Apertura 04","Clausura 05","Apertura 05","Clausura 06","Apertura 06","Clausura 07","Apertura 07","Clausura 08","Apertura 08","Clausura 09","Apertura 09","Clausura 10","Apertura 10","Clausura 11","Apertura 11","Clausura 12","Inicial 12"]

#creo que el archivo donde voy a guardar los resultados y escribo el encabezado de las columnas
fp = open('data/resultados.csv', 'wb')
a = csv.DictWriter(fp, ['torneo', 'fecha', 'date', 'local', 'visitante', 'resultado'])
a.writeheader()

i=0
#ciclo por los torneos
for tour in tournaments:    
    

    # armo la url donde esta la data y hago una magia para que me den los resutlados
    url = "http://www.futbolxxi.com/Torneo.aspx?" + urllib.urlencode({'ID' : tour})    
    page = lxml.html.fromstring(urllib.urlopen(url).read())
    validtation = page.cssselect("input[id='__EVENTVALIDATION']")
    state = page.cssselect("input[id='__VIEWSTATE']")
    print "Scrappeando " + tour + "... "  + url
    print "Validation: " + validtation[0].get('value')

    # ciclo por las fechas
    fechas = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
    for fecha in fechas:
        print "Fecha " + str(fecha)

        # armo el request para que me de la data de esa fecha
        post_params = [    
            ('BF'+str(fecha), 'Fecha '+str(fecha)),        
            ('__EVENTVALIDATION', validtation[0].get('value')),
            ('__VIEWSTATE', state[0].get('value')),
        ]
        resp_data = urllib.urlencode(post_params)
        response = StringIO.StringIO()
        curl = pycurl.Curl()
        curl.setopt(pycurl.HTTP_VERSION, pycurl.CURL_HTTP_VERSION_1_1)
        curl.setopt(pycurl.WRITEFUNCTION, response.write)
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.POST, 1) 
        curl.setopt(pycurl.POSTFIELDS, resp_data) 
        
        curl.perform()
        root = lxml.html.fromstring(response.getvalue())                
        validation2 = root.cssselect("input[id='__EVENTVALIDATION']")        
        
        # busco en el html la tabla con los resultados y hago el scrapping propiamente dicho
        for tr in root.cssselect("table[id='DataGrid2'] tr"):    
            tds = tr.cssselect("td")
            data = {
                'torneo': tour,
                'fecha': str(fecha),
                'date': tds[0].text_content(),
                'local': tds[1].text_content().strip().encode('utf8').replace("Ãº","ú").replace("Ã©","é").replace("Ã³","ó").replace("Ã¡","á").replace("Ã±","ñ").replace("Ã­","í"),
                'visitante': tds[3].text_content().strip().encode('utf8').replace("Ãº","ú").replace("Ã©","é").replace("Ã³","ó").replace("Ã¡","á").replace("Ã±","ñ").replace("Ã­","í"),
                'resultado': tds[2].text_content().strip()
            }
            print data

            # escribo la data en el archivo
            a.writerow(data)
    i = i+1

# cierro el archivo
fp.close()
