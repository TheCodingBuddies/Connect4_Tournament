package cb;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonInclude(JsonInclude.Include.NON_NULL)
public class ConnectionData {
    @JsonProperty("id")
    private int id;
    @JsonProperty("connected")
    private boolean connected;

    public ConnectionData() {
    }

    public boolean getConnected() {
        return connected;
    }

    public void setConnected(boolean value) {
        connected = value;
    }

    public int getId() {
        return id;
    }

    public void setId(int value) {
        id = value;
    }
}
