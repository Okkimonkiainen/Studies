package urheilupaivakirja;

/**
 *
 * @author Ella Rauma ja Tiina Tuomisto
 */
public class Kayttaja {
    String nimi;
    int ika;
    double pituus;
    double paino;

    public Kayttaja() {
    }

    public Kayttaja(String nimi, int ika, double pituus, double paino) {
        this.nimi = nimi;
        this.ika = ika;
        this.pituus = pituus;
        this.paino = paino;
    }

    @Override
    public String toString() {
        return nimi + ", ikä=" + ika + ", pituus=" + pituus + ", paino= " + paino;
    }
    
    
}
