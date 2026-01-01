# Placement Game & Algorithm X Solver

Dieses Projekt ist ein kommandozeilenbasiertes Puzzle-Spiel, bei dem rechteckige Teile auf einem Spielfeld platziert werden müssen. Es enthält zudem eine Implementierung des **Algorithm X** (Dancing Links), um Lösungen automatisch zu finden.

## Installation & Start

Stellen Sie sicher, dass Python installiert ist. Klonen Sie das Repository und führen Sie die Hauptdatei aus:

```python PlacementGameCLI.py```


Beim Start können Sie aus verschiedenen Schwierigkeitsgraden wählen (Small, Medium, Standard, Big, Insanity).

## Spielanleitung

Ziel des Spiels ist es, alle verfügbaren Teile ohne Überlappungen auf dem Spielfeld zu platzieren.

### Befehle in der CLI

Wenn ein Level geladen ist, können Sie folgende Befehle nutzen:

*   `place <id> <x> <y>`: Platziert das Teil mit der angegebenen ID an den Koordinaten (x, y).
*   `remove <id>`: Entfernt das Teil mit der ID wieder vom Spielfeld.
*   `rotate <id>`: Dreht ein Teil um 90 Grad (nur möglich, wenn es aktuell nicht platziert ist).
*   `list`: Zeigt eine detaillierte Liste aller Teile, deren Größe und Status an.
*   `show`: Zeigt das aktuelle Spielfeld erneut an.
*   `solve`: Startet den Algorithm X Solver, um Lösungen automatisch zu berechnen und zu visualisieren.
*   `delay <sekunden>`: Setzt eine Verzögerung für den Solver (z. B. `delay 0.1`), um die Schritte der Platzierung besser verfolgen zu können.
*   `shuffle`: Mischt die Reihenfolge der Teile in der internen Liste.
*   `print`: Schaltet die automatische Bildschirmausgabe nach jedem Befehl an oder aus.
*   `reset`: Setzt das Spielfeld und alle Teile in den Ausgangszustand zurück.
*   `help`: Zeigt eine Kurzübersicht der verfügbaren Befehle.
*   `quit` oder `exit`: Beendet das aktuelle Level oder das Programm.

## Testen des Solvers (Empfehlung: Medium Level)

Um den Lösungsalgorithmus zu testen, wird das **Medium Level** besonders empfohlen.

**Warum Medium?**
In diesem Level reicht die Gesamtfläche der Teile nicht aus, um das komplette Spielfeld zu füllen. Der Solver muss daher interne "Pseudo-Teile" (Platzhalter) verwenden, um die leeren Zellen mathematisch als "belegt" zu markieren (Exact Cover Problem).
Das Level ist zudem klein genug, sodass der Algorithmus in wenigen Sekunden alle Lösungen finden kann.
