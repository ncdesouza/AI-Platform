import py4j.GatewayServer;

public class Py1va {
  private PlayerMove pyva0;
  private Player1Move pyva1;
  private Player2Move pyva2;
  private Player3Move pyva3;
  public Py1va() {
         pyva0 = new PlayerMove();
         pyva1 = new Player1Move();
         pyva2 = new Player2Move();
         pyva3 = new Player3Move();
       }
  public PlayerMove player0() {
         return pyva0;
  }

  public Player1Move player1() {
         return pyva1;
  }

  public Player2Move player2() {
         return pyva2;
  }

  public Player3Move player3() {
         return pyva3;
  }
       
  public static void main(String[] args) {
         Py1va pyva1Player = new Py1va();
         GatewayServer gatewayServer = new GatewayServer(pyva1Player);
         gatewayServer.start();
         System.out.println("Py1va pipe started");
  }
}