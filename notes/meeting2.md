* status update: github ogarnięty
* struktura projektu
    * Oleg - klasy DiscreteSpace, Element
* drive - dorzucanie cząstki
* toppling - rozpadanie na boki
* avalanche - iterowanie 

proponowany układ w pseudokodzie:
```python
class Simulation:
    a = NotImplemented
    def Initialization(self):
        raise NotImplementedError
    def Driving(self):
        raise NotImplementedError   # definiowane w subklasach 
    def Toppling(self):
        raise NotImplementedError
    def Dissipation(self):     # można zrobić po prostu pierścionek wokół tablicy (L+2, L+2) i wszystkie sumy robić po wewnętrznej 
        raise NotImplementedError
    
    def AvalancheLoop(self):
        while !układ_w_równowadze:
            self.Toppling()
            self.Dissipation()
        
        AvalancheSize = self.visited.sum() # dla Manna
        return AvalancheSize, len(while)  # nasze obserwable
    def Dissipation(self):
        ...

class Manna(Simulation):
    def __init__(self, L):
        self.a = zeros((L, L))
    def Toppling(self):   # u Olga "Rule"
        # jak są dwie to rozrzucamy losowo
```

