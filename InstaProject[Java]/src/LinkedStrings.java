public class LinkedStrings {
    Node head;

    private class Node
    {
        String value;
        Node next;

        Node(String x)
        {
            value = x;
            next = null;
        }
    }

    public LinkedStrings()
    {
        head = null;
    }


    public void insert(String x)
    {
        Node newNode = new Node(x);

        if(head == null)
            head = newNode;

        else
        {
            Node temp = head;
            while(temp.next != null)
                temp = temp.next;
            temp.next = newNode;
        }
    }

    public void displayList()
    {
        Node temp = head;

        while(temp != null)
        {
            System.out.println(temp.value);
            temp = temp.next;
        }
    }

    public void deleteLast()
    {
        Node temp = head;

        while(temp.next != null)
            temp = temp.next;
        temp = null;
    }

    public boolean deleteThis(String x)
    {
        Node temp = head;
        Node previous = temp;

        while(temp != null && (temp.value.compareTo(x) != 0))
        {
            previous = temp;
            temp = temp.next;
        }

        if(temp == null)
            return false;

        else
        {
            previous.next = temp.next;
            return true;
        }
    }

    public LinkedStrings searchDiff (LinkedStrings x)
    {
        Node temp = head;
        LinkedStrings diff = new LinkedStrings();

        while(temp != null)
        {
           boolean found = x.searchThis(temp.value);

           if(!found)
               diff.insert(temp.value);

           temp = temp.next;
        }

        return diff;
    }

    private boolean searchThis(String x)
    {
        Node temp = head;

        while(temp != null && (temp.value.compareTo(x) != 0))
            temp = temp.next;

        if(temp == null)
            return false;

        else
            return true;
    }
}
