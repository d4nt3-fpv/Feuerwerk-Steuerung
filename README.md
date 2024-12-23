# Feuerwerk-Steuerung
In diesem Projekt habe ich eine Software entwickt, die Videosynchrones Feuerwerk ermöglicht.

## Funktionsweise
Die Software stellt eine serielle Verbindung mit einem Arduino Mikrocontroller, welcher über USB an den Computer angeschlossen wird, her.
Anschließend liest die Software eine Video und eine Timecode (csv) Datei ein.
Wenn die Show gestartet wird spielt das Programm das Video ab und sendet an den entsprechendne Positionen die im Timecode hinterlegten Befehle an den Arduino, der dann das entsprechende Feuerwerk zündet

## Benötigte Programme

VLC Media Player in der 64-Bit Version muss installiert sein.

## Wie ist die Timecode Datei aufgebaut?

Die Timecode Datei setzt sich zusammen aus einer Zeit und einem Befehl getrennt von einem symmikolon in jeder Zeile:

Zeit[in sekunden];Befehl

Beispiel:
```
3;Raketen      (nach sekunde 3 wird der Befehl "Raketen" an den Arduino gesendet)
```

Seit Version 4.0 werden auch float werte für die Zeit unterstützt. Diese werden vom Programm mit einer Gemauigkeit von 0,2s verarbeitet. Wichtig hierbei ist die verwendung des Punktes als Dezimaltrennzeichen.

Beispiel:
```
3.4;Raketen      (nach sekunde 3,4 wird der Befehl "Raketen" an den Arduino gesendet)
```
