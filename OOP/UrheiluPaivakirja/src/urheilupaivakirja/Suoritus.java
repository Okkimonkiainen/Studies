package urheilupaivakirja;

/**
 *
 * @author Ella Rauma ja Tiina Tuomisto
 */
public class Suoritus implements Intensiteetti {
    Kayttaja kayttaja;
    Aika aika;
    Laji laji;
    Paikka paikka;
    String intensiteetti;
    
    public Suoritus() {
    }
    


    public Suoritus(Kayttaja kayttaja, Aika aika, Laji laji, Paikka paikka, int n) {
        this.kayttaja = kayttaja;
        this.aika = aika;
        this.laji = laji;
        this.paikka = paikka;
        this.intensiteetti=intensiteettiArvo(n);
        
    }

    @Override
    public String toString() {
        return "SUORITUS: " + "kayttaja=" + kayttaja + ", aika=" + aika + ", laji=" + laji + ", paikka=" + paikka + ", intensiteetti=" + intensiteetti;
    }
    
    public String intensiteettiArvo(int n){
        String teksti="";
        if(n==1){
            teksti="Raskas";
        }
        else if(n==2){
            teksti="Kohtalainen";
        }
        else if(n==3){
            teksti="Kevyt";
        }
        else{
            teksti="Ei voida arvioida";
        }
        
        return teksti;
    }
    
    
}
