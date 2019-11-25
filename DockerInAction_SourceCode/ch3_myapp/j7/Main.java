public class Main {
    public static void main(String[] args) {
        try (SomeResource res = new SomeResource();) {
            System.out.println("This is my app!");
        }
    }
}

class SomeResource implements AutoCloseable {
    public void close() {
        System.out.println("Hello from Java 7!");
    }
}
