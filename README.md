# pFlow-EdgeDetector

```python
    pFlow-EdgeDetector                    
    +---doc                        # Dokumentationen
    +---experiments                # Durchgeführte Experimente
    +---pFlowGRID                  # Bachelorarbeit von Nik Steinbrügge
    +---training_images            # Test-Bilder
    +---imageClearner.py           # Methoden für Bildverarbeitung
    +---main.py                    # Ergebnis dieser Bachelorarbeit
    \---polygon.py                 # Klasse für Polygone

```

Das Ziel dieses Projektes ist es, Polygonzüge aus klaren und simplen Grundrissbilder automatisiert zu erstellen. 
Um sich in die Bildverarbeitung einzuarbeiten, wurden diverse Experimente (siehe Ordner <a href="">experiments</a>) durchgeführt.

Damit das Ziel schlussendlich erreicht wurde, ist wie folgt vorgegangen worden:
1. Vorverarbeitung erfolgt mit Closing und einem Gaußfilter.
2. Kanten werden mittels Canny-Kantendetektor lokalisiert.
3. Für die Nachverarbeitung wird ein Closing eingesetzt.
4. Ecken werden mittels Harris-Eckendetektor detektiert.
5. Ecken werden bereinigt.
6. Mithilfe des Dijkstra Algorithmus werden die Ecken sinnvoll miteinander verbunden. Die Polygone werden erzeugt und abschließend gespeichert


Die Implementierung hierzu findet man in <a href="https://github.com/ju851han/pFlow-EdgeDetector/tree/main/experiments">main.py</a>.
Ausführliche Dokumentation für diese Bachelorarbeit kann entweder im Ordner <a href="https://github.com/ju851han/pFlow-EdgeDetector/blob/main/main.py">doc</a> oder in den Python-Scripten selbst gefunden werden.
