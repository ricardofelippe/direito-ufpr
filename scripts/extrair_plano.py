import json
import re
import subprocess
import sys
from pathlib import Path

DATA_RE = re.compile(r'^(\d{2})/(0[1-9]|1[0-2])/(\d{4})$')
ROMANOS = {'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII'}


def extrair_texto(pdf_path):
    result = subprocess.run(
        ['pdftotext', '-layout', str(pdf_path), '-'],
        check=True, capture_output=True, text=True, encoding='utf-8'
    )
    return result.stdout.replace('\r', '')


def separar_secoes(texto):
    linhas = [linha.strip() for linha in texto.splitlines()]
    marcadores = {
        'ementa': re.compile(r'^1\.\s*Ementa$', re.I),
        'objetivos': re.compile(r'^2\.\s*Objetivos$', re.I),
        'conteudo_programatico': re.compile(r'^3\.\s*Conteúdo programático$', re.I),
        'cronograma': re.compile(r'^4\.\s*Cronograma', re.I),
        'avaliacao': re.compile(r'^5\.\s*Avaliação$', re.I),
        'bibliografia': re.compile(r'^6\.\s*Bibliografia$', re.I),
    }
    encontrados = []
    for i, linha in enumerate(linhas):
        for chave, padrao in marcadores.items():
            if padrao.match(linha):
                encontrados.append((i, chave))
                break
    resultado = {}
    for pos, (inicio, chave) in enumerate(encontrados):
        fim = encontrados[pos + 1][0] if pos + 1 < len(encontrados) else len(linhas)
        resultado[chave] = [linha for linha in linhas[inicio + 1:fim] if linha]
    return resultado


def juntar(linhas):
    return ' '.join(linhas).strip()


def parse_conteudos(linhas):
    itens = []
    for linha in linhas:
        match = re.match(r'^([IVX]+)\s{2,}(.+)$', linha)
        if match and match.group(1) in ROMANOS:
            itens.append({'unidade': match.group(1), 'conteudo': match.group(2).strip()})
    return itens


def parse_cronograma(linhas):
    itens = []
    for linha in linhas:
        match = re.match(r'^(\d{2}/\d{2}/\d{4})\s{2,}(.+)$', linha)
        if match and DATA_RE.match(match.group(1)):
            itens.append({'data': match.group(1), 'atividade': match.group(2).strip()})
    return itens


def extrair(pdf_path):
    partes = separar_secoes(extrair_texto(pdf_path))
    return {
        'status_extracao': 'pre_visualizacao',
        'ementa': juntar(partes.get('ementa', [])),
        'objetivos': juntar(partes.get('objetivos', [])),
        'conteudos_programaticos': parse_conteudos(partes.get('conteudo_programatico', [])),
        'cronograma': parse_cronograma(partes.get('cronograma', [])),
        'avaliacao': juntar(partes.get('avaliacao', [])),
        'bibliografia': juntar(partes.get('bibliografia', [])),
        'observacao': 'Dados extraídos automaticamente. Conferir antes de confirmar qualquer incorporação.'
    }


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('Uso: python scripts/extrair_plano.py arquivo.pdf saida.json')
    origem, destino = map(Path, sys.argv[1:3])
    dados = extrair(origem)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({
        'ementa': bool(dados['ementa']),
        'unidades': len(dados['conteudos_programaticos']),
        'itens_cronograma': len(dados['cronograma']),
        'avaliacao': bool(dados['avaliacao'])
    }, ensure_ascii=False))
