from flask import Flask, jsonify, render_template, make_response,redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, RadioField, FieldList, StringField, validators, IntegerField, SelectField, widgets, SelectMultipleField, ValidationError
from flask_wtf.csrf import CSRFProtect
from flask import session, redirect, url_for, Response, flash
import datetime
from datetime import datetime, timedelta
from dateutil import tz
from wtforms.fields import DateField,DateTimeField, TimeField
from flask_cors import CORS
import hashlib
from functools import wraps
from wtforms import Form, BooleanField, StringField, SubmitField, validators, IntegerField, PasswordField, SelectField, widgets, SelectMultipleField, ValidationError

#Sähköposti:
from flask_mail import Mail, Message
import os
#Tietokanta yhteyden luominen:
import json
import io
import mysql.connector
import mysql.connector.pooling
import mysql.connector.errors
from mysql.connector import errorcode


#Tietokantaan liittyvien tietojen käsittely
dbtiedosto=io.open("mysite/dbconfig.json", encoding="UTF-8")
dbconfig=json.load(dbtiedosto)

# Globaalin tietokantayhteyden alustaminen
pool=mysql.connector.pooling.MySQLConnectionPool(
    pool_name="tietokantayhteydet",
    pool_size=2,
    **dbconfig
)


app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app, resources={r"/*": {"origins": "*"}})

app.config.update(
    SESSION_COOKIE_SAMESITE='Lax'
)


# set the secret key.  keep this really secret:
app.secret_key = b'\x17\xb4\xcbK\x1e\x14!\x9b=\x88\xaf\xe7\xf8\xfe\x00\xea)\x85\x18=\xd2\xac\xd8\x02'





#Hälytyssähköpostin lähetystä varten tehdyt määritykset:
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


#Yleisfunktio: sähköpostin lähetys, kun poikkeava arvo luettu tietokannasta:
def virheSposti(mittaus):
    with app.app_context():
        #Otetaan poikkeavaan mittaukseen liittyvät tiedot ja asetetaan ne sähköpostiin:
        alue=""
        solmu=str(mittaus['paikka'])
        if int(solmu)==1:
            alue='Avohyllyt'
        elif int(solmu)==2:
            alue='Jääkaappi'
        elif int(solmu)==3:
            alue='Infuusionestelaatikko'
        else:
            alue='Ovellinen lääkekaappi'
        olosuhde=str(mittaus['olosuhde'])
        arvo=str(mittaus['tulos'])
        aika=str(mittaus['aika'])
        if olosuhde=='lämpötila':
            arvo=arvo+"  °C"
        elif olosuhde=='ilmankosteus':
            arvo=arvo+" %"
        elif olosuhde=='ovi':
            arvo='Auki'

        viesti=Message(subject="LÄÄKEHUONE: HÄLYTYS",
                       sender=app.config.get("MAIL_USERNAME"),
                       recipients=[emailconfig['VASTAANOTTAJA1'],emailconfig['VASTAANOTTAJA2']],
                       html="<h2>Lääkehuoneen olosuhteiden valvonta</h2><p><b>Olosuhdehälytys: </b>"+aika+"</p><p><b>Sijainti: </b>"+alue+"</p><p><b>Poikkeama: </b>"+olosuhde+"</p><p><b>Poikkeava arvo: </b>"+arvo+"</p><p>Ole hyvä ja tarkasta olosuhteet.</p><p>Tilanteen ratkettua kuittaa hälytys.</p><p>Muussa tapauksessa toimi yksikön ohjeiden mukaisesti.</p>"
                       )
        mail.send(viesti)


#Yleisfunktio: haetaan tietokannasta lääkehuoneen valittuun alueeseen, liittyvät mittaukset:
def mittaustenHaku(alue):
    #Haetaan tietokannasta kaikkiin solmuihin liittyvät mittaukset:
    try:
        con=pool.get_connection()
        cur=con.cursor(buffered=True, dictionary=True)

        #Valitaan vain tänään mitatut arvot taulukkoon:
        aika=datetime.now().strftime("%Y-%m-%d")
        sql="""SELECT so.solmun_sijoituspaikka AS paikka, so.sensorit, m.mittauksen_datetime AS aika, m.tulos, m.mittauksen_id, m.mitattava_suure AS olosuhde, m.kuitattu, s.sensorin_id AS sid
        FROM solmut so
        JOIN sensorit s
        ON s.solmun_id=so.solmun_id AND so.solmun_sijoituspaikka= %s
        JOIN mittaukset m
        ON m.sensorin_id=s.sensorin_id AND DATE(mittauksen_datetime)= %s
        ORDER BY TIME(mittauksen_datetime) DESC;
        """

        cur.execute(sql,(alue, aika))
        laakehuone=cur.fetchall()
        #Haetaan svg-palloon lääkehuoneen nykyinen tilanne (svg-pallo toimii siis reaaliaikaisemmin) ja tallennetaan sessioihin:
        if(alue!='Avohylly'):
            sql="""SELECT so.solmun_sijoituspaikka AS paikka, so.sensorit, m.mittauksen_datetime AS aika, m.tulos, m.mittauksen_id, m.mitattava_suure AS olosuhde, s.sensorin_id AS sid
            FROM solmut so
            JOIN sensorit s
            ON s.solmun_id=so.solmun_id AND so.solmun_sijoituspaikka= %s
            JOIN mittaukset m
            ON m.sensorin_id=s.sensorin_id AND DATE(mittauksen_datetime)= %s
            ORDER BY TIME(mittauksen_datetime) DESC LIMIT 5;
            """
            cur.execute(sql,('Avohylly', aika))
            pallo=cur.fetchall()
            teksti=[]
            for p in pallo:
                if p['olosuhde']=='lämpötila':
                    teksti.append(p['olosuhde'])
                    session['lampotila']=p['tulos']
                elif p['olosuhde']=='valo':
                    teksti.append(p['olosuhde'])
                    session['valo']=p['tulos']
                elif p['olosuhde']=='ilmankosteus':
                    teksti.append(p['olosuhde'])
                    session['kosteus']=p['tulos']
                elif p['olosuhde']=='ilmanpaine':
                    teksti.append(p['olosuhde'])
                    session['ilmanpaine']=p['tulos']
        #Alueeksi valittu avohylly, joten asetetaan aikaisemin haetut arvot sessioihin:
        else:
            teksti=[]
            laskuri=0
            for l in laakehuone:
                if l['olosuhde']=='lämpötila' and laskuri<4:
                    laskuri=laskuri+1
                    teksti.append(l['olosuhde'])
                    session['lampotila']=l['tulos']
                elif l['olosuhde']=='valo' and laskuri<4:
                    laskuri=laskuri+1
                    teksti.append(l['olosuhde'])
                    session['valo']=l['tulos']
                elif l['olosuhde']=='ilmankosteus' and laskuri<4:
                    laskuri=laskuri+1
                    teksti.append(l['olosuhde'])
                    session['kosteus']=l['tulos']
                elif l['olosuhde']=='ilmanpaine' and laskuri<4:
                    laskuri=laskuri+1
                    teksti.append(l['olosuhde'])
                    session['ilmanpaine']=l['tulos']



    except Exception as err:
        return "Virhe tietokannan käytössä"
    finally:
        con.close()
    #Palautetaan lääkehuoneeseen liittyvät kyselyt:
    return laakehuone






#Yleisfunktio: lisätään sivuille, joihin vaaditaan kirjautuminen:
def auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not 'kayttaja' in session:
            return redirect(url_for('kirjaudu'))
        return f(*args, **kwargs)
    return decorated

@app.route('/', methods=['GET'])
@auth
def siirto():
    return redirect(url_for('paasivu'))


#Autentikointi:
#SISÄÄN KIRJAUTUMINEN:
@app.route('/kirjaudu', methods=['POST', 'GET'])
def kirjaudu():
    #Lomakkeen kentät ja virheilmoitusten määrittely:
    class Kirjautuminen(FlaskForm):
        kayttajatunnus=StringField('kayttajatunnus', validators=[])
        def validate_kayttajatunnus(field, form):
            kayttajatunnus=field.data['kayttajatunnus']
            if len(kayttajatunnus.strip())<1 or kayttajatunnus.strip() is None:
                 raise ValidationError(u"Syötä käyttäjätunnus")

        salasana=PasswordField('salasana', validators=[])
        def validate_salasana(field, form):
            salasana=field.data['salasana']
            if len(salasana.strip())<1 or salasana.strip() is None:
                 raise ValidationError(u"Syötä salasana")

    virhe=False
    try:
        kayttajatunnus=request.form.get('kayttajatunnus', "")
        salasana=request.form.get('salasana', "")


        #Tarkistetaan, että tietokannasta löytyy syötetty käyttäjänimi ja että käyttäjän salasana on oikein
        kayttajansala=""
        if kayttajatunnus!="" and salasana!="":
            try:
                con=pool.get_connection()
                cur=con.cursor(buffered=True, dictionary=True)

                sql="""SELECT *
                FROM kayttajat
                WHERE tunnus=%s;
                """
                cur.execute(sql,(kayttajatunnus,))
                kayttajat=cur.fetchall()

                if len(kayttajat)>0:
                    kayttajansala=kayttajat[0]['salasana']

            except Exception as err:
                return "Virhe tietokannan käytössä"
            finally:
                con.close()
    except:
        kayttajatunnus=""
        salasana=""

    #Tarkitetaan, että käyttäjän salasana syötetty oikein ja tehdään tarvittaessa virheilmoitus:
    if len(salasana)>0 and len(kayttajatunnus)>0:
        m=hashlib.sha512()
        m.update(salasana.encode("UTF-8"))
        syotettysala=m.hexdigest()
        if syotettysala==kayttajansala:
            session['kayttaja']="ok"
            return redirect(url_for('paasivu'))
        else:
            virhe=True

    if request.method=="POST":
        form=Kirjautuminen()
        form.validate()
    else:
        try:
            form=Kirjautuminen()
        except:
            return render_template('kirjautuminen.html', form=form)

# jos ei ollut oikea salasana niin pysytään kirjautumissivulla ja tehdään virheilmoitus
    return render_template('kirjautuminen.html', form=form, virhe=virhe)



#PÄÄSIVU:
#Tähän mennään kirjautumisen jälkeen
#Solmu 4: Avohyllyt
@app.route('/laakehuone', methods=['GET'])
@auth
def paasivu():
    #Haetaan tietokannasta mittaustiedot avohyllyistä:
    alue="Avohylly"
    laakehuone=mittaustenHaku(alue)
    #Alueen olosuhteet:
    tmaara=['Lämpötila', 'Ilmankosteus', 'Valoisuus', 'Ilmanpaine']
    session['huone']=4
    return render_template("paasivu.html", tmaara=tmaara, laakehuone=laakehuone)


#JÄÄKAAPPI:
#Solmu 2
@app.route('/jaakaappi', methods=['GET'])
@auth
def jaakaappi():
    #Haetaan tietokannasta mittaustiedot jääkaapista:
    alue="Jääkaappi"
    jaakaappi=mittaustenHaku(alue)
    #taulukoiden määrä:
    tmaara=[1,2]
    session['huone']=2
    return render_template("jaakaappi.html", tmaara=tmaara, jaakaappi=jaakaappi)


#INFUUSIONESTEKAAPPI:
#Solmu 3
@app.route('/infuusionestekaappi', methods=['GET'])
@auth
def infuusionestekaappi():
    #Haetaan tietokannasta mittaustiedot infuusionestelaatikosta:
    alue="Infuusionestelaatikko"
    infuusio=mittaustenHaku(alue)
    #Mahdolliset olosuhteet alueella:
    tmaara=['Lämpötila','Valoisuus']
    session['huone']=3
    return render_template("infuusioneste.html", tmaara=tmaara, infuusio=infuusio)

#OVELLINEN LÄÄKEKAAPPI:
#Solmu 1
@app.route('/ovellinenlaakekaappi', methods=['GET'])
@auth
def ovellinenlaakekaappi():
    #Haetaan tietokannasta mittaustiedot ovellisesta lääkekaapista:
    alue="Ovellinen lääkekaappi"
    ovilaakekaappi=mittaustenHaku(alue)
    #Mahdolliset olosuhteet alueella:
    tmaara=['Lämpötila']
    session['huone']=1
    return render_template("ovilaakekaappi.html", tmaara=tmaara, ovilaakekaappi=ovilaakekaappi)


#ULOS KIRJAUTUMINEN:
@app.route('/logout', methods=['GET'])
@auth
def logout():
    #Nollataan sessiot:
    session.pop('kayttaja', None)
    session.pop('lampotila', None)
    session.pop('kosteus', None)
    session.pop('valo', None)
    session.pop('ilmanpaine', None)
    session.pop('huone', None)
    return redirect(url_for('paasivu')) #ohjataan takaisin pääsivulle



#HAKUTOIMINTO:
@app.route('/haku', methods=['POST','GET'])
@auth
def haku():
    lista=[]
    datenow = datetime.now().strftime("%Y-%m-%d")
    #Hakulomake:
    class Hakulomake(FlaskForm):
        alue=SelectField('alue', choices=[('Avohylly'), ('Jääkaappi'), ('Infuusionestelaatikko'), ('Ovellinen lääkekaappi')])
        pvmA = DateField('pvmA', format='%Y-%m-%d')
        pvmL = DateField('pvmL', format='%Y-%m-%d')
        aikaA = TimeField('aikaA')
        aikaL = TimeField('aikaL')

    try:
        alue=request.form.get('alue', "")
        lista.append(alue); # lista[0]
    except:
        alue=""
    try:
        pvmA=request.form.get('pvmA', "")
        if(pvmA > datenow):
            pvmA = datenow
        lista.append(pvmA) # lista[1]

    except:
        pvmA=datetime.now().strftime("%Y-%m-%d") #%H:%M:%S"
    try:
        pvmL=request.form.get('pvmL', "")
        if(pvmL > datenow):
            pvmL = datenow
        lista.append(pvmL) # lista[2]
    except:
        pvmL=datetime.now().strftime("%Y-%m-%d")
    try:
        aikaA=request.form.get('aikaA', "")
        aikaNyt = datetime.now().strftime("%H:%M")
        if(pvmA == datenow and aikaA>aikaNyt):
            aikaA = aikaNyt
        lista.append(aikaA); # lista[3]
    except:
        aikaA=datetime.now().strftime("%H:%M")
    try:
        aikaL=request.form.get('aikaL', "")
        aikaNyt = datetime.now().strftime("%H:%M")
        if(pvmL == datenow and aikaL>aikaNyt):
            aikaL = aikaNyt
        lista.append(aikaL) # lista[4]
    except:
        aikaL=datetime.now().strftime("%H:%M")

    hakuTulokset = ""

    if request.method == "POST":
        lomake=Hakulomake()
        #haetaan tietokannasta mittaukset lomakkeeseen syötettyjen tietojen avulla ja esitetään ne käyttäjälle:
        hakuTulokset = hakutulokset(lista, lomake)
        return render_template('hakutulokset.html', hakutulokset = hakuTulokset, alue=lista[0])

    if request.method=="GET":
        lomake=Hakulomake()
        lomake.validate()



        return render_template('haku.html', lomake = lomake)

    return render_template("haku.html", lomake = lomake)

#Haetaan hakutulos-mittaukset:
def hakutulokset(lista, lomake):

    alue  = lista[0]
    aika_alku = lista[1]
    aika_alku += " "
    aika_alku += lista[3]
    aika_loppu = lista[2]
    aika_loppu += " "
    aika_loppu += lista[4]

    hakutulokset = ""
    try:
        con=pool.get_connection()
        cur=con.cursor(buffered=True, dictionary=True)
        sql="""
        SELECT mittaukset.mittauksen_datetime, mittaukset.mitattava_suure, mittaukset.tulos, mittaukset.kuitattu
        FROM mittaukset, sensorit, solmut
        WHERE mittaukset.mittauksen_datetime between %s and %s
        AND mittaukset.sensorin_id = sensorit.sensorin_id
        AND sensorit.solmun_id = solmut.solmun_id
        AND solmut.solmun_sijoituspaikka = %s;
        """
        #
        cur.execute(sql,(aika_alku, aika_loppu, alue))
        hakutulokset = cur.fetchall()
    except:
        return Response("Virhe tietokannassa")
        #return render_template('haku.html', lomake = lomake)

    finally:
        con.close()

    return hakutulokset

#SOLMUILTA TULEVIEN TIETOJEN TALLENNUS TIETOKANTAAN:
#ESP32-solmuilta tulevien tietojen tallentaminen tietokantaan:
def tallennetaanMittaus(solmu, solmun_tiedot):
    try:
        con=pool.get_connection()
        cur=con.cursor(buffered=True, dictionary=True)
        #Sama sql pohjana kaikille mittausten tallentamisille:
        sql="""INSERT INTO mittaukset (mittauksen_datetime, sensorin_id, mitattava_suure, tulos, poikkeus, kuitattu)
        VALUES(%s, %s, %s, %s, %s, %s);
        """
        #Solmu 1: Ovellinen lääkekaappi
        if(solmu==1):
            try:
                cur.execute(sql,(solmun_tiedot['aika'], solmun_tiedot['sidL1'], solmun_tiedot['suureL1'], solmun_tiedot['tulosL1'], solmun_tiedot['poikkeusL1'], solmun_tiedot['kuitattuL1']))
                con.commit()
                cur.execute(sql,(solmun_tiedot['aika'], solmun_tiedot['sidV'], solmun_tiedot['suureV'], solmun_tiedot['tulosV'], solmun_tiedot['poikkeusV'], solmun_tiedot['kuitattuV']))
                con.commit()
                cur.execute(sql,(solmun_tiedot['aika'], solmun_tiedot['sidI'], solmun_tiedot['suureI'], solmun_tiedot['tulosI'], solmun_tiedot['poikkeusI'], solmun_tiedot['kuitattuI']))
                con.commit()
                cur.execute(sql,(solmun_tiedot['aika'], solmun_tiedot['sidK'], solmun_tiedot['suureK'], solmun_tiedot['tulosK'], solmun_tiedot['poikkeusK'], solmun_tiedot['kuitattuK']))
                con.commit()
                cur.execute(sql,(solmun_tiedot['aika'], solmun_tiedot['sidO'], solmun_tiedot['suureO'], solmun_tiedot['tulosO'], solmun_tiedot['poikkeusO'], solmun_tiedot['kuitattuO']))
                con.commit()
                return "tietokantaan lukeminen onnistui"
            except:
                return "tietokantaan tallennus epäonnistui"
        #Solmu 2: Jääkaappi
        elif(solmu==2):
            try:
                cur.execute(sql,(solmun_tiedot['aika'], solmun_tiedot['sidL1'], solmun_tiedot['suureL1'], solmun_tiedot['tulosL1'], solmun_tiedot['poikkeusL1'], solmun_tiedot['kuitattuL1']))
                con.commit()
                cur.execute(sql,(solmun_tiedot['aika'], solmun_tiedot['sidL2'], solmun_tiedot['suureL2'], solmun_tiedot['tulosL2'], solmun_tiedot['poikkeusL2'], solmun_tiedot['kuitattuL2']))
                con.commit()
                cur.execute(sql,(solmun_tiedot['aika'], solmun_tiedot['sidO'], solmun_tiedot['suureO'], solmun_tiedot['tulosO'], solmun_tiedot['poikkeusO'], solmun_tiedot['kuitattuO']))
                con.commit()
                return "tietokantaan lukeminen onnistui"
            except:
                return "tietokantaan tallennus epäonnistui"
        #Solmu 3: Infuusionestelaatikko
        elif(solmu==3):
            try:
                cur.execute(sql,(solmun_tiedot['aika'], solmun_tiedot['sidL'], solmun_tiedot['suureL'], solmun_tiedot['tulosL'], solmun_tiedot['poikkeusL'], solmun_tiedot['kuitattuL']))
                con.commit()
                cur.execute(sql,(solmun_tiedot['aika'], solmun_tiedot['sidV'], solmun_tiedot['suureV'], solmun_tiedot['tulosV'], solmun_tiedot['poikkeusV'], solmun_tiedot['kuitattuV']))
                con.commit()
                return "tietokantaan lukeminen onnistui"
            except:
                return "tietokantaan tallennus epäonnistui"
        #Solmu 4: Avohyllyt
        elif(solmu==4):
            try:
                #Jos tarvii testata:
                #return str(solmun_tiedot['solmu']) +" "+ str(solmun_tiedot['aika'])+" "+ str(solmun_tiedot['sid'])+" "+ str(solmun_tiedot['suure'])+" "+str(solmun_tiedot['tulos'])
                cur.execute(sql,(solmun_tiedot['aika'], solmun_tiedot['sid'], solmun_tiedot['suure'], solmun_tiedot['tulos'], solmun_tiedot['poikkeus'], solmun_tiedot['kuitattu']))
                con.commit()
                return "tietokantaan lukeminen onnistui"
            except:
                return "tietokantaan tallennus epäonnistui"
    except Exception as err:
        return 'Virhe tietokantaan tallentamisessa'
    finally:
        con.close()






#Kaikkien solmujen mittausarvojen vastaanottaminen solmulta 4:
@app.route('/update-sensor') #methods=['GET']
def updatesensor():

    solmu=0
    solmunTiedot={}
    lista=[]


    #Vastaanotetaan solmun numero:
    if request.method=="GET":
        try:
            solmu=request.args.get("solmu")
            solmu=int(solmu)
            lista.append(str(solmu))
        except:
            solmu=0


        #Tarkistetaan, miltä solmulta saadaan mittausarvoja,
        #tarkistetaan, että saadaan kaikki solmuun kuuluvilta sensoreilta tietoja ja
        #yritetään tallentaa saadut arvot tietokantaan:
        match solmu:
            #Avohyllyt, solmu1:
            case 1:
                try:
                    listasuureet=[] #testausta varten
                    lampotila1=request.args.get("lampotila1")
                    valo=request.args.get("valo")
                    ilmanpaine=request.args.get("ilmanpaine")
                    kosteus=request.args.get("kosteus")
                    ovi=request.args.get("ovi")
                    if lampotila1 is not None and valo is not None and ilmanpaine is not None and kosteus is not None and ovi is not None:
                        lista.append(" Lampotila1: "+str(lampotila1) +" valo: " +str(valo) +" ilmanpaine: "+ilmanpaine +" kosteus: "+kosteus +" Ovi: "+str(ovi))
                        aika=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        #Määritellään, milloin kyseessä on poikkeus ja lähetetään hälytyssposti, jos arvo on poikkeava:
                        poikkeusL1=0
                        poikkeusV=0
                        poikkeusI=0
                        poikkeusK=0
                        poikkeusO=0
                        #Tarkistetaan onko arvo poikkeava ja lähetetään spostiin viesti poikkeuksesta:
                        if float(lampotila1)>23:
                            poikkeusL1=1
                            mittaustiedot={
                                'paikka':solmu,
                                'olosuhde':'lämpötila',
                                'tulos':lampotila1,
                                'aika':aika
                                }
                            virheSposti(mittaustiedot)

                        if int(valo)>4000:
                            poikkeusV=1
                            mittaustiedot={
                                'paikka':solmu,
                                'olosuhde':'valo',
                                'tulos':valo,
                                'aika':aika
                                }
                            virheSposti(mittaustiedot)

                        if int(ilmanpaine)>1028 or int(ilmanpaine)<1013:
                            poikkeusI=1
                            mittaustiedot={
                                'paikka':solmu,
                                'olosuhde':'ilmanpaine',
                                'tulos':ilmanpaine,
                                'aika':aika
                                }
                            virheSposti(mittaustiedot)

                        if int(kosteus)>70 or int(kosteus)<45:
                            poikkeusK=1
                            mittaustiedot={
                                'paikka':solmu,
                                'olosuhde':'ilmankosteus',
                                'tulos':kosteus,
                                'aika':aika
                                }
                            virheSposti(mittaustiedot)

                        if int(ovi)!=0:
                            poikkeusO=1
                            mittaustiedot={
                                'paikka':solmu,
                                'olosuhde':'ovi',
                                'tulos':ovi,
                                'aika':aika
                                }
                            virheSposti(mittaustiedot)

                        #Lähetetään kaikki solmuun liittyvät tiedot tietokantaan tallennusta varten:
                        solmun_tiedot = {
                            'solmu': solmu,
                            'aika': aika,
                            'sidL1': 101001,
                            'suureL1': 'lämpötila',
                            'tulosL1': lampotila1,
                            'poikkeusL1':poikkeusL1,
                            'kuitattuL1':0,
                            'sidV': 101002,
                            'suureV': 'valo',
                            'tulosV': valo,
                            'poikkeusV':poikkeusV,
                            'kuitattuV':0,
                            'sidI': 101001,
                            'suureI': 'ilmanpaine',
                            'tulosI': ilmanpaine,
                            'poikkeusI':poikkeusI,
                            'kuitattuI':0,
                            'sidK': 101001,
                            'suureK': 'ilmankosteus',
                            'tulosK': kosteus,
                            'poikkeusK':poikkeusK,
                            'kuitattuK':0,
                            'sidO': 101003,
                            'suureO': 'ovi',
                            'tulosO': ovi,
                            'poikkeusO':poikkeusO,
                            'kuitattuO':0
                            }

                        if solmun_tiedot is not None:
                            teksti=tallennetaanMittaus(solmu, solmun_tiedot)
                            return Response(teksti)

                    else:
                        return "ei syötetty kaikkia solmu1:n arvoja"
                except:
                    return "virhe"
            #Jääkaappi, solmu2:
            case 2:
                try:
                    lampotila1=request.args.get("lampotila1")
                    lampotila2=request.args.get("lampotila2")
                    ovi=request.args.get("ovi")
                    if lampotila1 is not None and lampotila2 is not None and ovi is not None:
                        aika=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        #id 1:ylä temp, id 2: ala temp

                        #Määritellään, milloin kyseessä on poikkeus:
                        poikkeusL1=0
                        poikkeusL2=0
                        poikkeusO=0
                        #Tarkistetaan onko arvo poikkeava ja lähetetään spostiin viesti poikkeuksesta:
                        if float(lampotila1)>8 or float(lampotila1)<2:
                            poikkeusL1=1
                            mittaustiedot={
                                'paikka':solmu,
                                'olosuhde':'lämpötila',
                                'tulos':lampotila1,
                                'aika':aika
                                }
                            virheSposti(mittaustiedot)

                        if float(lampotila2)>8 or float(lampotila2)<2:
                            poikkeusL2=1
                            mittaustiedot={
                                'paikka':solmu,
                                'olosuhde':'lämpötila',
                                'tulos':lampotila2,
                                'aika':aika
                                }
                            virheSposti(mittaustiedot)
                        if int(ovi)!=0:
                            poikkeusO=1
                            mittaustiedot={
                                'paikka':solmu,
                                'olosuhde':'ovi',
                                'tulos':ovi,
                                'aika':aika
                                }
                            virheSposti(mittaustiedot)

                        #Lähetetään kaikki solmuun liittyvät tiedot tietokantaan tallennusta varten:
                        solmun_tiedot = {
                            'solmu': solmu,
                            'aika': aika,
                            'sidL1': 102001,
                            'suureL1': 'lämpötila',
                            'tulosL1': lampotila1,
                            'poikkeusL1':poikkeusL1,
                            'kuitattuL1':0,
                            'sidL2': 102002,
                            'suureL2': 'lämpötila',
                            'tulosL2': lampotila2,
                            'poikkeusL2':poikkeusL2,
                            'kuitattuL2':0,
                            'sidO': 102003,
                            'suureO': 'ovi',
                            'tulosO': ovi,
                            'poikkeusO':poikkeusO,
                            'kuitattuO':0
                            }

                        if solmun_tiedot is not None:
                            teksti=tallennetaanMittaus(solmu, solmun_tiedot)
                            return Response(teksti)

                    else:
                        return "ei syötetty kaikkia solmu2:n arvoja"
                except:
                    return "virhe"
            #Infuusionesteet, solmu3:
            case 3:
                try:
                    lampotila1=request.args.get("lampotila1")
                    valo=request.args.get("valo")
                    if lampotila1 is not None and valo is not None:
                        lista.append(" Lampotila1: "+str(lampotila1)+" valo: "+str(valo))
                        aika=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        #Määritellään, milloin kyseessä on poikkeus:
                        poikkeusL=0
                        poikkeusV=0
                        #Tarkistetaan onko arvo poikkeava ja lähetetään spostiin viesti poikkeuksesta:
                        if float(lampotila1)>23:
                            poikkeusL=1
                            mittaustiedot={
                                'paikka':solmu,
                                'olosuhde':'lämpötila',
                                'tulos':lampotila1,
                                'aika':aika
                                }
                            virheSposti(mittaustiedot)
                        if int(valo)>4000:
                            poikkeusV=1
                            mittaustiedot={
                                'paikka':solmu,
                                'olosuhde':'valo',
                                'tulos':valo,
                                'aika':aika
                                }
                            virheSposti(mittaustiedot)
                        #Lähetetään kaikki solmuun liittyvät tiedot tietokantaan tallennusta varten:
                        solmun_tiedot = {
                            'solmu': solmu,
                            'aika': aika,
                            'sidL': 103001,
                            'suureL': 'lämpötila',
                            'tulosL': lampotila1,
                            'poikkeusL':poikkeusL,
                            'kuitattuL':0,
                            'sidV': 103002,
                            'suureV': 'valo',
                            'tulosV': valo,
                            'poikkeusV':poikkeusV,
                            'kuitattuV':0
                            }

                        if solmun_tiedot is not None:
                            teksti=tallennetaanMittaus(solmu, solmun_tiedot)
                            return Response(teksti)

                    else:
                        return "ei syötetty kaikkia solmu3:n arvoja"
                except:
                    return "virhe"

            #Ovellinen lääkekaappi, solmu4:
            case 4:
                try:
                    lampotila1=request.args.get("lampotila1")
                    if lampotila1 is not None:
                        lista.append(" Lampotila1: "+str(lampotila1))
                        aika=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        #Määritellään, milloin kyseessä on poikkeus:
                        poikkeus=0
                        #Tarkistetaan onko arvo poikkeava ja lähetetään spostiin viesti poikkeuksesta:
                        if float(lampotila1)>23:
                            poikkeus=1
                            mittaustiedot={
                                'paikka':solmu,
                                'olosuhde':'lämpötila',
                                'tulos':lampotila1,
                                'aika':aika
                                }
                            virheSposti(mittaustiedot)
                        #Lähetetään kaikki solmuun liittyvät tiedot tietokantaan tallennusta varten:
                        solmun_tiedot = {
                            'solmu': solmu,
                            'aika': aika,
                            'sid': 104001,
                            'suure': 'lämpötila',
                            'tulos': lampotila1,
                            'poikkeus':poikkeus,
                            'kuitattu':0
                            }
                        if solmun_tiedot is not None:
                            teksti=tallennetaanMittaus(solmu, solmun_tiedot)
                            return Response(teksti)

                    else:
                        return "ei syötetty kaikkia solmun4:n arvoja"
                except:
                    return "virhe"
            #Jos solmua ei olemassa:
            case other:
                return "solmun arvo oltava 1-4 väliltä"

    return Response(lista)

#POPUP:
poikkeukset=[] #kaikki tietokannasta löytyvät poikkeavat arvot, joita ei vielä olla kuitattu

def poikkeustenHaku():
    try:
        con=pool.get_connection()
        cur=con.cursor(buffered=True, dictionary=True)

        #Valitaan vain tänään mitatut arvot, jotka ovat poikkeavia ja niitä ei olla kuitattu:
        aika=datetime.now().strftime("%Y-%m-%d")
        sql="""SELECT so.solmun_sijoituspaikka AS paikka, so.sensorit, m.mittauksen_datetime AS aika, m.tulos, m.mittauksen_id, m.mitattava_suure AS olosuhde, s.sensorin_id AS sid, m.poikkeus, m.kuitattu
        FROM solmut so
        JOIN sensorit s
        ON s.solmun_id=so.solmun_id
        JOIN mittaukset m
        ON m.sensorin_id=s.sensorin_id AND DATE(mittauksen_datetime)= %s AND m.poikkeus= %s AND m.kuitattu= %s
        ORDER BY TIME(mittauksen_datetime);
        """

        cur.execute(sql,(aika, 1, 0))
        poikkeukset=cur.fetchall()
        return poikkeukset

    except Exception as err:
        return "Virhe tietokannan käytössä"
    finally:
        con.close()

    return "poikkeusten haku ei onnistunut"






#POPUP: javascript hakee tämän urlin ja luo tämän avulla popupin!
@app.route('/popup')
def popup():
    #Haetaan poikkeukset tietokannasta ja lähetetään ne yksikerrallaan javascript-puolelle
    palaute=poikkeustenHaku()
    if len(palaute)>0:
        tulos=palaute.pop()
        return jsonify(tulos)

    return Response(str(poikkeukset))

#POPUP:hälytyksen kuittaus
#Päivitetään tieto kuittauksesta, hälytyksen aiheuttaneen mittauksen tietoihin:
def kuitataanMittaus(id, aika):
    try:

        con=pool.get_connection()
        cur=con.cursor(buffered=True, dictionary=True)

        sql="""UPDATE mittaukset
        SET kuitattu=%s, kuittaus_aika=%s
        WHERE mittauksen_id=%s;
        """
        cur.execute(sql,(1, aika, id))
        con.commit()

    except Exception as err:
        return "Virhe tietokannan käytössä"
    finally:
        con.close()

#Tullaan tähän urliin, kun painettu popupissa kuittaa-painonappia:
@app.route('/kuittaus')
def kuittaus():
    aika=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #tietokantaan kuittaus kuntoon:
    try:
        id=request.args.get('mittaus', 0)
        alue=request.args.get('alue', '')
        if alue=='laakehuone':
            alue='paasivu'
    except:
        id=0
    if int(id)>0:
        #Päivitetään tieto mittauksen kuittauksesta tietokantaan:
        kuitataanMittaus(int(id), aika)
    #Palataan takaisin sille sivulle, jolla oltiin popupin ilmestyessä:
    return redirect(url_for(alue))





