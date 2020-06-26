import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class Main {

    public static void main(String[] args)
    {
        LinkedStrings followers = readFollowers();
        LinkedStrings followings = readFollowings();

        LinkedStrings iDontFollow = new LinkedStrings();
        LinkedStrings dontFollowMe = new LinkedStrings();

        iDontFollow = followers.searchDiff(followings);
        dontFollowMe = followings.searchDiff(followers);

        System.out.println("*******I don't follow*************");
        iDontFollow.displayList();

        System.out.println("*******They don't follow me*************");
        dontFollowMe.displayList();

        return;
    }

    private static LinkedStrings readFollowers()
    {
        File file = new File("C:\\Users\\alfre\\OneDrive\\Documents\\InstaProject[Java]\\src\\Followers.txt");
        Scanner sc = null;
        try {
            sc = new Scanner(file);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
            System.out.println("File name not valid");
            return null;
        }

        LinkedStrings followers = new LinkedStrings();
        while(sc.hasNextLine())
            followers.insert(sc.nextLine());

        return followers;
    }

    private static LinkedStrings readFollowings()
    {
        File file = new File("C:\\Users\\alfre\\OneDrive\\Documents\\InstaProject[Java]\\src\\Following.txt");
        Scanner sc = null;
        try {
            sc = new Scanner(file);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
            System.out.println("File name not valid");
            return null;
        }

        LinkedStrings followings = new LinkedStrings();
        while(sc.hasNextLine())
            followings.insert(sc.nextLine());

        return followings;
    }

}
