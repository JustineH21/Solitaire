class Pile():
    def __init__(self) -> None:
        self.p = self.creer_pile_vide()
        
    def creer_pile_vide(self) -> list:
        return []
    
    def est_vide(self) -> bool:
        if self.p == []:
            return True
        else:
            return False
        
    def empiler(self, elem) -> None:
        self.p.append(elem)
        
    def depiler(self) -> any:
        return self.p.pop()
    
    def sommet(self) -> any:
        return self.p[-1]
    
    def taille(self) -> int:
        return len(self.p)
    
class File:

    def __init__(self, file: list = None) -> None:
        if file != None:
            self.f = file
        else:
            self.f = self.creer_file_vide()
    
    def creer_file_vide(self) -> list:
        return []
    
    def est_vide(self) -> bool:
        if len(self.f) == 0:
            return True
        else:
            return False
        
    def enfiler(self, elem) -> None:
        self.f.append(elem)
    
    def defiler(self) -> any:
        return self.f.pop(0)
        
    def tete(self) -> any:
        return self.f[0]
        
    def taille(self) -> int:
        return len(self.f)