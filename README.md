[README.md](https://github.com/user-attachments/files/31816509/README.md)
# Data Quality Pipeline

Pipeline em Python que le uma base de dados (CSV ou Excel), valida a
qualidade das informacoes e gera um relatorio apontando problemas
como registros duplicados. O objetivo nao e corrigir os dados
automaticamente, e sim **alertar** quem e responsavel por eles, para
que a decisao final continue sendo humana.

---

## Estudo de caso

### Introducao

Bases de dados usadas no dia a dia de uma empresa raramente chegam
perfeitas. Duplicatas, campos vazios e valores inconsistentes sao
comuns quando os dados vem de cadastros manuais, planilhas separadas
ou sistemas diferentes sendo unificados. Um erro desse tipo, se nao
detectado antes da analise, pode levar a decisoes erradas ou custos
desnecessarios.

Este projeto nasceu com um objetivo simples: criar uma ferramenta que
identifique esses problemas **antes** que os dados cheguem a qualquer
relatorio ou tomada de decisao, aplicando um raciocinio de teste e
validacao (QA) diretamente sobre os dados.

Para validar a ferramenta, ela foi testada tanto com uma base
fictícia (cadastro de pacientes) quanto com uma base real, disponibilizada
como material de estudo no Certificado em Analise de Dados do Google:
um cadastro de associados de uma associacao internacional de logistica,
contendo 71 registros.

### Problemas

Ao rodar o pipeline sobre a base real de associados, o script identificou
uma linha duplicada: o `Member ID 100027` (Christophe de Alava Casado)
aparecia cadastrado duas vezes na planilha, com o mesmo valor de
mensalidade (`Dues amount = 500`) em ambos os registros.

Durante a analise, outros pontos "estranhos" tambem foram observados
manualmente na base, como um erro de digitacao no campo de tipo de
associado (um valor que deveria ser `Professional Member` aparecia
como `{rofessional Member`) e algumas datas de validade de associacao
bem mais antigas que a maioria dos registros.

Optou-se por nao transformar todos esses achados em regras automaticas
de validacao. A decisao de priorizar foi guiada por uma pergunta:
**qual e a consequencia real se esse problema passar despercebido?**

- Um `Member ID` duplicado pode gerar **cobranca duplicada** de
  mensalidade, ou inflar artificialmente o numero total de associados
  em um relatorio -- um impacto financeiro e operacional concreto.
- Um erro de digitacao em uma unica linha de categoria afeta apenas
  a contagem por tipo de associado em um relatorio -- um problema
  menor, sem impacto financeiro direto.

Por esse motivo, a regra de deteccao de duplicatas foi a escolhida
para compor a primeira versao funcional do pipeline.

### Solucoes

A solucao foi um script (`pipeline.py`) organizado em funcoes
reutilizaveis, seguindo o fluxo:

1. **Entrada** -- le o arquivo (CSV ou Excel, detectado automaticamente
   pela extensao).
2. **Validacao** -- verifica duplicatas com base em uma ou mais colunas
   escolhidas por quem esta rodando o pipeline (por exemplo, `nome` em
   uma base de pacientes, ou `Member ID` em uma base de associados).
3. **Relatorio** -- imprime os alertas encontrados, sem alterar o
   arquivo original.

Uma alternativa considerada foi corrigir a duplicata automaticamente
(removendo a linha repetida). Essa opcao foi descartada de proposito:
remover dados sem confirmacao humana pode apagar informacao relevante
por engano (por exemplo, dois membros diferentes que, por coincidencia,
tenham o mesmo ID por erro de digitacao em outro campo). O pipeline
prioriza a **transparencia do alerta** sobre a correcao automatica.

Rodando o pipeline sobre a base real de associados:

```
python pipeline.py associados.xlsx "Member ID" "Member ID"
```

Resultado:

```
=== RELATORIO DE QUALIDADE ===
1. 2 linhas duplicadas encontradas (ids: [100027, 100027])

Total de alertas: 1
```

### Conclusao

O projeto mostrou, na pratica, que mesmo uma base de dados pequena
(71 linhas) pode conter erros reais com impacto financeiro. Tambem
reforcou a importancia de **priorizar** quais problemas validar,
em vez de tentar detectar tudo de uma vez -- nem todo dado incomum
e, de fato, um erro que merece virar regra automatizada.

### Proximas etapas

- [ ] Adicionar deteccao de valores fora de uma lista de categorias
      esperadas (ex.: tipos de associado), para pegar erros de
      digitacao como o `{rofessional Member` encontrado manualmente.
- [ ] Exportar o relatorio em Excel ou PDF, alem do texto no terminal.
- [ ] Calcular um "score de qualidade" geral do dataset.
- [ ] Adicionar testes automatizados (pytest) para cada regra de validacao.
- [ ] Aplicar o pipeline a dados publicos de saude (ex.: DATASUS,
      OpenDataSUS), area de interesse pessoal da autora.

---

## Como usar

### Pre-requisitos

- Python 3.8 ou superior
- Bibliotecas pandas e openpyxl

### Instalacao

```bash
pip install -r requirements.txt
```

### Executando

```bash
python pipeline.py caminho/para/arquivo.csv coluna_chave coluna_id
```

- `coluna_chave`: coluna usada para identificar duplicatas (ex.: `nome`, `"Member ID"`)
- `coluna_id`: coluna usada para exibir quais linhas duplicaram no relatorio

Exemplos:

```bash
python pipeline.py dados/exemplo_pacientes.csv nome id
python pipeline.py associados.xlsx "Member ID" "Member ID"
```

## Estrutura do projeto

```
data-quality-pipeline/
├── pipeline.py                 # Script principal
├── dados/
│   └── exemplo_pacientes.csv     # Dataset fictício para testes
├── relatorios/                  # Pasta reservada para relatorios gerados
├── requirements.txt
└── README.md
```

## Autora

Projeto desenvolvido como parte de portfolio de transicao de carreira,
unindo experiencia previa em enfermagem, QA e cibersegurança com
novas habilidades em analise de dados (Certificado em Analise de Dados
do Google, Coursera).
