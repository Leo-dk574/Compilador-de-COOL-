import Lexico

def mensagemErro(token, token_esperado):
    print(f"Esperado {token_esperado} mas recebeu um {token["valor"]} do tipo {token["tipo"]} na linha:{Lexico.num_linha}")

def sintaticoExpr():
    print("Entrou no Expr")
    erro, token = ExprAtribuicao()
    return erro, token


def ExprAtribuicao():
    erro, token = ExprNotLogical()
    if erro: return True, token

    proximo = Lexico.peek()

    if(proximo["valor"] == "<-"):
        
        if(token["tipo"] != "ID"):
            mensagemErro(token, "ID para atribuição")
            return True, token
    
        token = Lexico.lexico()
        erro, token = sintaticoExpr()
        return erro, token

    return False, token


def ExprNotLogical():
    proximo = Lexico.peek()

    if(proximo["valor"] == "not"):
        token = Lexico.lexico()
        return sintaticoExpr()
    
    return ExprComparacao()

def ExprComparacao():
    erro, token = ExprSomaSub()
    if erro: return True, token

    proximo = Lexico.peek()

    if(proximo["valor"] in ["<", "<=", "="]):
        token = Lexico.lexico()
        
        return ExprSomaSub()

    return False, token

def ExprSomaSub():
    erro, token = ExprMultDiv()
    if erro: return True, token

    proximo = Lexico.peek()

    while(proximo["valor"] in ["+", "-"]):
        token = Lexico.lexico()
        erro, token = ExprMultDiv()
        if erro: return True, token
        proximo = Lexico.peek()

    return False, token


def ExprMultDiv():
    erro, token = ExprIsvoidNeg()
    if erro: return True, token

    proximo = Lexico.peek()

    while(proximo["valor"] in ["/", "*"]):
        token = Lexico.lexico()
        
        erro, token = ExprIsvoidNeg()
        if erro: return True, token
        proximo = Lexico.peek()

    return False, token


def ExprIsvoidNeg():
    proximo = Lexico.peek()

    if(proximo["valor"] in ["isvoid", "~"]):
        token = Lexico.lexico()
        return ExprIsvoidNeg()

    return ExprDispatch()


def ExprDispatch():
    erro, token = ExprAtomo()
    if erro: return True, token

    proximo = Lexico.peek()

    while proximo["valor"] in [".", "@", "("]:

        if proximo["valor"] == "@":
            Lexico.lexico()
            token_type = Lexico.lexico()
            if token_type["tipo"] != "TYPE":
                mensagemErro(token_type, "TYPE")
                return True, token_type

            proximo = Lexico.peek()
            if proximo["valor"] != ".":
                mensagemErro(proximo, ".")
                return True, proximo

        if proximo["valor"] == ".":
            Lexico.lexico()
            token = Lexico.lexico()
            if token["tipo"] != "ID":
                mensagemErro(token, "ID do método")
                return True, token

            if Lexico.peek()["valor"] != "(":
                mensagemErro(Lexico.peek(), "(")
                return True, Lexico.peek()

            erro, token_erro = validarArgumentosChamada()
            if erro: return True, token_erro

        if proximo["valor"] == "(":
            erro, token_erro = validarArgumentosChamada()
            if erro: return True, token_erro

        proximo = Lexico.peek()
            
    return False, token
        

def validarArgumentosChamada():
    Lexico.lexico()
    
    if Lexico.peek()["valor"] != ")": 
        while True:
            erro, _ = ExprAtribuicao() 
            if erro: return True, _
            
            if Lexico.peek()["valor"] == ",":
                Lexico.lexico() 
            else:
                break 
                
    token = Lexico.lexico()
    if token["valor"] != ")":
        mensagemErro(token, ")")
        return True, token
        
    return False, token

def ExprAtomo():
    proximo = Lexico.peek()

    
    if proximo["tipo"] == "ID":
        return False, Lexico.lexico()

    
    if proximo["tipo"] in ["Numero", "String"] or proximo["valor"] in ["true", "false"]:
        return False, Lexico.lexico()

    
    if proximo["valor"] == "(":
        Lexico.lexico()  

        erro, token = sintaticoExpr()
        if erro:
            return True, token

        token_fecha = Lexico.lexico()
        if token_fecha["valor"] != ")":
            mensagemErro(token_fecha, ")")
            return True, token_fecha

        return False, token_fecha

   
    if proximo["valor"] == "if":
        Lexico.lexico() 

        erro, token = sintaticoExpr()
        if erro: return True, token

        token_then = Lexico.lexico()
        if token_then["valor"] != "then":
            mensagemErro(token_then, "then")
            return True, token_then

        erro, token = sintaticoExpr()
        if erro: return True, token

        token_else = Lexico.lexico()
        if token_else["valor"] != "else":
            mensagemErro(token_else, "else")
            return True, token_else

        erro, token = sintaticoExpr()
        if erro: return True, token

        token_fi = Lexico.lexico()
        if token_fi["valor"] != "fi":
            mensagemErro(token_fi, "fi")
            return True, token_fi

        return False, token_fi

    
    if proximo["valor"] == "while":
        Lexico.lexico()  

        erro, token = sintaticoExpr()
        if erro: return True, token

        token_loop = Lexico.lexico()
        if token_loop["valor"] != "loop":
            mensagemErro(token_loop, "loop")
            return True, token_loop

        erro, token = sintaticoExpr()
        if erro: return True, token

        token_pool = Lexico.lexico()
        if token_pool["valor"] != "pool":
            mensagemErro(token_pool, "pool")
            return True, token_pool

        return False, token_pool

  
    if proximo["valor"] == "{":
        Lexico.lexico()  

        while True:
            erro, token = sintaticoExpr()
            if erro: return True, token

            token_pv = Lexico.lexico()
            if token_pv["valor"] != ";":
                mensagemErro(token_pv, ";")
                return True, token_pv

            if Lexico.peek()["valor"] == "}":
                break

        token_fecha = Lexico.lexico()
        if token_fecha["valor"] != "}":
            mensagemErro(token_fecha, "}")
            return True, token_fecha

        return False, token_fecha

    
    if proximo["valor"] == "new":
        Lexico.lexico()  

        token_type = Lexico.lexico()
        if token_type["tipo"] != "TYPE":
            mensagemErro(token_type, "TYPE")
            return True, token_type

        return False, token_type

    
    if proximo["valor"] == "let":
        Lexico.lexico() 

        while True:
            token_id = Lexico.lexico()
            if token_id["tipo"] != "ID":
                mensagemErro(token_id, "ID")
                return True, token_id

            token_dp = Lexico.lexico()
            if token_dp["valor"] != ":":
                mensagemErro(token_dp, ":")
                return True, token_dp

            token_type = Lexico.lexico()
            if token_type["tipo"] != "TYPE":
                mensagemErro(token_type, "TYPE")
                return True, token_type

            if Lexico.peek()["valor"] == "<-":
                Lexico.lexico()
                erro, token = sintaticoExpr()
                if erro: return True, token

            if Lexico.peek()["valor"] == ",":
                Lexico.lexico()
                continue
            else:
                break

        token_in = Lexico.lexico()
        if token_in["valor"] != "in":
            mensagemErro(token_in, "in")
            return True, token_in

        erro, token = sintaticoExpr()
        if erro: return True, token

        return False, token

    if proximo["valor"] == "case":
        Lexico.lexico()  

        erro, token = sintaticoExpr()
        if erro: return True, token

        token_of = Lexico.lexico()
        if token_of["valor"] != "of":
            mensagemErro(token_of, "of")
            return True, token_of

        while True:
            token_id = Lexico.lexico()
            if token_id["tipo"] != "ID":
                mensagemErro(token_id, "ID")
                return True, token_id

            token_dp = Lexico.lexico()
            if token_dp["valor"] != ":":
                mensagemErro(token_dp, ":")
                return True, token_dp

            token_type = Lexico.lexico()
            if token_type["tipo"] != "TYPE":
                mensagemErro(token_type, "TYPE")
                return True, token_type

            token_seta = Lexico.lexico()
            if token_seta["valor"] != "=>":
                mensagemErro(token_seta, "=>")
                return True, token_seta

            erro, token = sintaticoExpr()
            if erro: return True, token

            token_pv = Lexico.lexico()
            if token_pv["valor"] != ";":
                mensagemErro(token_pv, ";")
                return True, token_pv

            if Lexico.peek()["valor"] == "esac":
                break

        token_esac = Lexico.lexico()
        if token_esac["valor"] != "esac":
            mensagemErro(token_esac, "esac")
            return True, token_esac

        return False, token_esac

    mensagemErro(proximo, "exprAtomo válido")
    return True, proximo