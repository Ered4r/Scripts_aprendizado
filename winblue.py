import subprocess
import json
import sys

def win_vuln(host, port):
    detected = False
    details = ""

    try:
        # Executa o comando e captura a saída
        result = subprocess.run(
            ["nmap", "-Pn", f"{host}", "-p", f"{port}", "--script", "smb-vuln-ms17-010"],
            capture_output=True, text=True, timeout=10
        )

        # Confere se a saída contém a string 'VULNERABLE'
        if "VULNERABLE" in result.stdout:
            detected = True
            details = "Windows vulneravel"
        else:
            details = "Windows seguro"

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
        print("Modo de uso: python winblue.py <hostname_ou_ip> <porta>")
        sys.exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    result = win_vuln(host, port)

    # Exibe o resultado como JSON
    print(json.dumps(result))