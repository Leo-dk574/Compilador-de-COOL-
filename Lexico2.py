def tipador(palavra):
    token = {
        "tipo": "Tipo",
        "valor": palavra
    }
    if(palavra == "Fim do Arquivo"):
        token["tipo"] = "EOF"
        return token
    if(palavra[0]=='\"'):
        token["tipo"] = "String"
    if(palavra.isdecimal()):
        token["tipo"] = "Numero"
    if(palavra in ["+","-","<","<=","=>","<-","*","/","~","="]):
        token["tipo"] = "Operador"
    if(palavra in "{}();:~+-*/=.,@"):
        token["tipo"] = "Delimitador"
    if(palavra.lower() in ["class","inherits","if","then","fi","while","loop","pool","let","in","case","of","esac","new","isvoid","not","true","false"]):
        token["tipo"] = "PR"
    if(palavra[0].isupper()):
        token["tipo"] = "Class"
    if(token["tipo"] == "Tipo"):
        token["tipo"] = "Variavel"
    return token

# PR, Class, String, Numero, Operador, Variavel, Delimitator