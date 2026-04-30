import Lexico
from SintaticoExpr import mensagemErro
import SintaticoExpr

def sintaticoExprPrototipo(tipo=0):
    print("Entrou no Expr")
    chaves = 1
    token = {
        "tipo": "",
        "valor": ""
    }
    if(tipo == 0):
        while(token["tipo"] != "EOF"):
            token = Lexico.lexico()
            if(token["valor"] == '{'):
                chaves = chaves + 1
            if(token["valor"] == '}'):
                chaves = chaves - 1
            if(chaves == 0):
                return False, token
    else:
        while(token["valor"] != ";"):
            token = Lexico.lexico()
        return False, token


def sintaticoFormal():
    print("Entrou no Formal")
    token = Lexico.lexico()

    if(token["valor"] == ")"):
        return False, token
    
    while True:
        if(token["tipo"] != "ID"):
            mensagemErro(token, "ID")
            return True, token
        
        token = Lexico.lexico()
        if(token["valor"] != ":"):
            mensagemErro(token, ":")
            return True, token

        token = Lexico.lexico()
        if(token["tipo"] != "TYPE"):
            mensagemErro(token, "TYPE")
            return True, token
        
        token = Lexico.lexico()
        if(token["valor"] == ")"):
            return False, token
        
        if(token["valor"] == ","):
            token = Lexico.lexico()
        else:
            mensagemErro(token, ", ou )")
            return True, token


def sintaticoFeature(token):
    print("Entrou no Feature")
    
    if token["tipo"] != "ID":
        mensagemErro(token, "ID")
        return True, token
    
    token = Lexico.lexico()
    
    
    if token["valor"] == "(":
        erro, token = sintaticoFormal()
        if erro: return True, token
        
        token = Lexico.lexico()
        if token["valor"] != ":":
            mensagemErro(token, ":")
            return True, token
            
        token = Lexico.lexico()
        if token["tipo"] != "TYPE":
            mensagemErro(token, "TYPE")
            return True, token
            
        token = Lexico.lexico()
        if token["valor"] != "{":
            mensagemErro(token, "{")
            return True, token
            
        erro, token = SintaticoExpr.sintaticoExpr()
        if erro: return True, token

        token = Lexico.lexico()
        if token["valor"] != "}":
            mensagemErro(token, "}")
            return True, token
        
        
        token = Lexico.lexico()
        if token["valor"] != ";":
            mensagemErro(token, ";")
            return True, token

        return False, token

    
    elif token["valor"] == ":":
        token = Lexico.lexico()
        if token["tipo"] != "TYPE":
            mensagemErro(token, "TYPE")
            return True, token
        
        if Lexico.peek()["valor"] == "<-":
            Lexico.lexico() 
            erro, token = SintaticoExpr.sintaticoExpr()
            if erro: return True, token
        
        
        token = Lexico.lexico()
        if token["valor"] != ";":
            mensagemErro(token, ";")
            return True, token

        return False, token

    else:
        mensagemErro(token, "( ou :")
        return True, token

def sintaticoClass(token):
    print("Entrou na Class")
    
    if token["valor"] != "class":
        mensagemErro(token, "class")
        return True
    
    token = Lexico.lexico()
    if token["tipo"] != "TYPE":
        mensagemErro(token, "TYPE")
        return True
    
    token = Lexico.lexico()
    if token["valor"] == "inherits":
        
        token = Lexico.lexico()
        if token["tipo"] != "TYPE":
            mensagemErro(token, "TYPE")
            return True
        token = Lexico.lexico()
    
    if token["valor"] != "{":
        mensagemErro(token, "{")
        return True
    
    token = Lexico.lexico()
    while(token["valor"] != "}"):
        erro, token = sintaticoFeature(token)
        
        if(erro):
            return True
        
        if token["valor"] != ";":
            mensagemErro(token, ";")
            return True
        token = Lexico.lexico()
    return False



def sintaticoProgram():
    print("Entrou no Program")
    token = Lexico.lexico()
    while(token["tipo"] != "EOF"):
        erro = sintaticoClass(token)

        if(erro):
            break

        token = Lexico.lexico()
        if token["valor"] != ";":
            mensagemErro(token, ";")
            break
        token = Lexico.lexico()