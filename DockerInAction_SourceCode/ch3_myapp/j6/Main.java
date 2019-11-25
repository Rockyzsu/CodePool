public class Main {
    public static void main(String[] args) {
        SomeResource res = new SomeResource();
        try {
            System.out.println("This is my app!");
        } finally {
            res.close();
        }
    }
}

class SomeResource {
    public void close() {
        System.out.println("Hello from Java 6!");
    }
}
