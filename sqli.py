import json
import subprocess
import sys
import shlex

def sql_injection_test(ip, parameter):
    detected = False
    details = ''
    
    # Constrói a URL com o parâmetro a ser testado
    url = f"http://{ip}/?{parameter}=*"
    
    command = [
        'sqlmap',
        '-u', url,
        '--technique=E',  # Seleciona a técnica error-based
        '--level=5',       # Maior nível de testes
        '--risk=3',        # Maior risco de testes
        '--batch',         # Modo não-interativo
        '--answers=follow=Y',
        '--flush-session'
    ]
    
    try:
        # Executa o comando e captura a saída
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=300,
            check=False
        )

        # Checa se a saída contém as strings 'SQL injection' ou 'injectable'
        if any(phrase in result.stdout for phrase in ['SQL injection', 'injectable']):
            if 'not vulnerable' not in result.stdout:
                detected = True
                details = 'Vulnerabilidade SQL injection detectada'
                
                # Extrai as linhas relevantes da saída
                vuln_lines = [line for line in result.stdout.split('\n') 
                            if any(keyword in line.lower() 
                                  for keyword in ['injection', 'parameter', 'payload'])]
                details += '\n' + '\n'.join(vuln_lines[:10])  # Mostra as 10 linhas mais relevantes
        else:
            details = 'Nenhuma vulnerabilidade SQL injection detectada'

    except subprocess.TimeoutExpired:
        details = f'Timeout ao testar a URL: {url}'
    except subprocess.CalledProcessError as e:
        details = f'Erro ao executar sqlmap: {e}\nOutput: {e.output}'
    except FileNotFoundError:
        details = 'Comando sqlmap não encontrado.'
    except Exception as e:
        details = f'Erro inesperado: {str(e)}'

    return {
        'detected': detected,
        'details': details.strip(),
        'command': ' '.join(shlex.quote(arg) for arg in command),
        'url': url
    }

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Modo de uso: python3 sqli.py <ip_address> <parameter>")
        print("Exemplo: python3 sqli.py 10.10.0.7 search")
        sys.exit(1)
    
    ip = sys.argv[1]
    parameter = sys.argv[2]
    
    try:
        result = sql_injection_test(ip, parameter)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)