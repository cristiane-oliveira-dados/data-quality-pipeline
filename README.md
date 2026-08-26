# Data Quality Pipeline

Pipeline simples em Python que le uma base de dados (CSV), valida a
qualidade das informacoes e gera um relatorio apontando problemas
como duplicatas, campos vazios e valores impossiveis.

## Motivacao

Com experiencia previa em enfermagem, QA e cibersegurança, este projeto
nasce da percepcao de que dados "sujos" (duplicados, incompletos ou
inconsistentes) sao uma causa comum de erro em analises - da mesma forma
que erros de registro em prontuarios podem comprometer decisoes clinicas.

O pipeline aplica uma logica de QA (teste e validacao) diretamente sobre
os dados, antes que eles cheguem a qualquer analise ou tomada de decisao.

**Principio de design:** o sistema alerta sobre os problemas encontrados,
mas nao corrige nada sozinho. A decisao sobre o que fazer com cada alerta
e sempre de quem esta responsavel pelos dados.

## O que o pipeline verifica

- **Duplicatas** - linhas com mesmo nome e mesma data de nascimento
- **Campos obrigatorios vazios** - ex: idade ou cidade nao preenchidas
- **Datas de nascimento invalidas** - datas no futuro ou anteriores a 1920

## Como usar

### Pre-requisitos

- Python 3.8 ou superior
- Biblioteca pandas

### Instalacao

```bash
pip install -r requirements.txt
```

### Executando

```bash
python pipeline.py dados/exemplo_pacientes.csv
```

### Exemplo de saida

```
=== RELATORIO DE QUALIDADE ===
1. 4 linhas duplicadas encontradas (ids: [1, 2, 3, 7])
2. Campo 'idade' vazio nos ids: [4]
3. Campo 'cidade' vazio nos ids: [6]
4. Data de nascimento no futuro nos ids: [5]
5. Data de nascimento improvavel (antes de 1920) nos ids: [8]

Total de alertas: 5
```

## Estrutura do projeto

```
data-quality-pipeline/
├── pipeline.py              # Script principal
├── dados/
│   └── exemplo_pacientes.csv  # Dataset fictício para testes
├── relatorios/               # Pasta reservada para relatorios gerados
├── requirements.txt
└── README.md
```

## Proximos passos (roadmap)

- [ ] Exportar relatorio em Excel/PDF
- [ ] Calcular um "score de qualidade" geral do dataset (% de linhas sem problemas)
- [ ] Adicionar testes automatizados (pytest) para cada funcao de validacao
- [ ] Testar com dados publicos reais (ex: DATASUS, OpenDataSUS)
- [ ] Permitir configurar as regras de validacao via arquivo externo (json/yaml)

## Autora

Projeto desenvolvido como parte de portfolio de transicao de carreira,
unindo experiencia em enfermagem, QA e analise de dados.
