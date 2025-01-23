import subprocess
import sys

def check_os(host, port):
    result = subprocess.run(
        f"snmpwalk -c public -v1 {host}:{port} 2>/dev/null | awk '{{if ($0 ~ /Windows/) print $2}}' | cut -d ' ' -f 1",
        shell=True, capture_output=True, text=True
    )
    return bool(result.stdout.strip())

def smb_vuln(host, port):
    result = subprocess.run(
        f"smbclient -L //{host}/:{port} -U 'Convidado' -N 2>/dev/null | awk '{{if ($0 ~ /listing/) print $2}}' ",
        shell=True, capture_output=True, text=True
    )
    return bool(result.stdout.strip())

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Modo de uso: python script.py <hostname_ou_ip> <porta> <vulnerabilidade>")
        print("Vulnerabilidade: snmp or smb")
        sys.exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    vuln_type = sys.argv[3]

    if vuln_type == "snmp":
        if check_os(host, port):
            print("SNMP Vulnerável, procure o suporte técnico responsável!")
        else:
            print("SNMP Seguro!")
    elif vuln_type == "smb":
        if smb_vuln(host, port):
            print("SMB Vulnerável, procure o suporte técnico responsável!")
        else:
            print("SMB Seguro!")
    else:
        print("Vulnerabilidade inválida. Digite 'snmp' ou 'smb'.")
        sys.exit(1)