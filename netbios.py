import subprocess
import json
import sys

#No comando nmblookup, não é possível especificar a porta, pois ele utiliza a porta 137 por padrão, então o argumento é recebido, mas não utilizado.

def nmb_vuln(host, port):
    detected = False
    details = ""

    try:
        # Executa o comando e captura a saída
        result = subprocess.run(
            ["nmblookup", "-A", f"{host}"],
            capture_output=True, text=True, timeout=10
        )

        # Confere se a saída contém a string 'ACTIVE'
        if "ACTIVE" in result.stdout:
            detected = True
            details = "NETBIOS vulneravel"
        else:
            details = "NETBIOS seguro"

    except subprocess.TimeoutExpired:
        details = f"Timeout ao tentar se conectar com o host: {host}."
    except subprocess.CalledProcessError as e:
        details = f"Erro ao executar o comando nmblookup: {e}"
    except FileNotFoundError:
        details = "Comando nmblookup não encontrado."

    # Retorna o resultado como dicionário
    result = {
        'detected': detected,
        'details': details,
    }

    return result

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Modo de uso: python netbios.py <hostname_ou_ip> <porta>")
        sys.exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    result = nmb_vuln(host, port)

    # Exibe o resultado como JSON
    print(json.dumps(result))