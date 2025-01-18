#!/bin/bash

if [[ -z "$1" ]]; then
  echo "Usage: $0 <hostname_or_ip>"
  exit 1
fi

snmpwalk -c public -v1 "$1" 2>/dev/null | 
  awk '{if ($0 ~ /Windows/) {print $2}}' | 
  cut -d ' ' -f 1 > teste

# Verifica se o arquivo 'teste' está vazio
if [[ -s teste ]]; then
  # Se não estiver vazio, o host está vulnerável
  echo "Vulnerável!"
else
  echo "Seguro!"
fi
