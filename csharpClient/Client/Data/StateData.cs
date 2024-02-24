using System.Text.Json;
using System.Text.Json.Serialization;

namespace CsClient.Client.Dto
{
    /// <summary>
    /// Antwortdata vom Server bzgl. Spielstatus
    /// </summary>
    public class StateData
    {
        [JsonPropertyName("id")]
        public int Id { get; set; }

        [JsonPropertyName("gameState")]
        public string? GameState { get; set; }

        [JsonPropertyName("field")]
        public double[][]? Field { get; set; }
    }
}
