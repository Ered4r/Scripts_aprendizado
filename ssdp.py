import subprocess
import json
import sys

# O comando -sU no nmap precisa de permissão de root, verificar como será feito

def ssdp_vuln(host, port):
    detected = False
    details = ""

    try:
        # Executa o comando nmap e captura a saída
        result = subprocess.run(
            ["sudo", "nmap", "-sU", "-p", f"{port}", f"{host}"], 
            capture_output=True, text=True, timeout=10
        )

        # Confere se a saída contém a string 'open' e 'ssdp' ou 'upnp'
        if "open" in result.stdout.lower() and ("ssdp" in result.stdout.lower() or "upnp" in result.stdout.lower()):
            detected = True
            details = "SSDP vulneravel"
        else:
            details = "SSDP seguro"

    except subprocess.TimeoutExpired:
        details = f"Timeout ao tentar se conectar com o host: {host}."
    except FileNotFoundError:
        details = "Comando nmap não encontrado."
    except Exception as e:
        details = f"Erro ao executar o comando nmap: {e}"

    # Retorna o resultado como dicionário
    result = {
        'detected': detected,
        'details': details,
    }

    return result

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Modo de uso: python ssdp.py <hostname_ou_ip> <porta>")
        sys.exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    result = ssdp_vuln(host, port)

    # Exibe o resultado como JSON
    print(json.dumps(result))