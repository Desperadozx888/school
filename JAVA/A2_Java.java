import java.util.HashMap;
import java.util.Random;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        // write your code here
        QueueSimulator Qs = new QueueSimulator();
        Scanner scanner = new Scanner(System.in);
        //Input runtime in minutes
        System.out.printf("Please enter the total minutes to run: ");
        int runtime = scanner.nextInt();
        //Execute the simulator
        Qs.emailProcess(runtime);
    }
}

class Email {
    //declare the count variable for queue
    //to push the message
    private int queueCounter;

    public Email() {
        //set queue count to 1
        queueCounter = 1;
    }

    //increments the queue counter
    public void IncCount() {
        queueCounter++;
    }

    //returns the queue counter
    public int getQCount() {
        return queueCounter;
    }
}

//Declare class called QueueSimulator
class QueueSimulator {
    //Create a queue for email messages
    private Queue<Email> messagesInQueue;
    //declare variable to count send messages
    private HashMap<Integer, Integer> messageCount;

    //declare variables for number of
    //messages sent and received
    int message_received = 0;
    int message_dequeued = 0;
    int enqueue = 0;
    int received_total = 0;
    int dequeued_total = 0;
    //Used to calculate the average number of request
    int total_time = 0;
    int total_value = 0;

    //create constructor to initialize
    //the queue and HashMap
    public QueueSimulator() {
        messagesInQueue = new Queue<Email>(1000);
        messageCount = new HashMap<Integer, Integer>();
    }

    //This method processes the email: Receives the email and tries to Send it
    public void emailProcess(int run_time) {
        //Process the email per second
        //Run time is in minutes, so multiply by 60 to get the seconds
        int run_time_seconds = run_time * 60;
        int counter = 0;

        //create a Random object for random number generation
        Random rand = new Random();
        //While counter is less than run time
        while (counter < run_time_seconds) {
            //receive a message
            receiveEmail(rand);
            //delivery attempt
            dequeMessage(rand);

            //If a minute has elapsed, increment the overall counts,
            //and reset the minute-wise counters
            if (counter % 60 == 0) {
                received_total += message_received;
                dequeued_total += message_dequeued;
                //enqueue is the number of emails that are
                //left in the queue after processing (receive and send)
                enqueue += messagesInQueue.size();
                message_dequeued = 0;
                message_received = 0;
            }
            //decrement time
            counter++;
        }

        //print the statistics
        System.out.printf("\nThe total messages processed: %d", dequeued_total);
        System.out.printf("\nThe average arrival time: %.2f", ((float) received_total / run_time));
        System.out.printf("\nThe average number of messages sent per minute: %.2f", ((float) dequeued_total / run_time));
        System.out.printf("\nThe number of messages in the queue in a minute: %.2f", ((float) enqueue / run_time));
        //show the number of requests
        messageCount.forEach((key, val) -> {
            System.out.printf("\nNumber of messages sent in %d attempt : %d", key, val);
            if (key > 1) {
                total_value += (key - 1) * val;
                total_time += key;
            }
        });
        //show the average number of request
        System.out.printf("\nAverage Number of times messages had to be requeued: %.2f", ((float) total_value / total_time));
    }

    public void receiveEmail(Random rand) {
        //generate a random number in range [0,1] and receive a message
        //if we get one 50% chance of receiving a message each second
        boolean rec_email = rand.nextInt(2) == 1 ? true : false;
        if (rec_email) {
            messagesInQueue.add(new Email());
            message_received++;
            enqueue++;
        }
    }

    public void dequeMessage(Random rand) {
        //generate a random number in range 0, 1, 2, 3. Since 25% cannot be sent is 1/4
        int prob_dq = rand.nextInt(4);
        if (!messagesInQueue.isEmpty()) {
            //if we get 1, 2, 3 successfully dequeue
            if (prob_dq != 0 && message_dequeued < 30) {
                int queueCount = messagesInQueue.peek().getQCount();
                if (messageCount.containsKey(queueCount)) {
                    int current_val = messageCount.get(queueCount);
                    messageCount.put(queueCount, current_val + 1);
                    enqueue--;
                } else {
                    messageCount.put(queueCount, 1);
                }
                messagesInQueue.remove();
                message_dequeued++;
            }
            //If we get 0, we count it as cannot dequeue (25% chance) in that case
            // we remove from the head and then enqueue it on the queue
            else {
                Email temp = messagesInQueue.peek();
                temp.IncCount();
                messagesInQueue.remove();
                messagesInQueue.add(temp);
            }
        }
    }
}

//Queue Class
class Queue<T> {
    private int maxSize;

    private Object[] queArray;

    private int front;

    private int rear;

    private int nItems;

    public Queue(int s) {
        maxSize = s;
        queArray = new Object[maxSize];
        front = 0;
        rear = -1;
        nItems = 0;
    }

    public void add(T j) {
        if (rear == maxSize - 1)
            rear = -1;
        queArray[++rear] = j;
        nItems++;
    }


    public T remove() {
        T temp = (T) queArray[front++];
        if (front == maxSize)
            front = 0;
        nItems--;
        return temp;
    }

    public T peek() {
        return (T) queArray[front];
    }

    public boolean isEmpty() {
        return (nItems == 0);
    }

    public boolean isFull() {
        return (nItems == maxSize);
    }

    public int size() {
        return nItems;
    }
}