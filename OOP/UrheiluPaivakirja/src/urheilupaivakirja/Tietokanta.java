package urheilupaivakirja;

import java.util.ArrayList;

/**
 *
 * @author Ella Rauma ja Tiina Tuomisto
 */
public class Tietokanta {
    ArrayList<Suoritus> suoritukset;
    
    public Tietokanta(){
        this.suoritukset= new ArrayList<>();
    }
    
    public void lisaaSuoritus(Kayttaja k, Aika a, Laji l, Paikka p){
        int i=0;
        if(l.nimi.equals("Jalkapallo") || l.nimi.contains("Koripallo") || l.nimi.contains("Tennis")){
            i=1;
        }
        else if(l.nimi.equals("Juoksu") || l.nimi.equals("Pyöräily") || l.nimi.equals("Uinti") || l.nimi.equals("Sulkapallo")){
        i=2;
        }
        else if(l.nimi.equals("Kävely")){
            i=3;
        }
        else{
            i=4;
        }
        
        suoritukset.add(new Suoritus(k, a, l, p, i));
    }
    
        
    public Suoritus etsiSuoritus(int arvo){
        return suoritukset.get(arvo);
    }    
    
    public void poistaSuoritus(int n){ 
        suoritukset.remove(n);
      
    }
    
    
}
