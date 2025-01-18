import subprocess

def check_os(host):

    # Executa o comando snmpwalk e captura a saída
    result = subprocess.run(
        f"snmpwalk -c public -v1 {host} 2>/dev/null | awk '{{if ($0 ~ /Windows/) print $2}}' | cut -d ' ' -f 1",
        shell=True, capture_output=True, text=True
    )

    # Verifica se a saída está vazia
    return bool(result.stdout.strip())

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python script.py <hostname_or_ip>")
        sys.exit(1)

    host = sys.argv[1]
    if check_os(host):
        print("Vulnerable!")
    else:
        print("Seguro!")
