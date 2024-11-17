package urheilupaivakirja;

/**
 *
 * @author Ella Rauma ja Tiina Tuomisto
 */
public class Laji {

    String nimi;

    public Laji() {
    }

    public Laji(String nimi) {
        this.nimi = nimi;

    }

    @Override
    public String toString() {
        return ", lajin nimi="+nimi;
    }
    
    
}
