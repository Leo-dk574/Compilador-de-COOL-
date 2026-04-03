import Lexico

def sintatico():
    token = {
        "tipo": "",
        "valor": ""
    }
    while(token["tipo"] != "EOF"):
        token = Lexico.lexico()
        print(f"{token["valor"]}   {token["tipo"]}   n:{Lexico.num_linha}")