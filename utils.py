VARIABLES = "abcdefghijklmnopqrstuvwxyz"

def isNum(char):
    return char in [str(i) for i in range(0, 10)] or char in ["+", "-"]
def isVar(char):
    return char in VARIABLES

def getSuperScriptString(string: str) -> str:
    return string.replace("^2", "²").replace("^3", "³").replace("^4", "⁴").replace("^x", "ˣ")