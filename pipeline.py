"""
Data Quality Pipeline
----------------------
Le um arquivo CSV, valida a qualidade dos dados e gera um relatorio
apontando problemas encontrados. O pipeline NAO corrige os dados
automaticamente - ele alerta, e quem decide o que fazer e a pessoa
responsavel pelos dados (mesmo principio de um sistema de apoio a
decisao: alerta, nao decide sozinho).

Uso:
    python pipeline.py caminho/para/arquivo.csv
"""

import sys
import pandas as pd
from datetime import datetime


def carregar_dados(caminho_arquivo):
    """Etapa 1: Entrada - le o arquivo CSV ou Excel, detectando pela extensao."""
    if caminho_arquivo.endswith(".csv"):
        return pd.read_csv(caminho_arquivo)
    elif caminho_arquivo.endswith((".xlsx", ".xls")):
        return pd.read_excel(caminho_arquivo)
    else:
        raise ValueError(
            "Formato de arquivo nao suportado. Use um arquivo .csv, .xlsx ou .xls."
        )


def checar_duplicatas(df, colunas_chave, coluna_id):
    """Verifica linhas duplicadas com base nas colunas_chave informadas.

    colunas_chave: lista de colunas que, juntas, identificam um registro
                   (ex.: ["nome", "data_nascimento"] ou ["Member ID"])
    coluna_id:     coluna usada apenas para exibir quais linhas duplicaram
    """
    duplicadas = df[df.duplicated(subset=colunas_chave, keep=False)]
    if not duplicadas.empty:
        return f"{len(duplicadas)} linhas duplicadas encontradas (ids: {list(duplicadas[coluna_id])})"
    return None


def checar_campos_vazios(df, colunas, coluna_id):
    """Verifica campos obrigatorios vazios em cada coluna informada."""
    alertas = []
    for coluna in colunas:
        vazios = df[df[coluna].isna()]
        if not vazios.empty:
            alertas.append(f"Campo '{coluna}' vazio nos ids: {list(vazios[coluna_id])}")
    return alertas


def checar_datas_invalidas(df, coluna_data, coluna_id, ano_minimo=1920):
    """Verifica datas na coluna_data que estao no futuro ou anteriores ao ano_minimo."""
    alertas = []
    hoje = datetime.now()
    datas = pd.to_datetime(df[coluna_data], errors="coerce")

    futuras = df[datas > hoje]
    if not futuras.empty:
        alertas.append(f"Data em '{coluna_data}' no futuro nos ids: {list(futuras[coluna_id])}")

    antigas = df[datas.dt.year < ano_minimo]
    if not antigas.empty:
        alertas.append(f"Data em '{coluna_data}' improvavel (antes de {ano_minimo}) nos ids: {list(antigas[coluna_id])}")

    return alertas


def gerar_relatorio(problemas):
    """Etapa 3: Relatorio - imprime os alertas encontrados."""
    print("\n=== RELATORIO DE QUALIDADE ===")
    if problemas:
        for i, p in enumerate(problemas, 1):
            print(f"{i}. {p}")
    else:
        print("Nenhum problema encontrado.")
    print(f"\nTotal de alertas: {len(problemas)}")


def rodar_pipeline(caminho_arquivo, colunas_chave, coluna_id, checar_vazios=None, ano_minimo_data=None, coluna_data=None):
    """Executa o pipeline completo: entrada -> validacao -> relatorio.

    colunas_chave:   colunas usadas para detectar duplicatas nesse arquivo
    coluna_id:       coluna usada para identificar cada linha no relatorio
    checar_vazios:   lista opcional de colunas para checar campos vazios
    coluna_data:     coluna opcional de data para checar datas invalidas
    ano_minimo_data: ano minimo aceitavel para coluna_data (padrao 1920)
    """
    df = carregar_dados(caminho_arquivo)

    print("=== DADOS ORIGINAIS ===")
    print(df)
    print(f"\nTotal de linhas: {len(df)}")

    problemas = []

    dup = checar_duplicatas(df, colunas_chave, coluna_id)
    if dup:
        problemas.append(dup)

    if checar_vazios:
        problemas.extend(checar_campos_vazios(df, checar_vazios, coluna_id))

    if coluna_data:
        problemas.extend(
            checar_datas_invalidas(df, coluna_data, coluna_id, ano_minimo_data or 1920)
        )

    gerar_relatorio(problemas)
    return problemas


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python pipeline.py caminho/para/arquivo.csv [coluna_chave] [coluna_id]")
        print("Exemplo (pacientes): python pipeline.py dados/exemplo_pacientes.csv nome id")
        print("Exemplo (associados): python pipeline.py associados.xlsx \"Member ID\" \"Member ID\"")
        sys.exit(1)

    caminho = sys.argv[1]
    coluna_chave = sys.argv[2] if len(sys.argv) > 2 else "nome"
    coluna_id = sys.argv[3] if len(sys.argv) > 3 else "id"

    rodar_pipeline(caminho, colunas_chave=[coluna_chave], coluna_id=coluna_id)
