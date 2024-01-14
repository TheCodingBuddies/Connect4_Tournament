package cb.bots;

public class UserBot implements BotAi {
    private String name;
    private int id;

    public UserBot() {
        // Wähle hier deinen Nickname aus (ändere "UserAI")
        name = "UserAI";
        // Die Token ID wird vom Server vergeben.. nicht editieren!
        id = -1;
    }

    @Override
    public int play(int[][] field) {
        /*
        Implementiere hier deine Logik, damit die KI spielen kann
         */
        return 0; // aktuell wird immer die erste Spalte ausgewählt als nächsten Zug
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
