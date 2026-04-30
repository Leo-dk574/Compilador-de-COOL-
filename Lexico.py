global num_linha
num_linha = 1
global f
global c
c = '' 
global prox_token
prox_token = None

def arquivoOpen(nome):
    global f, c
    f = open(nome, "r")
    c = f.read(1) # Inicializa o primeiro caractere aqui

def tipador(palavra):
    print(palavra)
    token = {"tipo": "Tipo", "valor": palavra}
    if palavra == "Fim do Arquivo":
        token["tipo"] = "EOF"
        return token
    if palavra[0] == '"':
        token["tipo"] = "String"
    elif palavra.isdecimal():
        token["tipo"] = "Numero"
    elif palavra in ["+", "-", "<", "<=", "=>", "<-", "*", "/", "~", "="]:
        token["tipo"] = "Operador"
    elif palavra in "{}();:~.,@": # Removi o +-*/= daqui pois são operadores
        token["tipo"] = "Delimitador"
    
    # Palavras Reservadas (Case Insensitive exceto true/false que começam com minúscula)
    pr_list = ["class","inherits","if","then","fi","while","loop","pool","let","in","case","of","esac","new","isvoid","not"]
    if palavra.lower() in pr_list or palavra in ["true", "false"]:
        token["tipo"] = "PR"
        token["valor"] = palavra.lower()
    elif palavra[0].isupper():
        token["tipo"] = "TYPE"
    
    if token["tipo"] == "Tipo":
        token["tipo"] = "ID"
    return token

def lexico():
    global prox_token, c, f, num_linha
    
    if prox_token is not None:
        token = prox_token
        prox_token = None
        return token

    while True:
        # 1. Pular espaços e contar linhas
        while c and c in ' \t\r\n':
            if c == '\n':
                num_linha += 1
            c = f.read(1)

        if not c:
            return tipador("Fim do Arquivo")

        # 2. Comentário de Bloco (* *)
        if c == '(':
            proximo = f.read(1)
            if proximo == '*':
                profundidade = 1
                while profundidade > 0:
                    c = f.read(1)
                    if not c: break 
                    if c == '\n': num_linha += 1
                    if c == '(':
                        proximo = f.read(1)
                        if proximo == '*': profundidade += 1
                    elif c == '*':
                        proximo = f.read(1)
                        if proximo == ')': profundidade -= 1
                c = f.read(1) 
                continue 
            else:
                aux = c
                c = proximo 
                return tipador(aux)

        # 3. Comentário de Linha -- OU Operador -
        if c == '-':
            proximo = f.read(1)
            if proximo == '-':
                while c and c != '\n':
                    c = f.read(1)
                continue 
            else:
                aux = c
                c = proximo
                return tipador(aux)

        # 4. Operadores Compostos e Simples (<, <-, <=, =, =>)
        if c == '<':
            proximo = f.read(1)
            if proximo in ['-', '=']:
                val = c + proximo
                c = f.read(1)
                return tipador(val)
            else:
                val = c
                c = proximo
                return tipador(val)
        
        if c == '=':
            proximo = f.read(1)
            if proximo == '>':
                val = c + proximo
                c = f.read(1)
                return tipador(val)
            else:
                val = c
                c = proximo
                return tipador(val)

        # 5. Strings
        if c == '"':
            palavra = '"'
            c = f.read(1)
            while c and c != '"':
                if c == '\n': num_linha += 1
                if c == '\\': 
                    palavra += c
                    c = f.read(1)
                palavra += c
                c = f.read(1)
            palavra += '"'
            c = f.read(1)
            return tipador(palavra)

        # 6. Identificadores e Números
        if c.isalnum() or c == '_':
            palavra = ""
            while c and (c.isalnum() or c == '_'):
                palavra += c
                c = f.read(1)
            return tipador(palavra)

        # 7. Delimitadores E Operadores Restantes (+, *, /, ~, etc.)
        # Adicionei todos os símbolos que o COOL usa aqui
        if c in "{}();:~+*/.,@":
            aux = c
            c = f.read(1)
            return tipador(aux)

        # Se for um caractere que não reconhecemos (ex: um símbolo estranho)
        # imprimimos para depuração e pulamos
        # print(f"Caractere ignorado: {c}")
        c = f.read(1)
                

def peek():
    global prox_token
    if prox_token is None:
        prox_token = lexico()
    return prox_token