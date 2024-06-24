//Name: Chow Keiren
//Student no: 10227382
//Tutorial Group: T09
//Declaration: This is my own code. Please do give feedback on code format if needed

//Filename: Chow_Keiren_A2.java
//Objective: Create a random number of 3D or 2D object for a random number times in a arraylist

import java.util.ArrayList;
import java.util.Random;

public class Chow_Keiren_A2 {
    private static boolean quit = false;

    public static void main(String[] args) {
        // declare ArrayList
        ArrayList<Shape> shapeArrayList = new ArrayList<Shape>();
        while (!quit) {//The while loop is false at the start of the program to keep the program running in a loop until the quit is true
            int k = (int) (Math.random() * 3);
            switch (k) {
                case 0:
                    displayList(shapeArrayList);
                    quit = true;
                    break;
                case 1:
                    shapeArrayList.add(getTwoD());
                    break;
                case 2:
                    shapeArrayList.add(getThreeD());
                    break;
            }
        }

    }

    //a method generates and returns a positive integer, not too large
    private static int getInt() {
        return (int) ((Math.random() * 10.0) + 1.0);
    }

    //a method generates and returns a positive real number, not too large
    private static double getDouble() {
        return ((Math.random() * 10.0) + 1.0);
    }

    //a method generates and returns a color.
    private static ShapeColor getColor() {
        Random random = new Random();
        ShapeColor shapeColors[] = ShapeColor.values();
        //Return a random Shape Color
        return shapeColors[random.nextInt(shapeColors.length)];
    }

    //Method to check if the triangle is true as negative sides cannot be a triangle at all
    private static boolean isTriangle(int a, int b, int c) {
        return ((a + b > c) && (b + c > a) && (c + a > b));
    }

    private static TwoD getTwoD() {
        //Declare instances
        TwoD twoD;
        //Generate random integer up to 4
        switch ((int) (Math.random() * 4.0)) {
            case 1:
                //Generate Circle
                twoD = new Circle(getColor(), getInt());
                break;
            case 2:
                //Generate Rectangle
                twoD = new Rectangle(getColor(), getInt(), getInt());
                break;
            case 3:
                //Declare variables
                int a;
                int b;
                int c;
                boolean bool;
                //Check the random side generated values is true for isTriangle() before generating a triangle
                do {
                    a = getInt();
                    b = getInt();
                    c = getInt();
                    bool = isTriangle(a, b, c);
                } while (!bool);
                //Generate Triangle
                twoD = new Triangle(getColor(), a, b, c);
                break;
            default:
                //Generate Trapezoid
                twoD = new Trapezoid(getColor(), getInt(), getInt(), getInt(), getInt(), getInt());
                break;
        }
        return twoD;
    }

    private static ThreeD getThreeD() {
        ThreeD threeD;
        switch ((int) (Math.random() * 3.0)) {
            case 1:
                //Generate Cube
                threeD = new Cube(getColor(), getDouble());
                break;
            case 2:
                //Generate Tetrahedron
                threeD = new Tetrahedron(getColor(), getDouble());
                break;
            default:
                //Generate Sphere
                threeD = new Sphere(getColor(), getDouble());
                break;
        }
        return threeD;
    }

    //Display 2D Shape output
    private static void process2DShape(Shape ss) {
        TwoD twod = (TwoD) ss;
        ShapeColor newShapeColor;
        
        //To guarantee a different color is generated
        do {
            newShapeColor = getColor();
        } while (newShapeColor == twod.getShapeColor());// As long as the newShapeColor generated is the same as the shape original color the do while loop will continue
        twod.recolor(newShapeColor);

        System.out.printf("Updated color: %s%n", newShapeColor);
        System.out.printf("Area = %.3f%n", twod.area());
        System.out.printf("I am a %s shape with color changed to %s%n", twod.getClass().getSimpleName(), newShapeColor);

    }

    //Display 3D Shape output
    private static void process3DShape(Shape ss) {
        ThreeD threeD = (ThreeD) ss;
        double random = Math.random();

        System.out.printf("Surface area = %.3f%n", threeD.area());
        System.out.printf("Volume = %.3f%n", threeD.volume());

        threeD.resize(random);
        System.out.printf("Size reduced by %.1f%%: %s%n", (random * 100), threeD);
        System.out.printf("Updated surface area = %.3f%n", threeD.area());
        System.out.printf("Updated volume = %.3f%n", threeD.volume());
        System.out.printf("I am a %s shape%n", threeD.getClass().getSimpleName());
    }

    private static void displayList(ArrayList<Shape> shapeArrayList) {
        //Declare counter variable
        int counter = 1;
        for (Shape s : shapeArrayList) {
            System.out.printf("Shape %d: %s%n", counter,s);

            //The of display the generated 2D or 3D shape is done by calling the subclass name as a string using the swtich case function to differentitate its shape 2D or 3D before processing/displaying the shape
            switch (s.getClass().getSimpleName()) {
                case "Circle":

                case "Rectangle":

                case "Triangle":

                case "Trapezoid":
                    process2DShape(s);
                    break;
                case "Sphere":

                case "Cube":

                case "Tetrahedron":
                    process3DShape(s);
                    break;
            }
            System.out.printf("---------------------------------------------------%n");
            counter++;
        }
    }

}

class Tetrahedron extends ThreeD {
    //Default constructor
    public Tetrahedron() {
    }

    //Other Constructor
    public Tetrahedron(ShapeColor sc, double a) {
        super(sc, a);
    }


    //Copy constructor
    public Tetrahedron(Tetrahedron t) {
        super(t.sc, t.a);
    }

    //
    @Override
    public double area() {
        return Math.sqrt(3) * Math.pow(a, 2);
    }

    @Override
    public double volume() {
        return Math.pow(a, 3) / (6 * Math.sqrt(2));
    }

    //Getter
    @Override
    public double getA() {
        return super.getA();
    }

    //Setter
    @Override
    public void set(ShapeColor sc, double a) {
        super.set(sc, a);
    }

    //ToString
    @Override
    public String toString() {
        return String.format("Tetrahedron %s", super.toString());
    }
}

class Cube extends ThreeD {
    //Default Constructor
    public Cube() {
    }

    //Other Constructor
    public Cube(ShapeColor sc, double a) {
        super(sc, a);
    }

    //Copy Constructor
    public Cube(Cube c) {
        super(c.sc, c.a);
    }

    @Override
    public double volume() {
        return Math.pow(a, 3);
    }

    @Override
    public double area() {
        return 6 * Math.pow(a, 2);
    }

    //Getter
    @Override
    public double getA() {
        return super.getA();
    }

    //Setter
    @Override
    public void set(ShapeColor sc, double a) {
        super.set(sc, a);
    }

    @Override
    public String toString() {
        return String.format("Cube %s", super.toString());
    }
}

class Sphere extends ThreeD {
    //Default Constructor
    public Sphere() {
    }

    //Other constructor
    public Sphere(ShapeColor sc, double a) {
        super(sc, a);
    }

    //Copy Constructor
    public Sphere(Sphere s) {
        this(s.sc, s.a);
    }

    @Override
    public double area() {
        return 4 * MYPI * Math.pow(a, 2);
    }

    @Override
    public double volume() {
        return (4.0 / 3.0) * MYPI * Math.pow(a, 3);
    }

    //Getter
    @Override
    public double getA() {
        return super.getA();
    }

    //Setter
    @Override
    public void set(ShapeColor sc, double a) {
        super.set(sc, a);
    }

    @Override
    public String toString() {
        return String.format("Sphere %s", super.toString());
    }
}

class Trapezoid extends TwoD {
    //Declare Variables
    private int h;

    //Default constructor
    public Trapezoid() {

    }

    //Other constructor
    public Trapezoid(ShapeColor sc, int a, int b, int c, int d, int h) {
        super(sc, a, b, c, d);
        this.h = h;
    }

    //Copy Constructor
    public Trapezoid(Trapezoid t) {
        this(t.sc, t.a, t.b, t.c, t.d, t.h);
    }

    @Override
    public double area() {
        return ((a + b) / 2.0) * h;
    }

    @Override
    public double perimeter() {
        return a + b + c + d;
    }

    //Getter
    @Override
    public int getA() {
        return super.getA();
    }

    @Override
    public int getB() {
        return super.getB();
    }

    @Override
    public int getC() {
        return super.getC();
    }

    @Override
    public int getD() {
        return super.getD();
    }

    public int getHeight() {
        return h;
    }

    //Setter
    public void set(ShapeColor sc, int a, int b, int c, int d, int h) {
        super.set(sc, a, b, c, d);
        this.h = h;
    }

    @Override
    public String toString() {
        return String.format("%s, %d)", super.toString(), h);
    }
}

class Triangle extends TwoD {
    //Default Constructor
    public Triangle() {

    }

    //Other Constructor
    public Triangle(ShapeColor sc, int a, int b, int c) {
        super(sc, a, b, c);
    }

    //Copy Constructor
    public Triangle(Triangle t) {
        this(t.sc, t.a, t.b, t.c);
    }


    @Override
    public double area() {
        double s = (a + b + c) / 2.0;
        return Math.sqrt(s * (s - a) * (s - b) * (s - c));
    }

    @Override
    public double perimeter() {
        return a + b + c;
    }

    //Getter
    @Override
    public int getA() {
        return super.getA();
    }

    @Override
    public int getB() {
        return super.getB();
    }

    @Override
    public int getC() {
        return super.getC();
    }

    //Setter
    @Override
    public void set(ShapeColor sc, int a, int b, int c) {
        super.set(sc, a, b, c);
    }

    @Override
    public String toString() {
        return String.format("%s", super.toString());
    }
}

class Rectangle extends TwoD {
    //Default Constructor
    public Rectangle() {

    }

    //Other Constructor
    public Rectangle(ShapeColor sc, int length, int width) {
        super(sc, length, width);
    }

    //Copy Constructor
    public Rectangle(Rectangle r) {
        this(r.sc, r.a, r.b);
    }

    @Override
    public double area() {
        return a * b;
    }

    @Override
    public double perimeter() {
        return 2 * (a + b);
    }

    //Getter
    public int getLength() {
        return super.getA();
    }

    public int getWidth() {
        return super.getB();
    }

    //Setter
    @Override
    public void set(ShapeColor sc, int length, int width) {
        super.set(sc, length, width);
    }

    @Override
    public String toString() {
        return String.format("%s", super.toString());
    }
}

class Circle extends TwoD {
    //Default constructor
    public Circle() {
    }

    //Other Constructor
    public Circle(ShapeColor sc, int radius) {
        super(sc, radius);
    }

    //Copy Constructor
    public Circle(Circle c) {
        this(c.sc, c.a);
    }

    //Getter
    public int getRadius() {
        return getA();
    }

    @Override
    public double area() {
        return MYPI * Math.pow(a, 2);
    }

    @Override
    public double perimeter() {
        return 2 * MYPI * a;
    }

    //Setter
    @Override
    public void set(ShapeColor sc, int radius) {
        super.set(sc, radius);
    }

    @Override
    public String toString() {
        return String.format("%s", super.toString());
    }
}

abstract class ThreeD implements Shape, OnlyThreeD {
    protected ShapeColor sc;
    protected double a;

    //Default constructor
    public ThreeD() {
    }

    //Other constructor
    public ThreeD(ShapeColor sc, double a) {
        this.sc = sc;
        this.a = a;
    }

    //Copy constructor
    public ThreeD(ThreeD td) {
        this(td.sc, td.a);
    }

    //Getter
    public double getA() {
        return a;
    }

    //Setter
    public void set(ShapeColor sc, double a) {
        this.sc = sc;
        this.a = a;
    }

    //Resize method
    public void resize(double percentage) {
        this.a = a * (1 - percentage);
    }

    @Override
    public String toString() {
        return String.format("(3D (%s, %.3f))", sc, a);
        //all 3D subclass has only a color and a double variable
    }
}

abstract class TwoD implements OnlyTwoD, Shape {
    protected ShapeColor sc;
    protected int a;
    protected int b;
    protected int c;
    protected int d;

    //default constructor
    public TwoD() {
    }

    //Other Constructor
    public TwoD(ShapeColor sc, int a) {
        this.sc = sc;
        this.a = a;
    }

    public TwoD(ShapeColor sc, int a, int b) {
        this.sc = sc;
        this.a = a;
        this.b = b;
    }

    public TwoD(ShapeColor sc, int a, int b, int c) {
        this.sc = sc;
        this.a = a;
        this.b = b;
        this.c = c;
    }

    public TwoD(ShapeColor sc, int a, int b, int c, int d) {
        this.sc = sc;
        this.a = a;
        this.b = b;
        this.c = c;
        this.d = d;
    }

    //Copy Constructor
    public TwoD(TwoD td) {
        this(td.sc, td.a, td.b, td.c, td.d);
    }


    //Getter
    public ShapeColor getShapeColor() {
        return sc;
    }

    public int getA() {
        return a;
    }

    public int getB() {
        return b;
    }

    public int getC() {
        return c;
    }

    public int getD() {
        return d;
    }

    //Setter
    public void set(ShapeColor sc, int a) {
        this.sc = sc;
        this.a = a;
    }

    public void set(ShapeColor sc, int a, int b) {
        this.sc = sc;
        this.a = a;
        this.b = b;
    }

    public void set(ShapeColor sc, int a, int b, int c) {
        this.sc = sc;
        this.a = a;
        this.b = b;
        this.c = c;
    }

    public void set(ShapeColor sc, int a, int b, int c, int d) {
        this.sc = sc;
        this.a = a;
        this.b = b;
        this.c = c;
        this.d = d;
    }

    //Recolor method
    public void recolor(ShapeColor sc) {
        this.sc = sc;
    }

    @Override
    public String toString() {
        if ((b == 0) && (c == 0) && (d == 0)) {//Circle only has a radius
            return String.format("Circle (2D (%s, %d))", sc, a);
        } else if ((d == 0)) { //Triangle only have 3 sides
            return String.format("Triangle (2D (%s, %d, %d, %d))", sc, a, b, c);
        } else if ((c == 0) && (d == 0)) { //Rectangle have 4 sides, 2 sides are of different values, the side opposite each other are the same
            return String.format("Rectangle (2D (%s, %d, %d))", sc, a, b);
        } else //Trapezoid has all 4 sides
            return String.format("Trapezoid (2D (%s, %d, %d, %d, %d)", sc, a, b, c, d);
    }
}

interface OnlyTwoD {
    public double perimeter();

    public void recolor(ShapeColor sc);

}

interface Shape {
    public final double MYPI = Math.PI;

    public double area();
}

interface OnlyThreeD {
    public double volume();

    public void resize(double percentage);
}

enum ShapeColor {
    Blue, Yellow, Red, Green, White
}
