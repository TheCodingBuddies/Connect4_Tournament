package cb.bots;

public class AiFactory {
     public static BotAi create(String type) {
         switch (type) {
             case "fill":
                 return new FillBot();
             default:
                 return new RandomBot();
         }
     }
}
