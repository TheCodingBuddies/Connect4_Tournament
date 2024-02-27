# Willkommen zum KI Wettbewerb "4 Gewinnt" von den Coding Buddies!

Zum krönenden Abschluss unseres Grundlagenkurses veranstalten wir einen KI Wettbewerb zu dem Klassiker "4 Gewinnt".
Nutzt euer erlangtes Wissen aus dem Kurs und tretet gegen andere Entwickler in einem spaßigen Turnier im KO Modus an!

**Grundsätzlich gilt:**

Solltet ihr Fragen haben oder Hilfe benötigen. Scheut euch nicht uns auf unseren Plattformen zu kontaktieren! Wir werden
auch verschiedene Starthilfen zur Verfügung stellen.

**UND ACHTUNG! Der Spaß und das Lernen steht im Vordergrund also macht mit :)**

<br>

![Beispielpartie](example.jpg)

## Aufgabe

Es ist ein **Bot** zu entwickeln, der nach den **Standardregeln** das Spiel "4 Gewinnt" spielt. Hierfür haben wir eine
Schnittstelle in den jeweiligen Clients (Java oder Python) bereit gestellt, welche implementiert werden muss. Das Ziel
ist es eine gewisse Anzahl an Spiele gegen eine Gegner KI zu gewinnen und als Turniersieger hervorzugehen! :)

## Teilnahmebedingungen

- Implementierung der vorgegebenen Bot Schnittstelle (Java oder Python)
- Der Bot sendet dem Spiel vor dem Timeout (ca 2 Sekunden), was der nächste Zug ist
- Die KI ist selbst geschrieben

## Anforderungen

- Python 3.10.4+ (für den Spieleserver und gegebenfalls für den Bot)
- Java SDK 17+  (falls der Bot in Java geschrieben wird)
- dotnet 8.0 (falls der Bot in csharp geschrieben wird)

## Den Spieleserver starten

Den Spieleserver findest du im Ordner "gameserver", welcher als Python projekt geöffnet werden kann.
Um die notwendigen Packages für den Server zu installieren:

```
py -m pip install -r requirements.txt
```

Danach kannst du den Spieleserver wie folgt starten (im gameserver ordner):

```  
py __main__.py
``` 

Hierfür wird default der Port 8765 verwendet. Falls du beispielsweise den Port 5555 
verwenden möchtest, ändere den Aufruf zu:

```  
py __main__.py 5555
```

Es sollte als letzte Nachricht zu sehen sein:

```  
start game server..
```

Der Server ist erfolgreich gestartet und die Clients können sich verbinden.
Sobald sich zwei Clients verbunden haben, beginnt das Spiel.

Den Server im "Manuellen Modus" starten auf dem standard Port:
```
py __main__.py --manual-mode
```
Den Server im "Manuellen Modus" starten mit selbst definiertem Port (z.B. port=7878):
```
py __main__.py 7878 --manual-mode
```
Das ist wichtig um den Server ohne Timeout laufen zu lassen. 
Das ist notwendig wenn man den manuellen Client zum spielen nutzen möchte.


## Einen Client mit dem Server verbinden (Python)

Den Python Client starten:

```  
cd pythonClient
py clientMain.py <BotName> <Port>
``` 

| Parameter | Beschreibung                                             |
|-----------|----------------------------------------------------------|
| BotName   | Name der KI, die gestartet werden soll (default: random) |
| Port      | Port des Servers (default: 8765)                         |

Möchtest du beispielsweise die Fill KI starten und der Server läuft auf 5555:

```  
py clientMain.py fill 5555
```

## Einen Client mit dem Server verbinden (Java)

Den Java Client starten:

```  
cd javaClient   # in den javaClient Ordner wechseln
.\gradlew run
```

Um einen anderen Port oder eine andere KI zu verwenden:

```  
.\gradlew run --args="<BotName <Port>"
``` 

| Parameter | Beschreibung                                             |
|-----------|----------------------------------------------------------|
| BotName   | Name der KI, die gestartet werden soll (default: random) |
| Port      | Port des Servers (default: 8765)                         |

Möchtest du beispielsweise deine eigene KI starten und der Server läuft auf 5555:

```  
.\gradlew run --args="user 5555"
``` 

## Einen Client mit dem Server verbinden (C#)

Den C# Client starten
```ps
cd csharpClient\Client
dotnet run -- -n OtherUserBot   #startet den Client und vergibt den Klassennamen "OtherUserBot"
```
| Parmeter | Switch         | Beschreibung                                  | Default     |
| -------- | -------------- | --------------------------------------------- | ----------- |
BotName    | -n or --name   | Name der KI, die gestartet werden soll        | UserBot     |
Server     | -s or --server | Serveradresse (ip oder dns)                   | localhost   |
Port       | -p or --port   | Port des 4 Connect Servers auf dem Zielserver | 8765        |

Wenn ihr also mehrere Bots geschrieben habt, könnt ihr mit dem Namen das ganze umschalten. 
Es ist aber natürlich auch ausreichend den Default zu belassen und alles im "UserBot" zu machen.

## Einen Client mit dem Server verbinden (Manueller Client)

Um gegen deine eigene KI spielen zu können, kannst du einen manuellen Client starten.
Anschließend kannst du mit der Eingabe von 1-7 in der Konsole deinen nächsten Zug auswählen.

Den Manual Client starten:

```  
cd manualClient   # in den ManuelClient Ordner wechseln
py manualClient.py <DeinName> <Port>
```

Möchtest du beispielsweise mit dem Namen "Jarvis" spielen und der Server läuft auf Port 5555:

```  
py manualClient.py Jarvis 5555
```

## Die Botklasse

Um eine Eigene KI in das Spiel zu integrieren, muss eine vorgegebene BotKlasse implmenetiert werden.
Dafür muss die play() Methode/Funktion ergänzt werden.

Die Botklasse kann wahlweise in Java oder Python entwickelt werden:

### Python

Unter dem Pfad "Bots" findest du das user_ai.py file.
Diese Klasse beinhaltet die user KI und die folgende Funktion "play":

```
    def play(self, current_field):
        #
        # Implementiere hier deine Logik, damit die KI spielen kann
        #
        return 0  # aktuell wird immer die erste Spalte ausgewählt als nächsten Zug
```

Der Returnwert der play Funktion ist ein Integer innerhalb von 0-5 (mögliche Spalten im Spielfeld)

### Java

Unter dem Package "bots" findest du das UserBot.java file.
Diese Klasse beinhaltet die user KI und die folgende Funktion "play":

```
    public int play(int[][] current_field) {
        /*
        Implementiere hier deine Logik, damit die KI spielen kann
         */
        return 0; // aktuell wird immer die erste Spalte ausgewählt als nächsten Zug
    }
```

Der Returnwert der play Funktion ist ein Integer innerhalb von 0-5 (mögliche Spalten im Spielfeld)

### Übersicht der aktuellen Bots

| Bot    | Beschreibung                           |
|--------|----------------------------------------|
| random | wählt zufällig eine nächste Spalte aus |
| fill   | füllt eine konfigurierte Spalte auf    |
| user   | verwendet deine eigene KI              |

### C#

Im rootverzeichnes des "Bots" Projektes findet ihr schon zwei Klassen, einmal den Beispiel RandomBot, den ihr vlt aus dem Java Teil kennt und eine Art Vorlage der "UserBot". Letzere ist quasi das Template für euren Bot, fügt hier in die Play Methode einfach euren C# Quellcode ein der ausgeführt werden soll. 

```cs
public int Play(int[][] field)
{
    //
    // Deine Play Methode - hier kann deine Logik stehen :)
    // 

    return 0;
}
```

Der Returnwert der Play Methode ist ein Integer innerhalb von 0-5 (mögliche Spalten im Spielfeld)



## Spielfeld Daten

Die aktuellen Spielfelddaten werden deiner KI pro Spielzug zur Verfügung gestellt.
Damit hast du die alle notwendigen Informationen und entsprechend "den Blick" auf das Spielfeld.

Die Variable "current_field" ist ein zweidimensionales Array, welches das Spielfeld beschreibt.

**Beispiel aktuelles Spielbrett der Variable "current_field [i] [j]":**
```  
       j=0   j=1   j=2   j=3   j=4   j=5   j=6 
i=0: [  1  ,  2  ,  0  ,  2  ,  0  ,  0  ,  0  ]
i=1: [  1  ,  0  ,  0  ,  2  ,  0  ,  0  ,  0  ]
i=2: [  1  ,  0  ,  0  ,  0  ,  0  ,  0  ,  0  ]
i=3: [  0  ,  0  ,  0  ,  0  ,  0  ,  0  ,  0  ]
i=4: [  0  ,  0  ,  0  ,  0  ,  0  ,  0  ,  0  ]
i=5: [  0  ,  0  ,  0  ,  0  ,  0  ,  0  ,  0  ]
```  

**Spieler 1 (Blau) hat die ID=1**

**Spieler 2 (Grün) hat die ID=2**

Um das Spiel zu gewinnen, muss die KI von Spieler 1 als nächsten Zug 
die erste Spalte auswählen/zurückgeben

**Die oben gezeigten Daten passen zu dem folgenden Bild:**

<br>

![Spielfelddaten](board_example.png)
