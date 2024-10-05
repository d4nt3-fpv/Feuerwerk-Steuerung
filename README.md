# Feuerwerk-Steuerung
In diesem Projekt habe ich eine Software entwickt, die Videosynchrones Feuerwerk ermöglicht.

## Funktionsweise
Die Software stellt eine serielle Verbindung mit einem Arduino Mikrocontroller, welcher über USB an den Computer angeschlossen wird, her.
Anschließend liest die Software eine Video und eine Timecode (csv) Datei ein.
Wenn die Show gestartet wird spielt das Programm das Video ab und sendet an den entsprechendne Positionen die im Timecode hinterlegten Befehle an den Arduino, der dann das entsprechende Feuerwerk zündet

## Benötigte Programme

VLC Media Player muss installiert sein.

## Wie ist die Timecode Datei aufgebaut?

Die Timecode Datei setzt sich zusammen aus einer Zeit und einem Befehl getrennt von einem symmikolon in jeder Zeile:

Zeit[in sekunden];Befehl

Beispiel:

3;Raketen      (nach sekunde 3 wird der Befehl "Raketen" an den Arduino gesendet)

## Credits

Vielen Dank an Johannes, der mich auf die Idee gebracht hat, das ganze zu Programmieren!
