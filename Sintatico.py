import Lexico

def mensagemErro(token, token_esperado):
    print(f"Esperado {token_esperado} mas recebeu um {token["valor"]} do tipo {token["tipo"]} na linha:{Lexico.num_linha}")

def sintaticoFeature(token):
    chaves = 1
    token = {
        "tipo": "",
        "valor": ""
    }
    while(token["tipo"] != "EOF"):
        token = Lexico.lexico()
        if(token["valor"] == '{'):
            chaves = chaves + 1
        if(token["valor"] == '}'):
            chaves = chaves - 1
        if(token["valor"] == ';' and chaves<1):
            return False, token
    mensagemErro(token, ';')
    return True, token
    

def sintaticoClass():
    token = {
        "tipo":"",
        "valor":""
    }
    token = Lexico.lexico()
    if(token["valor"] == "class"):
        token = Lexico.lexico()
        if(token["tipo"] == "TYPE"):
            token = Lexico.lexico()
            if(token["valor"] == "inherits"):
                token = Lexico.lexico()
                if(token["tipo"] == "TYPE"):
                    token = Lexico.lexico()
                else:
                    mensagemErro(token, "TYPE")
                    return False
            if(token["valor"] == '{'):
                token = Lexico.lexico()
                if(token["valor"] == '}'):
                    return True
                erro, token = sintaticoFeature(token);
                if(not erro):
                    if(token["valor"] == ';'): #mudar para }
                        return True
                mensagemErro(token, '}')
                return False
            mensagemErro(token, "{")
            return False
        else:
            mensagemErro(token, "TYPE")
            return False
    else:
        mensagemErro(token, "class")
        return False

def sintaticoProgram():
    token = {
        "tipo":"",
        "valor":""
    }
    while(token["tipo"] != "EOF"):
        if(not sintaticoClass()):
            print(f"Erro na Class")
            break
        token = Lexico.lexico()
        if(token["valor"] != ';' and token["tipo"] != "EOF"):
            print(f"Esperado ; mas encontrou {token["valor"]} na linha:{Lexico.num_linha}")
            break
        

def sintatico():
    token = {
        "tipo": "",
        "valor": ""
    }
    while(token["tipo"] != "EOF"):
        token = Lexico.lexico()
        print(f"{token["valor"]}   {token["tipo"]}   n:{Lexico.num_linha}")