package urheilupaivakirja;

/**
 *
 * @author Ella Rauma ja Tiina Tuomisto
 */
public class Aika {
    String pvm;
    String kesto;

    public Aika() {
    }

    public Aika(String pvm, String kesto) {
        this.pvm = pvm;
        this.kesto= kesto;
    }

    @Override
    public String toString() {
        return " kesto="+kesto+"," + "pvm="+pvm;
    }
    
    
}
