using System.Text.Json;
using System.Text.Json.Serialization;

namespace CsClient.Client.Dto
{
    /// <summary>
    /// Antwortdata vom Server bzgl. Connection
    /// </summary>
    public class ConnectionData
    {
        [JsonPropertyName("id")]
        public int Id { get; set; }
        [JsonPropertyName("connected")]
        public bool Connected { get; set; }
    }
}
