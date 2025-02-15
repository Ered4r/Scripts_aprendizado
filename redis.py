import subprocess
import json
import sys

def red_vuln(host, port):
    detected = False
    details = ""

    try:
        # Usa Popen para interpretar o pipe, sem utilizar shell=True
        echo_process = subprocess.Popen(["echo", "quit"], stdout=subprocess.PIPE)
        nc_process = subprocess.Popen(
            ["nc", "-v", host, port],
            stdin=echo_process.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Usa o communicate para enviar os dados e aguardar o resultado
        stdout, stderr = nc_process.communicate(timeout=10)

        # Confere se o stderr contém as strings "redis" e "open"
        if "redis" in stderr.lower() and "open" in stderr.lower():
            detected = True
            details = "REDIS vulneravel"
        else:
            details = "REDIS seguro"

    except subprocess.TimeoutExpired:
        details = f"Timeout ao tentar se conectar com o host: {host}."
    except subprocess.CalledProcessError as e:
        details = f"Erro ao executar o comando nc: {e}"
    except FileNotFoundError:
        details = "Comando nc não encontrado."

    # Retorna o resultado como dicionário
    result = {
        'detected': detected,
        'details': details,
    }

    return result

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Modo de uso: python redis.py <hostname_ou_ip> <porta>")
        sys.exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    result = red_vuln(host, port)

    # Exibe o resultado como JSON
    print(json.dumps(result))