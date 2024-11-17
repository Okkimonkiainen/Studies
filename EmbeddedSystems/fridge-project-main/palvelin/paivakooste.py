from flask import Flask
from datetime import datetime, timedelta
import mysql.connector
import mysql.connector.pooling
import mysql.connector.errors
import json
import io
#TIETOKANTA
dbtiedosto=io.open("mysite/dbconfig.json", encoding="UTF-8")
dbconfig=json.load(dbtiedosto)

# Globaalin tietokantayhteyden alustaminen
pool=mysql.connector.pooling.MySQLConnectionPool(
    pool_name="tietokantayhteydet",
    pool_size=2,
    **dbconfig
)

con=pool.get_connection()
cur=con.cursor(buffered=True, dictionary=True)

# Globaalit aikaan liittyvät muuttujat edellisen vuorokauden tietojen hakua varten
eilinenAikaAsDatetime = datetime.now()-timedelta(1)
eilinen = datetime.strftime(eilinenAikaAsDatetime, "%Y-%m-%d %H-%i-%S")
aika=datetime.strftime(datetime.now(), "%Y-%m-%d %H-&i-%S")

app = Flask(__name__)
app.config.update(
    SESSION_COOKIE_SAMESITE='Lax'
)

#Sähköpostin lähetystä varten:
from flask_mail import Mail, Message
import io, json
tiedosto=io.open("mysite/emailconfig.json", encoding="UTF-8")
emailconfig=json.load(tiedosto)
mail_settings={
    "MAIL_SERVER":'smtp.gmail.com',
    "MAIL_PORT":465,
    "MAIL_USE_TLS":False,
    "MAIL_USE_SSL":True,
    "MAIL_USERNAME": emailconfig['GMAIL'],
    "MAIL_PASSWORD": emailconfig['SALASANA']
}
app.config.update(mail_settings)
mail=Mail(app)

# Funktio keskilämpötilojen hakua varten
def haeKeskiLampo(sensorin_id):

    sql="""
    SELECT AVG(tulos)
    FROM mittaukset
    WHERE sensorin_id = %s
    AND mittauksen_datetime between %s and %s
    AND mitattava_suure = "lämpötila";
    """
    #

    cur.execute(sql,(str(sensorin_id), eilinen, aika))
    keskilampotila= cur.fetchall()
    keskilampotila = keskilampotila[0]['AVG(tulos)']

    # Pyöristetään tulokset yhden desimaalin tarkkuudelle
    if(keskilampotila != None):
        keskilampotila = round(keskilampotila, 1)
        return str(keskilampotila)

    return str(keskilampotila)

# Funktio maksimilämpötilojen hakua varten
def haeMaxLampo(sensorin_id):

    sql="""
    SELECT MAX(tulos)
    FROM mittaukset
    WHERE sensorin_id = %s
    AND mittauksen_datetime between %s and %s
    AND mitattava_suure = "lämpötila";
    """
    #

    cur.execute(sql,(str(sensorin_id), eilinen, aika))
    maxlampotila= cur.fetchall()
    maxlampotila = maxlampotila[0]['MAX(tulos)']

    return str(maxlampotila)

# Funktio minimilämpötilojen hakua varten
def haeMinLampo(sensorin_id):

    sql="""
    SELECT MIN(tulos)
    FROM mittaukset
    WHERE sensorin_id = %s
    AND mittauksen_datetime between %s and %s
    AND mitattava_suure = "lämpötila";
    """
    #

    cur.execute(sql,(str(sensorin_id), eilinen, aika))
    minlampotila= cur.fetchall()
    minlampotila = minlampotila[0]['MIN(tulos)']

    return str(minlampotila)

# Funktio minimikosteusarvojen hakua varten
def haeMinKosteus(sensorin_id):

    sql="""
    SELECT MIN(tulos)
    FROM mittaukset
    WHERE sensorin_id = %s
    AND mittauksen_datetime between %s and %s
    AND mitattava_suure = "ilmankosteus";
    """
    #

    cur.execute(sql,(str(sensorin_id), eilinen, aika))
    minKosteus= cur.fetchall()
    minKosteus = minKosteus[0]['MIN(tulos)']

    return str(minKosteus)

# Funktio maksimikosteusarvojen hakua varten
def haeMaxKosteus(sensorin_id):

    sql="""
    SELECT MAX(tulos)
    FROM mittaukset
    WHERE sensorin_id = %s
    AND mittauksen_datetime between %s and %s
    AND mitattava_suure = "ilmankosteus";
    """
    #

    cur.execute(sql,(str(sensorin_id), eilinen, aika))
    maxKosteus= cur.fetchall()
    maxKosteus = maxKosteus[0]['MAX(tulos)']

    return str(maxKosteus)

# Funktio keskikosteusarvojen hakua varten
def haeKeskiKosteus(sensorin_id):

    sql="""
    SELECT AVG(tulos)
    FROM mittaukset
    WHERE sensorin_id = %s
    AND mittauksen_datetime between %s and %s
    AND mitattava_suure = "ilmankosteus";
    """
    #

    cur.execute(sql,(str(sensorin_id), eilinen, aika))
    kosteus= cur.fetchall()
    kosteus = kosteus[0]['AVG(tulos)']

    # Pyöristetään arvo yhden desimaalin tarkkuuteen
    if(kosteus != None):
        kosteus = round(kosteus, 1)
        return str(kosteus)

    return str(kosteus)

# Funktio keskivaloisuuden hakua varten
def haeKeskiValo(sensorin_id):

    sql="""
    SELECT AVG(tulos)
    FROM mittaukset
    WHERE sensorin_id = %s
    AND mittauksen_datetime between %s and %s
    AND mitattava_suure = "valo";
    """
    #

    cur.execute(sql,(str(sensorin_id), eilinen, aika))
    valo= cur.fetchall()
    valo = valo[0]['AVG(tulos)']

    # Pyöristetään arvo yhden desimaalin tarkkuuteen
    if(valo != None):
        valo = round(valo, 1)
        return str(valo)

    return str(valo)

# Funktio maksimivaloisuuden hakua varten
def haeMaxValo(sensorin_id):

    sql="""
    SELECT MAX(tulos)
    FROM mittaukset
    WHERE sensorin_id = %s
    AND mittauksen_datetime between %s and %s
    AND mitattava_suure = "valo";
    """
    #

    cur.execute(sql,(str(sensorin_id), eilinen, aika))
    valo= cur.fetchall()
    valo = valo[0]['MAX(tulos)']

    return str(valo)

# Funktio minimivaloisuuden hakua varten
def haeMinValo(sensorin_id):

    sql="""
    SELECT MIN(tulos)
    FROM mittaukset
    WHERE sensorin_id = %s
    AND mittauksen_datetime between %s and %s
    AND mitattava_suure = "valo";
    """
    #

    cur.execute(sql,(str(sensorin_id), eilinen, aika))
    valo= cur.fetchall()
    valo = valo[0]['MIN(tulos)']

    return str(valo)

# Funktio keskipaineen hakua varten
def haeKeskiPaine(sensorin_id):

    sql="""
    SELECT AVG(tulos)
    FROM mittaukset
    WHERE sensorin_id = %s
    AND mittauksen_datetime between %s and %s
    AND mitattava_suure = "ilmanpaine";
    """
    #

    cur.execute(sql,(str(sensorin_id), eilinen, aika))
    paine= cur.fetchall()
    paine = paine[0]['AVG(tulos)']

    # Pyöristetään arvo yhden desimaalin tarkkuuteen
    if(paine != None):
        paine = round(paine, 1)
        return str(paine)

    return str(paine)

# Funktio maksimipaineen hakua varten
def haeMaxPaine(sensorin_id):

    sql="""
    SELECT MAX(tulos)
    FROM mittaukset
    WHERE sensorin_id = %s
    AND mittauksen_datetime between %s and %s
    AND mitattava_suure = "ilmanpaine";
    """
    #

    cur.execute(sql,(str(sensorin_id), eilinen, aika))
    paine= cur.fetchall()
    paine = paine[0]['MAX(tulos)']

    return str(paine)

# Funktio minimipaineen hakua varten
def haeMinPaine(sensorin_id):

    sql="""
    SELECT MIN(tulos)
    FROM mittaukset
    WHERE sensorin_id = %s
    AND mittauksen_datetime between %s and %s
    AND mitattava_suure = "ilmanpaine";
    """
    #

    cur.execute(sql,(str(sensorin_id), eilinen, aika))
    paine= cur.fetchall()
    paine = paine[0]['MIN(tulos)']

    return str(paine)

# Funktio, jolla haetaan ovien aukaisujen lkm
def haeOvienAvaukset(sensorin_id):

    sql="""
    SELECT SUM(tulos)
    FROM mittaukset
    WHERE sensorin_id = %s
    AND mittauksen_datetime between %s and %s
    """
    #

    cur.execute(sql,(str(sensorin_id), eilinen, aika))
    ovi= cur.fetchall()
    ovi = str(ovi[0]['SUM(tulos)'])

    return ovi

# Funktio, jolla haetaan edellisen vuorokauden aikana tulleet hälytykset
# Haun jälkeen tulokset yhdistetään html-koodiin ja palautetaan
def haeHalytykset():

    sql="""
    SELECT mittauksen_datetime, sensorin_id, mitattava_suure, tulos, kuitattu, kuittaus_aika
    FROM mittaukset
    WHERE poikkeus = 1
    AND mittauksen_datetime between %s and %s
    """
    #

    cur.execute(sql,(eilinen, aika))
    halytykset= cur.fetchall()
    palautus = ""
    i = len(halytykset)
    for x in range(i):
        palautus += "<h3>Hälytys " + str(x+1) + "</h3>"
        palautus += "<p>Hälytys tullut (pvm + aika): " + str(halytykset[x]['mittauksen_datetime']) +"</p>"
        palautus += "<p>Hälytys saapunut sensorista: " + str(halytykset[x]['sensorin_id'])+ "</p>"
        palautus += "<p>Mitattava suure: " + str(halytykset[x]['mitattava_suure']) + "</p>"
        palautus += "<p>Hälytyksen aiheuttanut tulos: " + str(halytykset[x]['tulos']) + "</p>"
        #Raja-arvojen ilmoitus spostissa:
        if str(halytykset[x]['sensorin_id'])=='102001' or str(halytykset[x]['sensorin_id'])=='102002':
            palautus +="<p>Lämpötilan raja-arvot: 2-8 °C</p>"
        else:
            if str(halytykset[x]['mitattava_suure'])=='lämpötila':
                palautus +="<p>Lämpötilan arvo ei saa olla yli: 23 °C</p>"
            elif str(halytykset[x]['mitattava_suure'])=='ilmankosteus':
                palautus +="<p>Kosteuden raja-arvot: 45-70 %</p>"
            elif str(halytykset[x]['mitattava_suure'])=='ilmanpaine':
                palautus +="<p>Ilmanpaineen raja-arvot: 1013-1028</p>"
            elif str(halytykset[x]['mitattava_suure'])=='valo':
                palautus +="<p>Valon arvo ei saa olla yli: 4000</p>"

        palautus += "<p>Onko hälytys kuitattu: " + str(halytykset[x]['kuitattu']) + "</p>"
        palautus += "<p>Kuittaus tehty (pvm + aika): " + str(halytykset[x]['kuittaus_aika']) + "</p>"

    return palautus

# Muodostetaan html-koodi sähköpostin lähetystä varten
# Funktiokutsuissa haetaan tiettyyn sensoriin liittyvät tiedot.
# Lopuksi viesti lähetetään.
with app.app_context():

    html="<h1>Lääkehuoneen olosuhdeseuranta</h1>"

    # HTML solmu 1:n liittyvä osa
    html += "<h2>Avohyllyt ja huumausainekaappi</h2><h3>Avohyllyjen lämpötila-arvot</h3><p>Avohyllyjen lämpötila keskiarvo: " + haeKeskiLampo(101001) + "</p><p>Avohyllyjen lämpötilan maksimiarvo: " + haeMaxLampo(101001) + "</p><p>Avohyllyjen lämpötilan minimiarvo: " + haeMinLampo(101001) + "</p>"
    html += "<h3>Avohyllyjen ilmanpainearvot</h3><p>Avohyllyjen ilmanpaine keskiarvo: " + haeKeskiPaine(101001) + "</p><p>Avohyllyjen ilmanpaineen maksimiarvo: " + haeMaxPaine(101001) + "</p><p>Avohyllyjen ilmanpaineen minimiarvo: " + haeMinPaine(101001) + "</p>"
    html += "<h3>Avohyllyjen ilmankosteusarvot</h3><p></p><p>Avohyllyjen ilmankosteus keskiarvo: "+ haeKeskiKosteus(101001) + "</p><p>Avohyllyjen ilmankosteuden maksimiarvo: " + haeMaxKosteus(101001) + "</p><p>Avohyllyjen ilmankosteuden minimiarvo: " + haeMinKosteus(101001) + "</p>"
    html += "<h3>Avohyllyjen valoisuusarvot</h3><p></p><p>Avohyllyjen valoisuus keskiarvo: " + haeKeskiValo(101002) +"</p><p>Avohyllyjen valoisuus maksimiarvo: " + haeMaxValo(101002) + "</p><p>Avohyllyjen valoisuus minimiarvo: " + haeMinValo(101002) + "</p>"
    html += "<h3>Huumauskaapin avaukset</h3><p></p><p>Huumekaappi avattu: " + haeOvienAvaukset(101003) + " kertaa</p>"

    # HTML solmu 2:n liittyvä osa
    html += "<h2>Jääkaappi</h2><h3>Jääkaapin yläosan lämpötilat</h3><p>Jääkaappi yläosa keskilämpötila: " + haeKeskiLampo(102001) + "</p><p>Jääkaappi yläosa maksimilämpötila: " + haeMaxLampo(102001) + "</p><p>Jääkaappi yläosa minimilämpötila: " + haeMinLampo(102001) + "</p>"
    html += "<h3>Jääkaapin alaosan lämpötilat</h3><p>Jääkaappi alaosa keskilämpötila: " + haeKeskiLampo(102002) + "</p><p>Jääkaappi alaosa maksimilämpötila: " + haeMaxLampo(102002) + "</p><p>Jääkaappi alaosa minimilämpötila: " + haeMinLampo(102002) + "</p>"
    html += "<h3>Jääkaapin aukaisusta aiheutuneet hälytykset</h3><p>Jääkapin ovesta aiheutuneita hälytyksiä: " + haeOvienAvaukset(102003) + " kertaa</p>"

    # HTML solmu 3:n liittyvä osa
    html += "<h2>Infuusionestekaappi</h2><h3>Infuusionestekaapin lämpötila-arvot</h3><p>Infuusionestekaappi keskilämpötila: " + haeKeskiLampo(103001) + "</p><p>Infuusionestekaappi maksimilämpötila: " + haeMaxLampo(103001) + "</p><p>Infuusionestekaappi minimilämpötila: " + haeMinLampo(103001) + "</p>"
    html += "<h3>Infuusionestekaapin valoisuusarvot</h3><p>Infuusionestekaappi valoisuus keskiarvo: " + haeKeskiValo(103002) + "</p><p>Infuusiokaappi valoisuus maksimiarvo: " + haeMaxValo(103002) + "</p><p>Infuusiokaappi valoisuus minimiarvo: " + haeMinValo(103002) + "</p>"

    # HTML solmu 4 liittyvä osa
    html += "<h2>Ovellinen lääkekaappi</h2><h3>Ovellisen lääkaapin lämpötila-arvot</h3><p>Ovellinen lääkekaappi keskilämpötila: " + haeKeskiLampo(104001) + "</p><p>Ovellinen lääkekaappi maksimilämpötila: " + haeMaxLampo(104001) + "</p><p>Ovellinen lääkekaappi minimilämpötila: " + haeMinLampo(104001)+ "</p>"

    html += "<h2>Hälytykset</h2><p>Hälytys kuitattu = 1</p><p>Hälytystä ei kuitattu = 0</p> " + str(haeHalytykset())


    viesti=Message(subject="LÄÄKEHUONEEN PÄIVÄKOOSTE",
                   sender=app.config.get("MAIL_USERNAME"),
                   recipients=[emailconfig['VASTAANOTTAJA1'], emailconfig['VASTAANOTTAJA2']],
                   html = html
                   )
    mail.send(viesti)

    con.close()
