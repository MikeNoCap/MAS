from utils import isNum, isVar, VARIABLES, getSuperScriptString
from parantesParser import isolerParantesPotenser, isolerBareParantes
from typing import Union


AlleUtrykk = Union[
    "Utrykk",
    "Utrykk.Ledd",
    "Utrykk.Ledd.Faktor",
    "Utrykk.Ledd.Faktor.Potens"
]

class Utrykk:
    class Ledd:
        class Faktor:
            class Potens:
                def __init__(self: "Utrykk.Ledd.Faktor.Potens", string: str):
                    self.grunntall, self.eksponent = string.split("^")

                    
                    self.grunntall: AlleUtrykk = Utrykk(self.grunntall)
                    if (self.grunntall.isLedd): 
                        self.grunntall = self.grunntall.getLedd()[0]
                    if (self.grunntall.isFaktor):
                        self.grunntall = self.grunntall.getLedd()[0].getFaktorer()[0]
                    
                    self.eksponent: AlleUtrykk = Utrykk(self.eksponent)
                    if (self.eksponent.isLedd): 
                        self.eksponent = self.eksponent.getLedd()[0]
                    if (self.eksponent.isFaktor):
                        self.eksponent = self.eksponent.getLedd()[0].getFaktorer()[0]
                    
                def __eq__(self, other: AlleUtrykk):
                    if isinstance(other, Utrykk.Ledd.Faktor.Potens):
                        return self.grunntall==other.grunntall and self.eksponent == other.eksponent
                    # TODO: Reflektere om dette faktisk er mattematisk korrekt når hodet ikke er fritert
                    return self.grunntall == other.value and self.eksponent == 1
                def __hash__(self):
                    return hash((self.grunntall, self.eksponent))    
                    
                def __repr__(self: "Utrykk.Ledd.Faktor.Potens") -> str:
                    grunntallString = \
                        str(self.grunntall) if self.grunntall.isFaktor \
                        else f"({self.grunntall})"
                    eksponentString = \
                        str(self.eksponent) if self.eksponent.isFaktor \
                        else f"({self.eksponent})"
                    
                    return f"{grunntallString}^{eksponentString}"
                
                
                    
                def __add__(self, other):
                    if isinstance(self, Utrykk.Ledd.Faktor.Potens) and isinstance(other, Utrykk.Ledd.Faktor.Potens):
                        if self == other:
                            return 2*self
                        return Utrykk(f"{self.grunntall}^{self.eksponent}+{other.grunntall}^{other.eksponent}")
                    
                    selfPotens = isinstance(self, Utrykk.Ledd.Faktor.Potens)
                    potens = self if selfPotens else other
                    annen = other if selfPotens else self
                    
                    return Utrykk(f"{potens}+{annen.value}")
                        

                    return NotImplemented
                __radd__ = __add__
                
                def __mul__(self: "Utrykk.Ledd.Faktor.Potens", other: AlleUtrykk):
                    if isinstance(other, (int, float)):
                        return Utrykk.Ledd(f"{other}*({self})")
                    if isinstance(other, (Utrykk.Ledd.Faktor)):
                        if other.isNum:
                            return Utrykk.Ledd(f"{other.value}*({self})")
                        if other.isVariable:
                            if other == self.grunntall:
                                self.eksponent = self.eksponent + 1
                        # Potensregler
                        
                        
                        # 1 a^m*a^n = a^(m+n)
                        # TODO: Lag en sortert standardform for Utrykk slik at man kan validere om de er like
                    if isinstance(other, Utrykk.Ledd.Faktor.Potens):
                        if self.grunntall == other.grunntall:
                            return Utrykk.Ledd.Faktor.Potens(f"{self.grunntall}^{self.eksponent + other.eksponent}")
                        if self.eksponent == other.eksponent:
                            return Utrykk.Ledd.Faktor.Potens(f"{self.grunntall}*{other.grunntall}^{self.eksponent}")
                                                
                
                __rmul__ = __mul__
                
            def __init__(
                self, 
                value: str, 
                isVariable: bool = False, 
                isParantes: bool = False, 
                isPotens: bool = False
                ):
                self.isVariable = isVariable
                self.isParantes = isParantes
                self.isPotens = isPotens
                self.isNum: bool = not (isPotens or isVariable or isParantes)
                if (isinstance(value, (int, float))):
                    value = str(value)
                
                self.isLedd = False
                self.isFaktor = True
                
                self.value = value
                if not isVariable and not any([isParantes, isPotens]):
                    if "." in value:
                        self.value = float(value)
                    else:
                        self.value = int(value)
                if isParantes:
                    # Bruker rekursjon. Fjerner parantes for å unngå evig rekursjon
                    self.value = Utrykk(value[1:-1])
                    
                    # Bryter helt ned til Faktor nivå. Hvis Faktor er potens skal det håndteres i implementeringen
                    
                    if self.value.isLedd:
                        self.value = self.value.getLedd()[0]
                    if self.value.isFaktor:
                        self.value = self.value.getLedd()[0].getFaktorer()[0]
                    
                if isPotens:
                    self.value = Utrykk.Ledd.Faktor.Potens(value)
                    
                    
                self.string_representation = str(self.value)
            def __eq__(self, other: AlleUtrykk):
                return self.value == other.value
            def __hash__(self):
                return hash(self.value)
    
                
            def __add__(self, other: AlleUtrykk):
                if isinstance(self, Utrykk) or isinstance(self, Utrykk.Ledd):
                    return NotImplemented
                if isinstance(other, Utrykk) or isinstance(other, Utrykk.Ledd):
                    return NotImplemented
                
                # Bare ta for seg faktor multiplikasjon på et faktor nivå
                if isinstance(other, (float, int)):
                    other = Utrykk.Ledd.Faktor(str(other),False, False, False)
                if isinstance(self, (float, int)):
                    self = Utrykk.Ledd.Faktor(str(self),False, False, False)
                    
                    
                if (isinstance(other, Utrykk.Ledd.Faktor) or isinstance(self, Utrykk.Ledd.Faktor)):
                    if self.isNum and other.isNum:
                        return self.value + other.value
                    if self.isNum and other.isVariable \
                        or self.isVariable and other.isNum:
                            faktorer = [self, other]
                            if faktorer[0].isNum:
                                faktorer.reverse()
                            return Utrykk(f"{faktorer[0]}+{faktorer[1]}")
                    if self.isVariable and other.isVariable:
                        if self == other:
                            return self*2
                        return Utrykk(f"{self.value}+{other.value}")
                    if self.isPotens or other.isPotens:
                        if self.isPotens and other.isPotens:
                            return self.value + other.value
                        selfPotens = isinstance(self.value, Utrykk.Ledd.Faktor.Potens)
                        potens = self if selfPotens else other
                        other = other if selfPotens else self
                        return potens.value+other
                    if self.isParantes or other.isParantes:
                        if self.isParantes:
                            return other+self.value
                        return self+other.value
                        
                return NotImplemented
            __radd__ = __add__
                        
                    
            def __mul__(self, other):
                
                # Bare ta for seg faktor multiplikasjon på et faktor nivå
                if isinstance(other, (float, int)):
                    other = Utrykk.Ledd.Faktor(str(other),False, False, False)
                if isinstance(self, (float, int)):
                    self = Utrykk.Ledd.Faktor(str(self),False, False, False)
                    
                if isinstance(other, Utrykk.Ledd.Faktor):
                    if other.isVariable and not self.isVariable \
                      or self.isVariable and not other.isVariable:
                        faktorer = [other, self]
                        
                        # Tall står først i feks 2x
                        if faktorer[1].isNum or (faktorer[1].isVariable and not faktorer[0].isNum):
                            faktorer.reverse()
                            
                        return Utrykk.Ledd(f"{faktorer[0].value}{faktorer[1].value}", False)

                    if other.isVariable and self.isVariable:
                        if other == self: 
                            return Utrykk.Ledd.Faktor(value=f"{self.value}^2", isPotens=True)
                        faktorer = [self, other]
                        def get_key(n: Utrykk.Ledd.Faktor):
                            return n.value
                        faktorer = sorted(faktorer, key=get_key)
                        return Utrykk.Ledd(f"{faktorer[0].value}{faktorer[1].value}")
                    
                    if other.isNum:
                        if self.isNum:
                            return Utrykk.Ledd.Faktor(str(self.value*other.value))
                        return Utrykk.Ledd(f"{other.value}{self.value}")
                    if self.isNum:
                        if other.isNum:
                            return Utrykk.Ledd.Faktor(str(self.value*other.value))
                        return Utrykk.Ledd(f"{self.value}{other.value}")
                        
                    

                return NotImplemented
            
            __rmul__ = __mul__

            
            def __repr__(self) -> str:
                return self.string_representation
                
            
        def lagFaktorer(self, string) -> list[Faktor]:
            # Isoler paranteser som egene faktorer
           
            parantesFaktorer = []
            parantesPotensFaktorer = []
            while ("(" in string):
                start, slutt = isolerBareParantes(string)
                parantesDel = string[start:slutt+1]
                
                # Ikke let etter potenser hvis vi har nådd slutten
                if slutt+1 == len(string):
                    parantesFaktorer.append(self.Faktor(parantesDel, isParantes=True))
                    string = string[:start] + string[slutt+1:]
                    continue
                    

                if string[start-1] == "^":
                    start, slutt = isolerParantesPotenser(string, start, slutt, "grunntall")
                    potens = string[start:slutt]
                    parantesPotensFaktorer.append(self.Faktor(potens, isPotens=True, isParantes=True))
                    string = string[:start] + string[slutt+1:]
                    continue
                elif string[slutt+1] == "^":
                    start, slutt = isolerParantesPotenser(string, start, slutt, "eksponent")
                    potens = string[start:slutt]
                    parantesPotensFaktorer.append(self.Faktor(potens, isPotens=True, isParantes=True))
                    string = string[:start] + string[slutt:]
                    continue
           
                parantesFaktorer.append(self.Faktor(parantesDel, isParantes=True))
                string = string[:start] + string[slutt+1:]
            
            charType = "number"
            newString = ""
            previousChar = ""
            inExponent = False
            for char in string:
                if len(string) == 1:
                    newString = string
                    break
                if previousChar == "^":
                    inExponent = True
                if inExponent:
                    newString += char
                    if char == "*":
                        inExponent = False
                        continue
                    continue
                if (charType == "variable" and isNum(char)):
                    newString += "*"
                    charType = "number"
                elif (charType == "number" and isVar(char)):
                    newString += "*"
                    charType = "variable"
                elif (charType == "variable" and isVar(char)):
                    newString += "*"
                newString += char
                previousChar = char
                
            andreFaktorer = []
            if newString[-1] == "*":
                newString = newString[:-1]
            if newString[0] == "*":
                newString = newString[1:]
                
            for faktor in newString.split("*"):
                andreFaktorer.append(self.Faktor(faktor, isVariable=isVar(faktor), isPotens=("^" in faktor)))
            
            return andreFaktorer + parantesFaktorer + parantesPotensFaktorer
                    
                    
            

            
            # while len(string) != stringIndex+1:
            #     stringIndex += 1
                
        def getFaktorer(self) -> list[Faktor]:
            return self.faktorer
        
        def __init__(self, string, negative=False):
            self.faktorer = self.lagFaktorer(string)
            self.negative = negative
            self.string = string
            
            self.isLedd = True
            self.isFaktor = len(self.faktorer) == 1

        def __repr__(self) -> str:
            if (self.negative):
                return f"-({self.string})"
            return self.string
        
    
    def lagLedd(self: "Utrykk", string: str) -> list["Utrykk.Ledd"]: # type: ignore
        # Lar utrykk bli parset som string. Feks Utrykk
        string = str(string)
        string = string.replace(' ', '')

        # Legg til + hvis første leddet er positivt
        if string[0] not in '+-':
            string = '+' + string

        ledd = []
        i = 0
        start = 0
        depth = 0

        while i < len(string):
            char = string[i]
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
            # Hvis vi når + eller - markerer det et nytt ledd. Hvis depth ikke er null er vi inne i en parantes og må fortsette.
            elif char in '+-' and i != start and depth == 0:
                # Hvis forrige karakter var ^ er det del av potens
                # og ikke et nytt ledd
                if i > 0 and string[i-1] == "^":
                    i += 1
                    continue
                ledd.append(string[start:i])
                start = i
            i += 1

        ledd.append(string[start:i])  # Legg til det siste leddet
        
        objektLedd = []
        
        for etLedd in ledd:
            erNegativ = etLedd[0] == "-"
            objektLedd.append(self.Ledd(etLedd[1:], erNegativ))
        
        return objektLedd  
    def getLedd(self: "Utrykk") -> list[Ledd]:
        return self.ledd
            

        
    def __init__(self, string):
        self.string: str = string
        self.ledd: list[Utrykk.Ledd] = self.lagLedd(self.string)
        self.isLedd = (len(self.ledd) == 1)
        self.isFaktor = (self.isLedd and len(self.ledd[0].getFaktorer()) == 1)
        
        
        if self.isFaktor:
            self.isLedd = False
        
    def __repr__(self) -> str:
        return self.string


if __name__ == "__main__":
    faktor1 = Utrykk.Ledd.Faktor(4)
    faktor2 = Utrykk.Ledd.Faktor("x^2", isPotens=True)
    print(getSuperScriptString(str(faktor1*faktor2)))

    
