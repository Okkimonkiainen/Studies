
package urheilupaivakirja;

/**
 *
 * @author Ella Rauma ja Tiina Tuomisto
 */
public class Paikka {
    String kaupunki;
    //String sali;

    public Paikka() {
    }

    public Paikka(String kaupunki) {
        this.kaupunki = kaupunki;
    }

    @Override
    public String toString() {
        return kaupunki;
    }
    
    
    
}
