import subprocess
import json
import sys

def slp_vuln(host, port):
    detected = False
    details = ""

    try:
        # Executa o comando e captura a saída
        result = subprocess.run(
            ["sudo", "nmap", "-sS", "-Pn", f"{host}", "-p", f"{port}"],
            capture_output=True, text=True, timeout=10
        )

        # Confere se a saída contém a string 'open' e 'svrloc'
        if "open" in result.stdout and "svrloc" in result.stdout:
            detected = True
            details = "SLP vulneravel"
        else:
            details = "SLP seguro"

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
        print("Modo de uso: python slp.py <hostname_ou_ip> <porta>")
        sys.exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    result = slp_vuln(host, port)

    # Exibe o resultado como JSON
    print(json.dumps(result))