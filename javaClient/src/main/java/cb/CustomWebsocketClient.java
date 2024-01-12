package cb;

import cb.bots.BotAi;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.java_websocket.client.WebSocketClient;
import org.java_websocket.handshake.ServerHandshake;

import java.net.URI;

public class CustomWebsocketClient extends WebSocketClient {
    private boolean connected = false;
    private final ObjectMapper mapper = new ObjectMapper();
    private final BotAi bot;

    public CustomWebsocketClient(URI serverUri, BotAi ai) {
        super(serverUri);
        bot = ai;
    }

    @Override
    public void onOpen(ServerHandshake handshakedata) {
        System.out.println("Verbindung zu connect4 geöffnet");
        send("{\"type\": \"connect\", \"name\": \""+ bot.getName()+ "\"}");
    }

    @Override
    public void onMessage(String message) {
//        System.out.println("on message " + message);
        if (!connected) {
            try {
                ConnectionData data = mapper.readValue(message, ConnectionData.class);
                connected = data.getConnected();
                bot.setPlayerId(data.getId());
                send("{\"id\":" + bot.getPlayerId() + ", \"type\": \"getState\"}");
            } catch (JsonProcessingException e) {
                System.out.println("wrong message");
            }
        } else {
            StateData stateData;
            try {
                stateData = mapper.readValue(message, StateData.class);
            } catch (JsonProcessingException e) {
                throw new RuntimeException(e);
            }
            if (stateData.getId() == bot.getPlayerId()) {
                switch (stateData.getGameState()) {
                    case "pending" -> {
                        sleep(100);
                        send("{\"id\":" + bot.getPlayerId() + ", \"type\": \"getState\"}");
                    }
                    case "finished" -> {
                        System.out.println("Spiel vorbei. Client wird beendet");
                    }
                    case "playing" -> {
                        int column = bot.play(stateData.getField());
                        send("{\"id\":" + bot.getPlayerId() + ", \"type\": \"play\", \"column\":" + column + "}");
                    }
                    default -> {
                        System.out.println("Not your turn");
                        sleep(50);
                        send("{\"id\":" + bot.getPlayerId() + ", \"type\": \"getState\"}");
                    }
                }
            }
        }
    }

    private static void sleep(int ms) {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public void onClose(int code, String reason, boolean remote) {
        System.out.println("Verbindung zum Server geschlossen: " + reason);
    }

    @Override
    public void onError(Exception ex) {
        System.err.println("Fehler: " + ex.getMessage());

    }
}