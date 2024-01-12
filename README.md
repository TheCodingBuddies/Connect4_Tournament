# Willkommen zum KI Wettbewerb "4 Gewinnt" von den Coding Buddies!

Zum krönenden Abschluss unseres Grundlagenkurses veranstalten wir einen KI Wettbewerb zu dem Klassiker "4 Gewinnt".
Nutzt euer erlangtes Wissen aus dem Kurs und tretet gegen andere Entwickler in einem spaßigen Turnier im KO Modus an!

**Grundsätzlich gilt:**

Solltet ihr Fragen haben oder Hilfe benötigen. Scheut euch nicht uns auf unseren Plattformen zu kontaktieren! Wir werden
auch verschiedene Starthilfen zur Verfügung stellen.

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

## Den Spieleserver starten

Den Spieleserver startest du wie folgt:

```  
cd gameServer
py main.py
``` 

Hierfür wird default der Port 8765 verwendet. Falls du beispielsweise den Port 5555 
verwenden möchtest, ändere den Aufruf zu:

```  
py main.py 5555
```

Es sollte als letzte Nachricht zu sehen sein:

```  
start game server..
```

Der Server ist erfolgreich gestartet und die Clients können sich verbinden.
Sobald sich zwei Clients verbunden haben, beginnt das Spiel.

## Einen Client mit dem Server verbinden

Den Python client startest du wie folgt:

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

## Die Botklasse

Die Botklasse kann wahlweise in Java oder Python implementiert werden:

### Python

TBD

### Java

TBD

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
