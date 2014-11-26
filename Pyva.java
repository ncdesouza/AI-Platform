import py4j.GatewayServer;

public class Pyva {
  private Player1 pyva1;
  private Player2 pyva2;
  private Player3 pyva3;
  private Player4 pyva4;

  public Pyva() {
         pyva1 = new Player1();
         pyva2 = new Player2();
         pyva3 = new Player3();
         pyva4 = new Player4();
       }
  public Player1 player1() {
         return pyva1;
  }

  public Player2 player2() {
         return pyva2;
  }

  public Player3 player3() {
         return pyva3;
  }

  public Player4 player4() {
         return pyva4;
  }
       
  public static void main(String[] args) {
         Pyva pyvaPlayer = new Pyva();
         GatewayServer gatewayServer = new GatewayServer(pyvaPlayer);
         gatewayServer.start();
         System.out.println("Pyva pipe started");
  }
}