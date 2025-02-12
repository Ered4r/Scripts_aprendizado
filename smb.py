import subprocess
import json
import sys

def smb_vuln(host, port):
    detected = False
    details = ""

    try:
        # Execute o comando e captura a saída
        result = subprocess.run(
            ["smbclient", "-L", f"//{host}/", "-p", f"{port}", "-N"],
            capture_output=True, text=True, timeout=10
        )

        # Confere se a saída contém a string 'Sharename'
        if "Sharename" in result.stdout:
            detected = True
            details = "SMB vulneravel"
        else:
            details = "SMB seguro"

    except subprocess.TimeoutExpired:
        details = f"Timeout ao tentar se conectar com o host: {host}."
    except subprocess.CalledProcessError as e:
        details = f"Erro ao executar o comando smbclient: {e}"
    except FileNotFoundError:
        details = "Comando smbclient não encontrado."

    # Retorna o resultado como dicionário
    result = {
        'detected': detected,
        'details': details,
    }

    return result

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Modo de uso: python smb.py <hostname_ou_ip> <porta>")
        sys.exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    result = smb_vuln(host, port)

    # Exibe o resultado como JSON
    print(json.dumps(result))