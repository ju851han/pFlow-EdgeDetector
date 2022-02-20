# pFlow-EdgeDetector

```python
    pFlow_Edge                    
    +---doc                        # Dokumentationen
    +---experiments                # Durchgeführte Experimente
    +---pFlowGRID                  # Bachelorarbeit von Nik Steinbrügge
    +---training_images            # Test-Bilder
    \---main.py                    # Ergebnis dieser Bachelorarbeit
```

Das Ziel dieses Projektes ist es, Polygonzüge aus klaren und simplen Grundrissbilder automatisiert zu erstellen. 
Um sich in die Bildverarbeitung einzuarbeiten, wurden diverse Experimente (siehe Ordner <a href="">experiments</a>) durchgeführt.

Damit das Ziel schlussendlich erreicht wurde, ist wie folgt vorgegangen worden:
1. Grundrissbild wird bereinigt, d. h. unerwünschte Bildstrukturen werden verwaschen.
2. Mittels Canny-Detektor werden danach die Kanten detektiert.
3. Via Harris-Detektor werden die Ecken lokalisiert.
5. Um die Ecken sinnvoll miteinander zu verknüpfen, wird eine abgewandelte Form des Dijkstra-Algorithmus verwendet.

Die Implementierung hierzu findet man in <a href="https://github.com/ju851han/pFlow-EdgeDetector/tree/main/experiments">main.py</a>.
Ausführliche Dokumentation für diese Bachelorarbeit kann entweder im Ordner <a href="https://github.com/ju851han/pFlow-EdgeDetector/blob/main/main.py">doc</a> oder in den Python-Scripten selbst gefunden werden.
