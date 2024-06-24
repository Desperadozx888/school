//Name: Chow Keiren
//Student no: 10227382
//Tutorial Group: T09
//Declaration: This is my own code. Please do give feedback on code format if needed

//Filename: Chow_Keiren_A3.java
//Objective: Create a GUI of a Q&A Room with interactive TextArea and Buttons.

import javax.swing.*;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.util.Random;

public class Chow_Keiren_A3 {

    public static void main(String[] args) {
        // create GUI and set variables for aesthetics purpose
        Gui gui = new Gui();
        gui.setSize(620, 500);
        gui.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        gui.getContentPane().setBackground(Color.DARK_GRAY);
        gui.setVisible(true);
        gui.setResizable(false);

    }
}

//GUI class
class Gui extends JFrame implements ActionListener, MouseListener {
    //Declare Instances
    private Random random = new Random();
    private JTextArea questionTextField;
    private JTextArea hostTextField;
    private JLabel jLabel;
    private Icon iconArray;
    private JButton[] buttonArray;
    private JButton hostBtn;
    private JButton clearBtn;
    //Randomly generated participant from 4 - 10
    private Participant participant[] = new Participant[(random.nextInt(10 - 4) + 4)];
    private String[] nameArray = {"Pat tan", "Fat huat", "Bui Bui", "Ah tan", "Bui Fei", "Siao Fei", "Si fei", "Da Fei", "Ah kaow", "Ah heng"};
    //Height and width for buttons
    private final int height = 65;
    private final int width = 145;
    //Image string values for editing & Pic Size around 50 by 50
    private final Icon defaultIcon = new ImageIcon("out/production/121_A3/com/company/Red.png");
    private final Icon replacedIcon = new ImageIcon("out/production/121_A3/com/company/Pink.png");
    //Single string for image, Array, each image is by a number in increasing order in the for loop below in btn method, eg img1.jpg = "img" + i + "jpg"
    private String imageName = "out/production/121_A3/com/company/";
    private final Icon clearIcon = new ImageIcon("out/production/121_A3/com/company/clear.png");
    private final Icon hostIcon = new ImageIcon("out/production/121_A3/com/company/hostdefault.jpg");
    private final Icon replaceHostIcon = new ImageIcon("out/production/121_A3/com/company/hostreplaced.png");
    private final Icon onclickHostIcon = new ImageIcon("out/production/121_A3/com/company/doge.gif");
    //Fonts setting for better viewing of words
    private Font font = new Font("Sans", Font.PLAIN, 14);

    public Gui() {
        super("Q & A Room");
        setLayout(new FlowLayout());

        //Question Text Area method
        setQuestionTextField();

        //Jlabel Host
        jLabel = new JLabel("Host");
        jLabel.setForeground(Color.WHITE);
        jLabel.setFont(font);
        add(jLabel);

        //Host Text area method
        setHostTextField();

        //Buttons method
        setButtons();

    }

    //Question Text Field , set dimensions and BG color and FG color and Insertion point color and fonts slightly bigger so teacher can see
    public void setQuestionTextField() {
        questionTextField = new JTextArea("Sir, i have problem in theses two statements:\n\tSystem.out.printn(\"I am sick of covid19\");\n\tSystem.out.println(\"Kill kill virus\");\nCompiler made noise , whats wrong huh?");
        questionTextField.setFont(font);
        questionTextField.setBackground(Color.black);
        questionTextField.setColumns(55);
        questionTextField.setForeground(Color.white);
        questionTextField.setRows(5);
        questionTextField.setCaretColor(Color.white);
        add(questionTextField);
    }

    //Host Text Field , set dimensions and BG color and FG color and Insertion point color and fonts slightly bigger so teacher can see
    public void setHostTextField() {
        hostTextField = new JTextArea("You are very careless\n1. printn should be println\n2. Missing a semicolon");
        hostTextField.setFont(font);
        hostTextField.setBackground(Color.BLUE);
        hostTextField.setColumns(55);
        hostTextField.setForeground(Color.white);
        hostTextField.setRows(5);
        hostTextField.setCaretColor(Color.white);
        add(hostTextField);
    }

    //All the buttons together in 1 method
    public void setButtons() {
        //Button and Participant
        buttonArray = new JButton[participant.length];
        for (int i = 0; i < participant.length; i++) {
            participant[i] = new Participant("Student " + (i + 1), nameArray[i], "T0" + (i + 1), (imageName + (i + 1) + ".jpg")); //remove image name if theres no name infront of the number
            buttonArray[i] = new JButton(participant[i].getNameButton());
            buttonArray[i].setIcon(defaultIcon);
            buttonArray[i].setPreferredSize(new Dimension(width, height));
            add(buttonArray[i]);
            //Add Events
            buttonArray[i].addActionListener(e -> actionPerformed(e));
            buttonArray[i].addMouseListener(this);
        }


        //Host Btn
        hostBtn = new JButton("Host");
        hostBtn.setIcon(hostIcon);
        hostBtn.setPreferredSize(new Dimension(width, height));
        add(hostBtn);
        //Add Events
        hostBtn.addMouseListener(this);
        //Lambda Expression
        hostBtn.addActionListener((ActionEvent e) -> {
            JOptionPane.showMessageDialog(null, hostTextField.getText(), "I am the host", JOptionPane.WARNING_MESSAGE, onclickHostIcon);
        });


        //Clear TextArea
        clearBtn = new JButton("Clear");
        clearBtn.setIcon(clearIcon);
        clearBtn.setPreferredSize(new Dimension(width, height));
        add(clearBtn);

        //Lambda expression for clear btn
        clearBtn.addActionListener((ActionEvent e) -> {
            questionTextField.setText("");
            hostTextField.setText("");
        });
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        String s = "";
        for (int i = 0; i < participant.length; i++) {
            if (e.getSource() == buttonArray[i]) {
                iconArray = new ImageIcon(participant[i].getImageFile());

                s += String.format("%s", participant[i]);
                s += String.format("%s", questionTextField.getText());
                JOptionPane.showMessageDialog(null, s, "Welcome to the chatroom", JOptionPane.WARNING_MESSAGE, iconArray);

            }
        }
    }

    //On Mouse Entered, Icon and Color will change
    @Override
    public void mouseEntered(MouseEvent e) {
        if (e.getSource() == hostBtn) {
            hostBtn.setBackground(Color.CYAN);
            hostBtn.setIcon(replaceHostIcon);
        } else {
            for (int i = 0; i < buttonArray.length; i++) {
                if (e.getSource() == buttonArray[i]) {
                    buttonArray[i].setBackground(Color.CYAN);
                    buttonArray[i].setIcon(replacedIcon);
                }
            }
        }
    }

    //On Mouse Exit, Icon and Color will change
    @Override
    public void mouseExited(MouseEvent e) {
        if (e.getSource() == hostBtn) {
            hostBtn.setBackground(new JButton().getBackground());
            hostBtn.setIcon(hostIcon);
        } else {
            for (int i = 0; i < buttonArray.length; i++) {
                if (e.getSource() == buttonArray[i]) {
                    buttonArray[i].setBackground(new JButton().getBackground());
                    buttonArray[i].setIcon(defaultIcon);
                }

            }
        }
    }

    //Unused method as it came required with mouse listener interface
    @Override
    public void mouseClicked(MouseEvent e) {

    }

    @Override
    public void mousePressed(MouseEvent e) {
    }

    @Override
    public void mouseReleased(MouseEvent e) {

    }
}

//Class participant
class Participant {
    private String nameButton;
    private String fullName;
    private String tutorialGp;
    private String imageFile;

    //Constructor
    public Participant(String nameButton, String fullName, String tutorialGp, String imageFile) {
        this.nameButton = nameButton;
        this.fullName = fullName;
        this.tutorialGp = tutorialGp;
        this.imageFile = imageFile;
    }

    //Getter Setter
    public String getNameButton() {
        return nameButton;
    }

    public String getFullName() {
        return fullName;
    }

    public String getTutorialGp() {
        return tutorialGp;
    }

    public String getImageFile() {
        return imageFile;
    }

    //toString
    @Override
    public String toString() {
        return String.format("Hi! I am participant %s%nMy name is %s%nI am from tutorial group: %s%n", nameButton, fullName, tutorialGp);
    }
}
