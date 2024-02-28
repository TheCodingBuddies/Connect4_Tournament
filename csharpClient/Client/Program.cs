﻿using CommandLine;
using CsClient.Bots;
using CsClient.Bots.Internal;
using CsClient.Client;

Parser.Default.ParseArguments<Options>(args)
    .WithParsed(Run)
    .WithNotParsed(OnError);

static async void Run(Options o)
{
#if DEBUG
    Console.WriteLine("Debug Mode");
#endif

    string serverUrl = $"ws://{o.Server}:{o.Port}";
    Console.WriteLine($"Run Bot {o.Name} with Serveraddress: {serverUrl}");

    FourConnectWebsocketClient myClient = new FourConnectWebsocketClient(
        BotFactory.GetBotByName(o.Name!));

    myClient.OnOpen += (s,e) => { Console.WriteLine("Connected!"); };
    myClient.OnClose += (s, e) =>
    {
        myClient.Disconnect().Wait();
        Console.WriteLine("Closed");
    };

    await myClient.Connect(serverUrl);
}

static void OnError(IEnumerable<Error> errors)
{
    Console.WriteLine(string.Join(Environment.NewLine, errors));
}

public class Options
{
    [Option('n', "name", Default = "UserBot", HelpText = "Name for your bot")]
    public string? Name { get; set; }

    [Option('s', "server", Default = "localhost", HelpText = "Server with running 4Connect Service")]
    public string? Server { get; set; }

    [Option('p', "port", Default = 8765, HelpText = "Used Port for server connection")]
    public int Port { get; set; }
}