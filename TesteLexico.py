import sys
import Lexico

def main():
    if len(sys.argv) < 2:
        print("Uso: py Main.py <numero_do_exemplo>")
        return

    numero = sys.argv[1]

    caminho = f"Exemplos/Ex{numero}.txt"

    try:
        Lexico.arquivoOpen(caminho)
    except FileNotFoundError:
        print(f"Arquivo {caminho} não encontrado.")
        return

    token = {
        "tipo": "",
        "valor": ""
    }
    while(token["tipo"] != "EOF"):
        token = Lexico.lexico()
        print(f"{token["valor"]}   {token["tipo"]}   n:{Lexico.num_linha}")


if __name__ == "__main__":
    main()