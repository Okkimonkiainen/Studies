package urheilupaivakirja;

/**
 *
 * @author Ella Rauma ja Tiina Tuomisto
 */
public class UrheiluPaivakirja {
   
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        Tietokanta t = new Tietokanta();
        
        Kayttaja k = new Kayttaja();
        k.ika=20;
        k.nimi="Sonja";
        k.paino=65.3;
        k.pituus=175;
        
        Aika a = new Aika();
        a.pvm="123"; 
        a.kesto="3h40min";
        
        Laji l = new Laji();
        l.nimi="Jalkapallo";
        
        Paikka p = new Paikka();
        p.kaupunki="Tampere";
        
        t.lisaaSuoritus(k, a, l, p);
       // t.naytaSuoritukset();
        
        String m="Sonja";
        String n="Mika";
       // t.etsiSuoritus(n);
        
        
        
        Kayttaja k2 = new Kayttaja();
        k2.ika=30;
        k2.nimi="Niko";
        k2.paino=85;
        k2.pituus=180;
        
        Aika a2 = new Aika();
        a2.pvm="654"; 
        a2.kesto="6h20min";
        
        Laji l2 = new Laji();
        l2.nimi="Tennis";
        
        Paikka p2 = new Paikka();
        p2.kaupunki="Helsinki";
        
        t.lisaaSuoritus(k2, a2, l2, p2);
       
        // t.naytaSuoritukset();
        
        //t.poistaSuoritus(0); //POISTETAAN SONJA
        //poistaSuoritus-metodissa tulostuu suoraan paivittynyt lista
    }
    
}
