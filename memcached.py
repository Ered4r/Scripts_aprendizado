import subprocess
import json
import sys

def mem_vuln(host, port):
    detected = False
    details = ""

    try:
        # Executa o comando e captura a saída
        result = subprocess.run(
            ["nmap", "-sV", "-Pn", f"{host}", "-p", f"{port}"],
            capture_output=True, text=True, timeout=10
        )

        # Confere se a saída contém a string 'open' e 'memcached'
        if "open" in result.stdout and "memcached" in result.stdout:
            detected = True
            details = "MEMCACHED vulneravel"
        else:
            details = "MEMCACHED seguro"

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
        print("Modo de uso: python memcached.py <hostname_ou_ip> <porta>")
        sys.exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    result = mem_vuln(host, port)

    # Exibe o resultado como JSON
    print(json.dumps(result))