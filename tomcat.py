import json
import subprocess
import sys

# Lista de conferência de versões vulneráveis do Apache Tomcat
VULNERABLE_VERSIONS = [
    # 11.x Versões vulneráveis
    '11.0.0-M1', '11.0.0-M2', '11.0.0-M3', '11.0.0-M4', '11.0.0-M5', '11.0.0-M6',
    '11.0.0-M7', '11.0.0-M8', '11.0.0-M9', '11.0.0-M10', '11.0.0-M11',
    '11.0.0', '11.0.1', '11.0.2',
    
    # 10.x Versões vulneráveis
    '10.1.0-M1', '10.1.0-M2', '10.1.0-M3', '10.1.0-M4', '10.1.0-M5', '10.1.0-M6',
    '10.1.0-M7', '10.1.0-M8', '10.1.0', '10.1.1', '10.1.2', '10.1.3', '10.1.4',
    '10.1.5', '10.1.6', '10.1.7', '10.1.8', '10.1.9', '10.1.10', '10.1.11',
    '10.1.12', '10.1.13', '10.1.14', '10.1.15', '10.1.16', '10.1.17', '10.1.18',
    '10.1.19', '10.1.20', '10.1.21', '10.1.22', '10.1.23', '10.1.24', '10.1.25',
    '10.1.26', '10.1.27', '10.1.28', '10.1.29', '10.1.30', '10.1.31', '10.1.32',
    '10.1.33', '10.1.34',
    
    # 9.x Versões vulneráveis
    '9.0.0.M1', '9.0.0.M2', '9.0.0.M3', '9.0.0.M4', '9.0.0.M5', '9.0.0.M6',
    '9.0.0.M7', '9.0.0.M8', '9.0.0.M9', '9.0.0.M10', '9.0.0.M11', '9.0.0.M12',
    '9.0.0.M13', '9.0.0.M14', '9.0.0.M15', '9.0.0.M16', '9.0.0.M17', '9.0.0.M18',
    '9.0.0.M19', '9.0.0.M20', '9.0.0.M21', '9.0.0.M22', '9.0.0.M23', '9.0.0.M24',
    '9.0.0.M25', '9.0.0.M26', '9.0.0', '9.0.1', '9.0.2', '9.0.3', '9.0.4', '9.0.5',
    '9.0.6', '9.0.7', '9.0.8', '9.0.9', '9.0.10', '9.0.11', '9.0.12', '9.0.13',
    '9.0.14', '9.0.15', '9.0.16', '9.0.17', '9.0.18', '9.0.19', '9.0.20', '9.0.21',
    '9.0.22', '9.0.23', '9.0.24', '9.0.25', '9.0.26', '9.0.27', '9.0.28', '9.0.29',
    '9.0.30', '9.0.31', '9.0.32', '9.0.33', '9.0.34', '9.0.35', '9.0.36', '9.0.37',
    '9.0.38', '9.0.39', '9.0.40', '9.0.41', '9.0.42', '9.0.43', '9.0.44', '9.0.45',
    '9.0.46', '9.0.47', '9.0.48', '9.0.49', '9.0.50', '9.0.51', '9.0.52', '9.0.53',
    '9.0.54', '9.0.55', '9.0.56', '9.0.57', '9.0.58', '9.0.59', '9.0.60', '9.0.61',
    '9.0.62', '9.0.63', '9.0.64', '9.0.65', '9.0.66', '9.0.67', '9.0.68', '9.0.69',
    '9.0.70', '9.0.71', '9.0.72', '9.0.73', '9.0.74', '9.0.75', '9.0.76', '9.0.77',
    '9.0.78', '9.0.79', '9.0.80', '9.0.81', '9.0.82', '9.0.83', '9.0.84', '9.0.85',
    '9.0.86', '9.0.87', '9.0.88', '9.0.89', '9.0.90', '9.0.91', '9.0.92', '9.0.93',
    '9.0.94', '9.0.95', '9.0.96', '9.0.97', '9.0.98'
]

def tomcat_vuln(host, port):
    detected = False
    details = ''
    version_found = ''

    try:
        # Executa o comando nmap para detectar o Apache Tomcat
        result = subprocess.run(
            ['nmap', '-sV', '-Pn', f'{host}', '-p', f'{port}', '--script', 'http-server-header.nse'],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

        # Confere se o Apache Tomcat está funcionando
        if 'open' in result.stdout and 'tomcat' in result.stdout.lower():
            # Extrai a versão do Apache Tomcat
            for line in result.stdout.split('\n'):
                if 'tomcat' in line.lower():
                    # Acha a versão do Tomcat
                    # Exemplo de linha: "Apache Tomcat/9.0.54"
                    parts = line.lower().split('tomcat')
                    if len(parts) > 1:
                        version_part = parts[1].strip().split()[0]
                        version_found = version_part.split('/')[-1].strip()
                        break

            # Confere se a versão encontrada é vulnerável
            if version_found:
                for vulnerable_version in VULNERABLE_VERSIONS:
                    if version_found.startswith(vulnerable_version):
                        detected = True
                        details = f'A versão {version_found} é vulnerável'
                        break
                
                if not detected:
                    details = f'A versão {version_found} não é vulnerável'
            else:
                details = 'A versão do Apache Tomcat não foi encontrada'
        else:
            details = 'O Apache Tomcat não está funcionando ou não é acessível na porta especificada'

    except subprocess.TimeoutExpired:
        details = f'Timeout ao tentar se conectar com o host: {host}.'
    except subprocess.CalledProcessError as e:
        details = f'Erro ao executar o comando nmap: {e}'
    except FileNotFoundError:
        details = 'Comando nmap não encontrado.'
    except Exception as e:
        details = f'Erro inesperado: {str(e)}'

    # Retorna a resposta como dicionário
    result = {
        'detected': detected,
        'details': details,
        'version': version_found if version_found else 'Não encontrado',
    }

    return result


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Modo de uso: python tomcat.py <hostname_ou_ip> <porta>')
        sys.exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    result = tomcat_vuln(host, port)

    # Exibe o resultado como JSON
    print(json.dumps(result, indent=2))