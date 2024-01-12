package cb.bots;

public class FillBot implements BotAi {
    private String name;
    private int id;

    public FillBot() {
        name = "JavaFill";
        id = -1;
    }
    @Override
    public int play(int[][] field) {
        return 0;
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
