import py4j.GatewayServer;

public class Pyva {
  private PlayerMove pyva;
  public Pyva() {
         pyva = new PlayerMove();
       }
  public PlayerMove getMove() {
         return pyva;
       }
       
  public static void main(String[] args) {
         Pyva pyvaPlayer = new Pyva();
         GatewayServer gatewayServer = new GatewayServer(pyvaPlayer); 
         gatewayServer.start();
         System.out.println("Pyva pipe started");        
      }
}