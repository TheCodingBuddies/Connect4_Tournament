package cb.bots;

import java.util.Random;

public class RandomBot implements BotAi {
    private String name;
    private int id;

    public RandomBot() {
        name = "JavaRandom";
        id = -1;
    }
    @Override
    public int play(int[][] field) {
        Random rand = new Random();
        return rand.nextInt(7);
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public void setPlayerId(int playerId) {
        id = playerId;
    }

    @Override
    public int getPlayerId() {
        return id;
    }
}
