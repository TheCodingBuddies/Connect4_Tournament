package cb.bots;

public class AiFactory {
     public static BotAi create(String type) {
         switch (type) {
             case "fill":
                 return new FillBot();
             case "user":
                 return new UserBot();
             default:
                 return new RandomBot();
         }
     }
}
