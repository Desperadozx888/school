//Name: NIAMA CB 
//Student no: 69696969
//Tutorial Group: T100
//Declaration: This is not my own code
//Filename: NIAMA_CB_A1.java
//Objective: Create a Zodiac info with the properties of set with a system to calculate randomly generated sets

import java.util.*;

public class NIAMA_CB_A1 {
    private static final Scanner scanner = new Scanner(System.in);
    private static Random random = new Random();
    private static Set setA, setB, setC;
    private static boolean quit = false;

    public static void main(String[] args) {
        displayZodiacInfo();
        displayMenu();
    }

    //Print Zodiac Info
    private static void displayZodiacInfo() {
        System.out.printf("Universal set info%n%n");
        System.out.printf("%-15s%-15s%-15s%-15s%n", "Zodiac Sign", "Known as", "From Date", "To Date");
        for (Zodiac zodiac : Zodiac.values())
            System.out.printf("%-15s%-15s%-15s%-15s%n", zodiac, zodiac.getAbbreviation(), zodiac.getStartingDate(), zodiac.getEndingDate());

    }

    //Generate a random Element
    private static Zodiac getAnElement() {
        Random random = new Random();
        Zodiac zodiacs[] = Zodiac.values();
        //Return a random zodiac
        return zodiacs[random.nextInt(zodiacs.length)];
    }

    //Generate a random set of elements
    private static Set getASet() {
        Random random = new Random();
        int randInt = random.nextInt(Zodiac.values().length);
        Set s = new Set();
        while (s.cardinality() < randInt) {
            Zodiac zodiac = getAnElement();
            if (!s.belongTo(zodiac))
                s.addElement(zodiac);
        }
        //Returns a random Set of Elements
        return s;
    }

    //Display Menu
    private static void displayMenu() {
        while (!quit) { //The while loop is false at the start of the program to keep the program running in a loop until the user press 9 to quit the program.

            System.out.printf("%nWelcome to SIM set Theory lesson%n%n");
            System.out.printf("0: Properties of Set%n");
            System.out.printf("1: Union example%n");
            System.out.printf("2: Intersection Example%n");
            System.out.printf("3: Subset Example%n");
            System.out.printf("4: Difference Example%n");
            System.out.printf("5: Complement Example%n");
            System.out.printf("6: Sets Equality Example%n");
            System.out.printf("7: Distributive Law 1%n");
            System.out.printf("8: Distributive Law 2%n");
            System.out.printf("9: Quit%n%n");

            System.out.printf("Your option: ");
            try {
                int input = scanner.nextInt();
                scanner.nextLine();


                switch (input) {
                    case 0:
                        //Initialize a new random Set for submenu and its functions
                        setA = getASet();
                        displaySubmenu();
                        break;
                    case 1:
                        unionExample();
                        break;
                    case 2:
                        intersectionExample();
                        break;
                    case 3:
                        subsetExample();
                        break;
                    case 4:
                        differenceExample();
                        break;
                    case 5:
                        complementExample();
                        break;
                    case 6:
                        equalityExample();
                        break;
                    case 7:
                        distributiveLaw1();
                        break;
                    case 8:
                        distributiveLaw2();
                        break;
                    case 9:
                        quit = true;
                        break;
                    default:
                        System.out.printf("No such Option, Please Enter Your Option again!%n");
                        System.out.printf("-----------------------------------------------------------------------------%n%n");
                        displayMenu();
                        break;
                }
            } catch (Exception exception) {
                System.out.printf("Please Enter a number only%n");
                scanner.next();
            }
            System.out.printf("-----------------------------------------------------------------------------%n%n");
        }
    }

    //Union (Option 1)
    public static void unionExample() {
        //Initialize a new random Set
        setA = getASet();
        setB = getASet();

        System.out.printf("%nGiven sets%n");
        System.out.printf("%-8sA = %s%n", "", setA);
        System.out.printf("%-8sB = %s%n", "", setB);
        setA.union(setB);
        System.out.printf("%-8sUnion of A and B = %s%n", "", setA);


    }

    //In both A & B (Option 2)
    public static void intersectionExample() {
        //Initialize a new random Set
        setA = getASet();
        setB = getASet();

        System.out.printf("%nGiven sets%n");
        System.out.printf("%-8sA = %s%n", "", setA);
        System.out.printf("%-8sB = %s%n", "", setB);
        setA.intersection(setB);
        System.out.printf("%-8sBIntersection of A and B = %s%n", "", setA);

    }

    //Every element of A is in B (Option 3)
    public static void subsetExample() {
        //Initialize a new random Set
        setA = getASet();
        setB = getASet();

        System.out.printf("%nGiven Sets%n");
        System.out.printf("%-8sA = %s%n", "", setA);
        System.out.printf("%-8sB = %s%n", "", setB);

        System.out.printf("%nConclusion%n");

        System.out.printf("%-8sA subset of B: %s%n", "", setA.subSet(setB));
        System.out.printf("%-8sB subset of A: %s%n", "",setB.subSet(setA));

    }

    //A - B (Option 4)
    public static void differenceExample() {
        //Initialize a new random Set
        setA = getASet();
        setB = getASet();

        System.out.printf("%-8sA = %s%n", "", setA);
        System.out.printf("%-8sB = %s%n%n", "", setB);

        setA.difference(setB);
        System.out.printf("%-8sA - B = %s%n","" , setA);
    }


    //Elements not in A (Option 5)
    public static void complementExample() {
        //Initialize a new random Set
        setA = getASet();
        System.out.printf("%nGiven sets%n");
        System.out.printf("%-8sA = %s%n%n", "",setA);
        System.out.printf("%-8sA' = %s%n", "",setA.complement());

    }

    //Both sets have the same Elements
    public static void equalityExample() {
        //Initialize a new random Set
        setA = getASet();
        setB = getASet();

        System.out.printf("%nGiven Sets%n");
        System.out.printf("%-8sA = %s%n", "", setA);
        System.out.printf("%-8sB = %s%n", "", setB);

        System.out.printf("%nAnalysis%n");
        System.out.printf("%-8sA is a subset of B: %s%n", "",setA.subSet(setB));
        System.out.printf("%-8sB is a subset of A: %s%n", "",setB.subSet(setA));

        System.out.printf("%nConclusion%n");
        System.out.printf("%-8sA equals to B: %s%n", "",setA.equality(setB));


    }

    //A ∪ (B ∩ C) = (A ∪ B) ∩ (A ∪ C)
    public static void distributiveLaw1() {
        ////Initialize a new random Set
        setA = getASet();
        setB = getASet();
        setC = getASet();

        //Print distributive law 1
        System.out.printf("We wish to prove: A ∪ (B I C) = (A ∪ B) I (A ∪ C)%n");

        //Print given Sets
        System.out.printf("%nGiven Sets%n");
        System.out.printf("%-8s%s%s%n", "", "A = ", setA);
        System.out.printf("%-8s%s%s%n", "", "B = ", setB);
        System.out.printf("%-8s%s%s%n%n", "", "C = ", setC);

        //Declare of LHS A,B,C
        Set lhsA = new Set(setA);
        Set lhsB = new Set(setB);
        Set lhsC = new Set(setC);
        //(B ∩ C)
        lhsB.intersection(lhsC);
        //A ∪ (B ∩ C)
        lhsA.union(lhsB);

        //Declare LHS instance
        Set lhsSet = new Set(lhsA);

        //Print LHS
        System.out.printf("LHS analysis%n");
        System.out.printf("%-8s%s%s%n%n", "", "LHS = ", lhsSet);

        //Declare of RHS A,B,C
        Set rhsA1 = new Set(setA);
        Set rhsA2 = new Set(setA);
        Set rhsB = new Set(setB);
        Set rhsC = new Set(setC);

        //(A ∪ B)
        rhsA1.union(rhsB);
        //(A ∪ B)
        rhsA2.union(rhsC);
        //(A ∪ B) ∩ (A ∪ C)
        rhsA1.intersection(rhsA2);

        //Declare RHS Instance
        Set rhsSet = new Set(rhsA1);

        //Print RHS
        System.out.printf("RHS analysis%n");
        System.out.printf("%-8s%s%s%n%n", "", "RHS = ", rhsSet);

        //Print Conclusion
        System.out.printf("Conclusion%n");
        System.out.printf("%-8s%s%s%n", "", "LHS = RHS is ", lhsSet.equality(rhsSet));


    }

    //A ∪ (B ∩ C) = (A ∪ B) ∩ (A ∪ C)
    public static void distributiveLaw2() {
        ////Initialize a new random Set
        setA = getASet();
        setB = getASet();
        setC = getASet();

        //Print Distributive Law 2
        System.out.printf("We wish to prove: A I (B ∪ C) = (A I B) ∪ (A I C)%n");

        //Print given Sets
        System.out.printf("%nGiven Sets%n");
        System.out.printf("%-8s%s%s%n", "", "A = ", setA);
        System.out.printf("%-8s%s%s%n", "", "B = ", setB);
        System.out.printf("%-8s%s%s%n%n", "", "C = ", setC);

        //Declare LHS instances
        Set lhsA = new Set(setA);
        Set lhsB = new Set(setB);
        Set lhsC = new Set(setC);

        //(B ∪ C)
        lhsB.union(lhsC);
        //A ∩ (B ∪ C)
        lhsA.intersection(lhsB);

        //Declare LHS instance
        Set lhsSet = new Set(lhsA);

        //Print LHS
        System.out.printf("LHS analysis%n");
        System.out.printf("%-8s%s%s%n%n", "", "LHS = ", lhsSet);

        //Declare RHS variables
        Set rhsA1 = new Set(setA);
        Set rhsA2 = new Set(setA);
        Set rhsB = new Set(setB);
        Set rhsC = new Set(setC);

        //(A ∩ B)
        rhsA1.intersection(rhsB);
        //(A ∩ C)
        rhsA2.intersection(rhsC);
        //A ∩ (B ∪ C) = (A ∩ B) ∪ (A ∩ C)
        rhsA1.union(rhsA2);

        //Declare RHS instance
        Set rhsSet = new Set(rhsA1);

        //Print RHS
        System.out.printf("RHS analysis%n");
        System.out.printf("%-8s%s%s%n%n", "", "RHS = ", rhsSet);

        //Conclusion
        System.out.printf("Conclusion%n");
        System.out.printf("%-8s%s%s%n", "", "LHS = RHS is ", lhsSet.equality(rhsSet));


    }


    private static void displaySubmenu() {
        while (!quit) {//The while loop is false at the start of the program to keep the program running in a loop until the user press 9 to return to the displayMenu before pressing 9 at displayMenu to quit

            anExample();

            System.out.printf("Some basic operations in set%n");
            System.out.printf("%-8s%s%n", "", "1: Add an element");
            System.out.printf("%-8s%s%n", "", "2: Check an element");
            System.out.printf("%-8s%s%n", "", "3: Cardinality");
            System.out.printf("%-8s%s%n", "", "4: Enum format");
            System.out.printf("%-8s%s%n%n", "", "9: Quit");
            System.out.printf("Enter your option: ");

            try {
                int input = scanner.nextInt();
                scanner.nextLine();

                //Declare variables
                String zodiacElement;
                boolean exist = false;

                switch (input) {
                    //Declare variables
                    case 1:
                        //Add an Element
                        //While condition is false the loop will continue
                        do {
                            System.out.printf("%nEnter an element: ");
                            zodiacElement = scanner.next();
                            scanner.nextLine();
                            //Check if Zodiac Element input is equals to Enum
                            for (Zodiac zodiac : Zodiac.values()) {
                                if (zodiacElement.equals(zodiac.toString())) {
                                    exist = true;
                                    //Condition is true, exit Loop
                                }
                            }
                        } while (!exist); //While condition is false enter loop
                        setA.addElement(Zodiac.valueOf(zodiacElement));
                        System.out.printf("A = %s%n", setA);
                        break;
                    case 2:
                        //Check if an element is in set
                        //While condition is false the loop will continue
                        do {
                            System.out.printf("%nEnter an element: ");
                            zodiacElement = scanner.next();
                            scanner.nextLine();
                            //Check if Zodiac Element input is equals to Enum
                            for (Zodiac zodiac : Zodiac.values()) {
                                if (zodiacElement.equals(zodiac.toString())) {
                                    exist = true;
                                    //Condition is true, exit Loop
                                }
                            }
                        } while (!exist); //While condition is false enter loop
                        //If set element belong to set A
                        if (!(setA.belongTo(Zodiac.valueOf(zodiacElement)))) {
                            System.out.printf("Element %s is not in set%n", zodiacElement);
                        } else {//If element does not belong to set A
                            System.out.printf("Element %s is in set%n", zodiacElement);
                        }
                        break;
                    case 3:
                        //Display the cardinal number of the set
                        System.out.printf("%nNo of elements in set is %d%n", setA.cardinality());
                        break;
                    case 4:
                        //Convert the Abbreviation to Element
                        System.out.printf("%nNotation in enum format%n");
                        System.out.printf("A = %s%n", setA.getEnumFormat());
                        break;
                    case 9:
                        displayMenu();
                        break;
                    default:
                        //Any other values will return back to submenu
                        System.out.printf("No such Option, Please Enter Your Option again!%n%n");
                        System.out.printf("-----------------------------------------------------------------------------%n%n");
                        displaySubmenu();
                        break;
                }
            } catch (Exception exception) {
                System.out.printf("Please Enter a number only%n");
                scanner.next();
            }
            System.out.printf("-----------------------------------------------------------------------------%n%n");
        }
    }

    //Print an Example
    public static void anExample() {
        System.out.printf("%nHere is an example of set%n");
        System.out.printf("%-8sA = %s%n", "", setA);
        System.out.printf("%-8s%s%n%n", "", "ALl elements in set are distinct and random order");
    }
}

class Set {
    //Instance variables
    private final ArrayList<Zodiac> s;

    //Constructor
    public Set() {
        this.s = new ArrayList<Zodiac>();
    }

    //Copy Constructor
    public Set(Set otherSet) {
        this.s = new ArrayList<Zodiac>(otherSet.s);
    }

    //Getter
    public ArrayList<Zodiac> getS() {
        return this.s;
    }

    //Check if s isEmpty.
    public boolean isEmpty() {
        return this.s.isEmpty();
    }

    //Return Set Size
    public int cardinality() {
        return this.s.size();
    }

    //Check if S have the element
    public boolean belongTo(Zodiac element) {
        return s.contains(element);
    }

    //Add Element to s
    public void addElement(Zodiac element) {
        if (belongTo(element) == false) {
            this.s.add(element);
        }
    }


    //every element of A is in B
    public boolean subSet(Set otherSet) {
        if (otherSet.cardinality() > cardinality()) {
            return false;
        } else {
            return this.s.containsAll(otherSet.getS());
        }
    }

    //Union: in A or B (or both)
    public void union(Set otherSet) {
        for (Zodiac zodiac : otherSet.s) {
            if (!this.s.contains(zodiac))
                this.s.add(zodiac);
        }
    }

    //Intersection: in both A and B
    public void intersection(Set otherSet) {
        this.s.retainAll(otherSet.getS());
    }

    //Difference: in A but not in B
    public void difference(Set otherSet) {
        this.s.removeAll(otherSet.getS());

    }

    //Returns the string of the Enum instead of the abbreviation
    public String getEnumFormat() {
        String enumString = "";
        int count = 0;
        //If Set is not empty print { ArrayList } else { }
        if (!isEmpty()) {
            System.out.printf("{");
            for (Zodiac zodiac : s) {
                if (count == (this.s.size() - 1)) {
                    enumString = enumString + String.format("%s", zodiac);
                } else {
                    enumString = enumString + String.format("%s, ", zodiac);
                }
                count++;
            }
        } else {
            enumString = String.format("{ }");
        }

        return enumString;
    }

    public Set complement() {
        Set set = new Set();
        Zodiac[] z = Zodiac.values();
        for (Zodiac zodiac : z) {
            set.addElement(zodiac);
        }

        set.getS().removeAll(this.s);
        return set;
    }

    //Check if s = otherSet
    public boolean equality(Set otherSet) {
        //Check if s is equal to otherSet
        if (this.s.equals(otherSet.getS()) && otherSet.getS().equals(this.s)) {
            return true;
        } else
            return false;
    }

    //Returns the string representation of the Set
    public String toString() {
        String abbreviation = "";
        int count = 0;
        //If Set is not empty print { ArrayList } else { }
        if (!isEmpty()) {
            System.out.printf("{");

            for (Zodiac zodiac : s) {
                if (count == s.size() - 1) {
                    abbreviation = abbreviation + String.format("%s}", zodiac.getAbbreviation());
                } else {
                    abbreviation = abbreviation + String.format("%s, ", zodiac.getAbbreviation());
                }
                count++;
            }
        } else {
            abbreviation = String.format("{ }");
        }
        return abbreviation;
    }
}

enum Zodiac {
    //Declare constants of enum type
    Aries("ARI", "March 21", "April 19"),
    Taurus("TAU", "April 20", "May 20"),
    Gemini("GEM", "May 21", "June 20"),
    Cancer("CAN", "June 21", "July 22"),
    Leo("LEO", "July 23", "August 23"),
    Virgo("VIR", "August 23", "September 22"),
    Libra("LIB", "September 23", "October 22"),
    Scorpio("SCO", "October 23", "November 21"),
    Sagittarius("SAG", "November 22", "December 21"),
    Capricorn("CAP", "December 22", "January 19"),
    Aquarius("AQU", "January 20", "March 20"),
    Pisces("PIS", "February 19", "March 20");

    //Instance variables
    private final String abbreviation;
    private final String startingDate;
    private final String endingDate;


    //Constructor
    Zodiac(String abbreviation, String startingDate, String endingDate) {
        this.abbreviation = abbreviation;
        this.startingDate = startingDate;
        this.endingDate = endingDate;
    }

    //Getter
    public String getAbbreviation() {
        return abbreviation;
    }

    public String getStartingDate() {
        return startingDate;
    }

    public String getEndingDate() {
        return endingDate;
    }

}