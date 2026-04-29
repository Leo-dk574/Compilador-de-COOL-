global num_linha
num_linha = 1

global f

global c
c = ' '

global prox_token
prox_token = None

def arquivoOpen(nome):
    global f
    f = open(nome)


def tipador(palavra):
    #print(palavra)
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
        token["valor"] = token["valor"].lower()
    if(palavra[0].isupper()):
        token["tipo"] = "TYPE"
    if(token["tipo"] == "Tipo"):
        token["tipo"] = "ID"
    return token

# PR, Class, String, Numero, Operador, Variavel, Delimitator


def lexico():
    global prox_token, c, f, num_linha
    
    if prox_token is not None:
        token = prox_token
        prox_token = None
        return token

    palavra = ""
    lemos_aspas = False
    comentario_bloco = 0 # COOL permite comentários aninhados (* (* *) *)
    comentario_linha = False

    while True:
        # 1. Tenta ler o próximo caractere se c estiver "vazio"
        if c == '' or c == ' ' or c == '\t' or c == '\r':
            c = f.read(1)
        
        if not c: 
            return tipador("Fim do Arquivo")

        # 2. Gerenciamento de Quebra de Linha
        if c == '\n':
            num_linha += 1
            comentario_linha = False # Termina comentário de linha
            c = f.read(1)
            continue

        # 3. Se estiver em comentário de linha, ignora tudo até o \n
        if comentario_linha:
            c = f.read(1)
            continue

        # 4. Tratamento de Comentários de Bloco (* *)
        if c == '(':
            proximo = f.read(1)
            if proximo == '*':
                comentario_bloco += 1
                c = ' ' # Limpa para a próxima iteração
                continue
            else:
                # Se não era comentário, devolve o caractere pro buffer
                f.seek(f.tell()-1) 
        
        if c == '*' and comentario_bloco > 0:
            proximo = f.read(1)
            if proximo == ')':
                comentario_bloco -= 1
                c = ' '
                continue
            else:
                f.seek(f.tell()-1)

        if comentario_bloco > 0:
            c = f.read(1)
            continue

        # 5. Comentário de Linha --
        if c == '-':
            proximo = f.read(1)
            if proximo == '-':
                comentario_linha = True
                c = ' '
                continue
            else:
                f.seek(f.tell()-1)

        # 6. Captura de Strings
        if c == '"':
            palavra += c
            c = f.read(1)
            while c and c != '"':
                if c == '\n': num_linha += 1
                palavra += c
                c = f.read(1)
            palavra += c # fecha aspas
            c = ' '
            return tipador(palavra)

        # 7. Operadores Compostos e Delimitadores
        if c in "{}();:~+-*/=.,@<>":
            # Verificar se é <- ou <= ou =>
            if c in '<=>':
                proximo = f.read(1)
                if (c == '<' and proximo in '=-') or (c == '=' and proximo == '>'):
                    token_composto = c + proximo
                    c = ' '
                    return tipador(token_composto)
                else:
                    f.seek(f.tell()-1)
            
            aux = c
            c = ' '
            return tipador(aux)

        # 8. Identificadores, Palavras Reservadas e Números
        if c.isalnum() or c == '_':
            palavra = ""
            while c.isalnum() or c == '_':
                palavra += c
                c = f.read(1)
            return tipador(palavra)
        
        # Se for espaço ou algo não identificado, pula
        c = ' '
                

def peek():
    global prox_token
    if prox_token is None:
        prox_token = lexico()
    return prox_token