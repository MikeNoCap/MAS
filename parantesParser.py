from utils import isNum, isVar

def isolerBareParantes(string):
    # Finner start og slutt index til første parantes funnet i utrykket
    parantesIndex = string.find("(")
    if parantesIndex == -1:
        return None
    leddStart = parantesIndex

    leddSlutt = leddStart
    openParantesCount = 1
    closedParantesCount = 0
    
    # Sørg for at index er utenfor parantesen
    while openParantesCount != closedParantesCount:
        leddSlutt += 1

        if string[leddSlutt] == "(":
            openParantesCount += 1
        if string[leddSlutt] == ")":
            closedParantesCount += 1
    return (leddStart, leddSlutt)
def isolerParantesPotenser(string, start, slutt, potensDel):
    if potensDel == "grunntall":
        indexAdd = -1
    else:
        indexAdd = 1
    grunntallStart = start+indexAdd
    if potensDel != "grunntall":
        grunntallStart = slutt+indexAdd
    

    if isVar(string[grunntallStart+indexAdd]):
        grunntallStart += indexAdd
        if potensDel != "grunntall":
            return start, grunntallStart
        return grunntallStart, slutt
    if isNum(string[grunntallStart+indexAdd]):
        if potensDel != "grunntall" and grunntallStart+indexAdd == len(string)-1:
            return start, grunntallStart+2
        while isNum(string[grunntallStart+indexAdd]):
            grunntallStart += indexAdd
        if potensDel != "grunntall":
            return start, grunntallStart
        return grunntallStart, slutt
    if string[grunntallStart+indexAdd] == ")":
        depth = 0
        while True:
            grunntallStart += indexAdd
            if string[grunntallStart] == ")":
                depth += 1
            if string[grunntallStart] == "(":
                depth -= 1
                if depth == 0:
                    return grunntallStart, slutt
    if string[grunntallStart+indexAdd] == "(":
        depth = 0
        while True:
            grunntallStart += indexAdd
            if string[grunntallStart] == "(":
                depth += 1
            if string[grunntallStart] == ")":
                depth -= 1
                if depth == 0:
                    return start, grunntallStart
            
            

            
            
        
            
            

if __name__ == "__main__":
    string = "(4-(x-x))^3"
    start, slutt = isolerParantesPotenser(string, 0, 8, "eksponent")
    print(string[start:slutt])