package cb.bots;

public interface BotAi {

    int play(int[][] field);

    String getName();

    void setPlayerId(int id);

    int getPlayerId();
}
