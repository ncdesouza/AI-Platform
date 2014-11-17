import py4j.GatewayServer;

public class CramClientEntryPoint {
  private PlayerMove entrypt;
  public CramClientEntryPoint() {
         entrypt = new PlayerMove();
       }
  public PlayerMove getMove() {
         return entrypt;
       }
       
  public static void main(String[] args) {
         CramClientEntryPoint cramEntryPoint = new CramClientEntryPoint();
         GatewayServer gatewayServer = new GatewayServer(cramEntryPoint); 
         gatewayServer.start();
         System.out.println("Pyva Gateway Started");        
      }
}