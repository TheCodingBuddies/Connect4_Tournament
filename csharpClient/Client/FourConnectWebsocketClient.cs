using System.Net.WebSockets;
using System.Text;
using System.Text.Json;
using CsClient.Bots;
using CsClient.Client.Data;
using CsClient.Client.Dto;

namespace CsClient.Client
{
    public class FourConnectWebsocketClient : IDisposable
    {
        public delegate void MyMessageReceivedEventHandler(object sender, string message);

        public event EventHandler OnOpen;
        public event EventHandler OnClose;
        public event MyMessageReceivedEventHandler OnMessage;

        private readonly UTF8Encoding _encoding = new();
        private readonly IBot _bot;
        private ClientWebSocket? _webSocket;
        private bool _isConnected;

        /// <summary>
        /// Verbindet mit Zielurl
        /// </summary>
        /// <param name="uri"></param>
        /// <returns>Das Taskobjekt welches die asynchrone ausfuehrung repraesentiert</returns>
        public async Task Connect(string uri)
        {
            await Connect(new Uri(uri));
        }

        /// <summary>
        /// Verbindet mit Zielurl
        /// </summary>
        /// <param name="uri"></param>
        /// <returns>Das Taskobjekt welches die asynchrone ausfuehrung repraesentiert</returns>
        public async Task Connect(Uri uri) 
        {

            _webSocket?.Dispose();
            _webSocket = new();
            _webSocket.ConnectAsync(uri, CancellationToken.None).Wait();

            await SendHandshake();
            Task.Run(Listen);
            OnOpen?.Invoke(this, EventArgs.Empty);
        }

        /// <summary>
        /// Trennt die Verbindung zum 4 Connect Server.
        /// </summary>
        /// <returns>Das Taskobjekt welches die asynchrone ausfuehrung repraesentiert</returns>
        public async Task Disconnect()
        {
            await _webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Normal Closure", CancellationToken.None);
            _webSocket.Dispose();
            OnClose?.Invoke(this, EventArgs.Empty);
        }

        /// <summary>
        /// Sendet Nachricht an den 4 Connect Server.
        /// </summary>
        /// <param name="message"></param>
        /// <returns>Das Taskobjekt welches die asynchrone ausfuehrung repraesentiert</returns>
        public async Task Send(string message)
        {
#if DEBUG
            Console.WriteLine("Send: " + message);
#endif
            await _webSocket!.SendAsync(
                new ArraySegment<byte>(_encoding.GetBytes(message)),
                messageType: WebSocketMessageType.Text,
                endOfMessage: true,
                cancellationToken: CancellationToken.None);
        } 

        public async Task Sleep(int ms)
        {
            await Task.Delay(TimeSpan.FromMilliseconds(ms));
        }

        public FourConnectWebsocketClient(IBot bot)
        {
            _bot = bot;
        }

        private async Task SendHandshake()
        {
            await Send("{\"type\": \"connect\", \"name\": \"" + _bot.Name + "\"}");
        }

        private async Task Listen()
        {
            ArraySegment<byte> buffer = new ArraySegment<byte>(new byte[1024]);
            WebSocketReceiveResult result = null;
            while (_webSocket.State == WebSocketState.Open)
            {
                using (var ms = new MemoryStream())
                {
                    do
                    {
                        result = _webSocket.ReceiveAsync(buffer, CancellationToken.None).Result;
                        if (result.MessageType == WebSocketMessageType.Close)
                        {
                            _webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, string.Empty, CancellationToken.None).Wait();
                            break;
                        }
                        else
                        {
                            ms.Write(buffer.Array, buffer.Offset, result.Count);
                        }
                    }
                    while (!result.EndOfMessage);

                    ms.Seek(0, SeekOrigin.Begin);
                    if (result.MessageType == WebSocketMessageType.Text)
                    {
                        using (var reader = new StreamReader(ms, Encoding.UTF8))
                        {
                            var stringData = await reader.ReadToEndAsync();
#if DEBUG
                            Console.WriteLine($"Receive: {stringData}");
#endif
                            OnMessage?.Invoke(this, stringData);
                            HandleMessage(stringData);
                        }
                    }
                }
            }

        }

        private void HandleMessage(string stringData)
        {
            if (!_isConnected)
            {
                ConnectionData connectionData = JsonSerializer.Deserialize<ConnectionData>(stringData);
                _isConnected = connectionData.Connected;
                _bot.PlayerId = connectionData.Id;

                var connectRequest = Request.GetStateFor(_bot.PlayerId);
                Send("{\"id\":" + _bot.PlayerId + ", \"type\": \"getState\"}").Wait();
            }
            else
            {
                StateData stateData = JsonSerializer.Deserialize<StateData>(stringData);
                switch (stateData.GameState.ToLower())
                {
                    case "pending":
                        Sleep(100).Wait();
                        Send(Request.GetStateFor(_bot.PlayerId)).Wait();
                        break;
                    case "finished":
                    // exit
                        break;
                    case "playing":
                        var column = _bot.Play(stateData.Field.Select(row => row.Select(cell => (int)cell).ToArray()).ToArray());
                        Send(Request.PlayColumn(_bot.PlayerId, column)).Wait();
                        break;
                    default:
                        // not your turn
                        Sleep(50).Wait();
                        Send(Request.GetStateFor(_bot.PlayerId)).Wait();
                        break;
                }
            }
        }

        public void Dispose()
        {
            _webSocket.Dispose();
        }
    }
}
