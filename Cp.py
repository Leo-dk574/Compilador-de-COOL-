global num_linha
num_linha = 1

global f
f = open("nome_do_arq.txt")

global c
c = ' '

def lexico():
 global c
 global f
 global num_linha
 palavra = ""
 lemos_aspas = False
 comentario = False
 comentario_linha = False
 while(True):
    if c == '\n':
        if comentario_linha:
            comentario_linha = False
        num_linha += 1
    if c in "{}();~+-*/=.,@" and not lemos_aspas and (not comentario and not comentario_linha):
        if c == '=':
            aux2 = f.read(1)
            if aux2 == '>':
                c = c+aux2
            else:
                f.seek(f.tell()-1,0)

        aux = c
        c = ' '
        return aux
    else:
        c = f.read(1)
        if not c: 
            return "Fim do arquivo"
        if c in '(-' or (c == '*' and comentario):
            aux = f.read(1)
            if aux in '*-' or (aux == ')' and comentario):
                if c == '-' and aux == '-':
                    comentario_linha = True
                else:
                    comentario = not comentario
                c = ' '
                aux = ' '
            else:
                f.seek(f.tell()-1,0)
        if c == '<':
            aux = f.read(1)
            if aux == '-' or aux == '=':
                if palavra != '':
                    f.seek(f.tell()-2,0)
                    return palavra
                else:
                    return c+aux
            else:
                if palavra != '':
                    f.seek(f.tell()-2,0)
                    return palavra
                else:
                    f.seek(f.tell()-1,0)
                    return c
        if not comentario and not comentario_linha:
            if c == '"':
                lemos_aspas = not lemos_aspas
            if c not in " '\t''\n'{}();~+-*/=.,@" or lemos_aspas:
                palavra += c
            else:
                if palavra != "":
                    return palavra


def sintatico():
    token = ""
    while(token != "Fim do arquivo"):
        token = lexico()
        print(token, num_linha, sep=' n:')
       
sintatico()
