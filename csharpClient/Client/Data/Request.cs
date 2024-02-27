using System.Text.Json;
using System.Text.Json.Serialization;

namespace CsClient.Client.Data
{
    public static class Request
    {
        public static string GetStateFor(int botId)
        {
            return JsonSerializer.Serialize(new StateRequest { Id = botId });
        }

        public static string PlayColumn(int botId, int column)
        {
            return JsonSerializer.Serialize(new PlayRequest { Id = botId, Column = column });
        }
        
        public class StateRequest
        {
            [JsonPropertyName("id")] public int Id { get; set; }
            [JsonPropertyName("type")] public string Type { get; set; } = "getState";
        }

        public class PlayRequest
        {
            [JsonPropertyName("id")] public int Id { get; set; }
            [JsonPropertyName("type")] public string Type { get; set; } = "play";
            [JsonPropertyName("column")] public int Column { get; set; }
        }
    }
}
