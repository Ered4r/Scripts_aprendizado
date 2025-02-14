import subprocess
import json
import sys

def dns_vuln(host, port):
    detected = False
    details = ""

    try:
        # Executa o comando e captura a saída
        result = subprocess.run(
            ["dig", "google.com", "A", f"@{host}", "-p", f"{port}"],
            capture_output=True, text=True, timeout=10
        )

        # Confere se a saída contém a string 'flags: qr rd ra'
        if "flags: qr rd ra" in result.stdout:
            detected = True
            details = "DNS vulneravel"
        else:
            details = "DNS seguro"

    except subprocess.TimeoutExpired:
        details = f"Timeout ao tentar se conectar com o host: {host}."
    except subprocess.CalledProcessError as e:
        details = f"Erro ao executar o comando dig: {e}"
    except FileNotFoundError:
        details = "Comando dig não encontrado."

    # Retorna o resultado como dicionário
    result = {
        'detected': detected,
        'details': details,
    }

    return result

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Modo de uso: python dns.py <hostname_ou_ip> <porta>")
        sys.exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    result = dns_vuln(host, port)

    # Exibe o resultado como JSON
    print(json.dumps(result))