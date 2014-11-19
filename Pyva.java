import py4j.GatewayServer;

public class Pyva {
  private PlayerMove pyva0;
  private PlayerMove1 pyva1;
  private PlayerMove2 pyva2;
  private PlayerMove3 pyva3;
  public Pyva() {
         pyva0 = new PlayerMove();
         pyva1 = new PlayerMove1();
         pyva2 = new PlayerMove2();
         pyva3 = new PlayerMove3();
       }
  public PlayerMove player0() {
         return pyva0;
  }

  public PlayerMove1 player1() {
         return pyva1;
  }

  public PlayerMove2 player2() {
         return pyva2;
  }

  public PlayerMove3 player3() {
         return pyva3;
  }
       
  public static void main(String[] args) {
         Pyva pyvaPlayer = new Pyva();
         GatewayServer gatewayServer = new GatewayServer(pyvaPlayer); 
         gatewayServer.start();
         System.out.println("Pyva pipe started");        
  }
}