import subprocess
import json
import sys

def sql_vuln(host, port):
    detected = False
    details = ""

    try:
        # Executa o comando e captura a saída
        result = subprocess.run(
            ["nmap", "-sV", "-Pn", f"{host}", "-p", f"{port}"],
            capture_output=True, text=True, timeout=10
        )

        # Confere se a saída contém a string 'open' e 'mysql'
        if "open" in result.stdout and "mysql" in result.stdout:
            detected = True
            details = "MYSQL vulneravel"
        else:
            details = "MYSQL seguro"

    except subprocess.TimeoutExpired:
        details = f"Timeout ao tentar se conectar com o host: {host}."
    except subprocess.CalledProcessError as e:
        details = f"Erro ao executar o comando nmap: {e}"
    except FileNotFoundError:
        details = "Comando nmap não encontrado."

    # Retorna o resultado como dicionário
    result = {
        'detected': detected,
        'details': details,
    }

    return result

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Modo de uso: python mysql.py <hostname_ou_ip> <porta>")
        sys.exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    result = sql_vuln(host, port)

    # Exibe o resultado como JSON
    print(json.dumps(result))