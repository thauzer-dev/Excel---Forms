# 📊 Excel Forms — Fórmulas do Excel em Python

Módulo Python com **52 funções inspiradas no Excel**, nomes em **português** e processamento de dados com **Pandas e NumPy**.

O projeto reúne buscas, agregações condicionais, operações com datas, indicadores de negócio e utilitários de texto em um único arquivo reutilizável. As funções podem ser incorporadas a scripts de análise, notebooks e rotinas de automação.

## 🎯 Sobre o Projeto

O **Excel Forms** aproxima a lógica de fórmulas usadas em planilhas do desenvolvimento em Python, permitindo aplicar operações como `PROCV`, `SOMASES` e `SOMARPRODUTO` a dados em memória.

A implementação combina funções reutilizáveis, validação de entradas e operações vetorizadas nos indicadores numéricos. Os intervalos são relacionados pela **posição dos registros**, evitando que índices diferentes do Pandas causem alinhamentos inesperados.

O projeto demonstra tratamento de dados, organização de regras de cálculo e testes de regressão aplicados a rotinas de análise e inteligência de negócios.

## ✨ Principais Recursos

### 🔎 Busca e Relacionamento

- Buscas exatas e aproximadas com `PROCV` e `PROCX`.
- Seleção da primeira ou da última correspondência com `PROCX`.
- Busca com curingas e opção de ignorar maiúsculas e minúsculas em `PROCX`.
- Retorno de uma linha completa quando o vetor de retorno de `PROCX` é um DataFrame.
- Localização por posição com `CORRESP`, `INDICE` e `INDICE_CORRESP`.
- Junções entre DataFrames com validação opcional da cardinalidade, como `many_to_one`.

### 🧮 Agregações e Critérios

- Somas, médias, contagens, mínimos e máximos condicionais.
- Múltiplos critérios combinados por **E lógico**: todos devem ser atendidos.
- Critérios numéricos como `">=100"`, `"<500"` e `"<>0"`.
- Curingas `*` e `?`, com `~` para escape.
- Critérios em tuplas, como `(">=", 100)`, ou funções que retornam booleanos.
- Comparação de datas com alvos explícitos do tipo `date`, `datetime` ou `Timestamp`.
- Produto de intervalos seguido de soma com `SOMARPRODUTO`.

### 📅 Datas e Dias Úteis

- Extração de ano, mês e dia.
- Deslocamento de meses e identificação do último dia do mês.
- Diferenças entre datas em dias, meses, anos e componentes restantes.
- Contagem inclusiva de dias úteis, com feriados informados pelo usuário.
- Deslocamento por dias úteis e personalização dos dias trabalhados na semana.
- Intervalo do início do mês até ontem, com tratamento configurável para o primeiro dia do mês.

### 📈 Indicadores de Negócio

- Margem, crescimento, ticket médio e participação.
- Distribuição percentual de uma série com `SHARE`.
- Variações por uma posição ou por uma defasagem configurável.
- Cálculos com escalares, listas, arrays e Series nas funções de divisão e indicadores derivados.
- Tratamento de divisões por zero e resultados não finitos com `NaN`.
- Variações sem preenchimento automático de valores ausentes.

### 🧹 Conversão, Texto e Seleção

- Conversão explícita de números brasileiros, moedas e percentuais com `VALOR`.
- Arredondamento de empates para longe de zero com `ARRED`.
- Limpeza de espaços e extração de trechos de texto.
- Seleção condicional com `SE` e tratamento de erros com `SEERRO`.
- Remoção de duplicatas com `UNICOS` e filtragem por máscara com `FILTRO`.

### 🧪 Demonstração e Validação

- Demonstração executável com dados fictícios.
- Listagem das funções pelo terminal.
- Documentação interna acessível por `help()`.
- **16 testes de regressão**, executáveis sem instalar um framework adicional.
- Importação do módulo sem iniciar demonstrações, ler arquivos ou acessar a rede.

## 🧮 Convenções de Cálculo

Os indicadores percentuais retornam **frações decimais**: `0.20` representa **20%**.

```text
Margem = (Receita − Custo) / Receita

Crescimento = (Valor atual − Valor anterior) / |Valor anterior|

Ticket médio = Receita total / Quantidade

Participação = Valor da parte / Valor total

Share = Valor do registro / Soma dos valores da série

Variação por N posições = Valor atual / Valor de N posições atrás − 1
```

`CRESCIMENTO` utiliza o valor absoluto da base anterior. As funções de variação preservam o sinal do denominador; por isso, podem produzir resultados diferentes para bases negativas.

| Situação | Comportamento |
| --- | --- |
| Busca sem correspondência | Retorna `None` ou o valor alternativo configurado. |
| Intervalos relacionados com tamanhos diferentes | Gera `ValueError`. |
| Critérios de agregação com texto | Ignoram maiúsculas e minúsculas. |
| Buscas exatas | Distinguem maiúsculas e minúsculas por padrão. |
| `None`, `NaN`, `NaT`, `pd.NA` e `""` nos critérios | São considerados vazios; vazio não equivale a zero. |
| Soma sem números selecionados | Retorna zero. |
| Média sem números selecionados | Retorna `NaN`. |
| Extremos condicionais sem números selecionados | Retornam `None`. |
| Texto não numérico selecionado para agregação | Gera erro, em vez de ser descartado silenciosamente. |
| Divisão por zero nos indicadores | Retorna `NaN`. |

Textos numéricos simples são aceitos nas agregações. Valores formatados, como `"R$ 1.234,56"`, devem ser convertidos explicitamente com `VALOR`.

## 🛠️ Arquitetura e Engenharia de Código

A implementação está concentrada em `formulas_excel.py`, organizada por grupos de funções e apoiada por utilitários internos de validação e processamento.

| Componente | Responsabilidade |
| --- | --- |
| `_serie()` | Normalizar vetores para operações posicionais. |
| `_numeros()` | Converter valores numéricos e rejeitar textos incompatíveis. |
| `_aplicar_criterio()` | Interpretar operadores, curingas, valores e critérios personalizados. |
| `_mascara()` | Validar tamanhos e combinar múltiplas condições. |
| `_agregar()` | Compartilhar a lógica de soma, média, mínimo e máximo. |
| `_data()` e `_calendario()` | Validar datas e configurar dias úteis e feriados. |
| `_operacao_numerica()` | Executar indicadores vetorizados e tratar resultados não finitos. |
| `_demo()` | Apresentar exemplos com dados fictícios. |
| `_testes()` | Executar a suíte de regressão com `unittest`. |
| `_main()` | Interpretar os argumentos da linha de comando. |

As buscas aproximadas selecionam candidatos sem ordenar a tabela inteira. A contagem de dias úteis utiliza as operações de calendário do NumPy. Não há dependência do Microsoft Excel para executar as funções.

## 🚀 Como Executar o Projeto

### 1. Prepare o ambiente

Utilize **Python 3.10 ou superior**. Na pasta que contém `formulas_excel.py`, crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative no Windows, pelo PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Ou no Linux/macOS:

```bash
source .venv/bin/activate
```

### 2. Instale as dependências

```bash
python -m pip install pandas numpy python-dateutil
```

A versão foi validada com **Pandas 2.2.3**, **NumPy 2.3.5** e **python-dateutil 2.9.0.post0**. Essas são as versões verificadas, não uma declaração de versões mínimas.

### 3. Explore pelo terminal

```bash
# Executar exemplos fictícios
python formulas_excel.py --demo

# Listar as funções disponíveis
python formulas_excel.py --listar

# Executar os testes de regressão
python formulas_excel.py --test

# Consultar a ajuda
python formulas_excel.py --help

# Exibir a versão
python formulas_excel.py --version
```

Executar o arquivo sem argumentos exibe a ajuda. As opções `--demo`, `--listar` e `--test` são utilizadas separadamente.

### 4. Importe em outro script ou notebook

Mantenha `formulas_excel.py` na mesma pasta do script ou em um diretório disponível no caminho de importação do Python:

```python
import pandas as pd
from formulas_excel import PROCV, SOMASES, MARGEM

vendas = pd.DataFrame({
    "Produto": ["Peça A", "Peça B", "Peça A"],
    "Regiao": ["Sul", "Norte", "Sul"],
    "Receita": [100, 250, 150],
    "Custo": [60, 180, 90],
})

receita_peca_b = PROCV("Peça B", vendas, 3)
receita_sul = SOMASES(vendas, "Receita", "Regiao", "Sul")
vendas["Margem"] = MARGEM(vendas["Receita"], vendas["Custo"])

print(receita_peca_b)                        # 250
print(receita_sul)                          # 250
print(vendas["Margem"].round(2).tolist())    # [0.4, 0.28, 0.4]
```

## 💻 Exemplos de Uso

### Busca independente dos índices do Pandas

```python
import pandas as pd
from formulas_excel import PROCX, CORRESP

codigos = pd.Series([101, 102, 103], index=[10, 20, 30])
nomes = pd.Series(["Filtro", "Óleo", "Vela"], index=["a", "b", "c"])

print(PROCX(102, codigos, nomes))          # Óleo
print(CORRESP(102, codigos))              # 1 — posição em base zero
print(CORRESP(102, codigos, base=1))      # 2 — posição em base um
print(PROCX(999, codigos, nomes, "Não encontrado"))
```

O relacionamento ocorre pela ordem dos elementos, mesmo quando os rótulos dos índices são diferentes.

### Agregação com múltiplos critérios

```python
from formulas_excel import SOMASES, CONTSES, CONTSE

valores = [100, 200, 300, 400]
regioes = ["Sul", "Norte", "Sul", "Sul"]

print(SOMASES(valores, regioes, "Sul", valores, ">=250"))  # 700
print(CONTSES(valores, regioes, "Sul", valores, ">=250"))  # 2
print(CONTSE(["Ana", "André", "Bia"], "An*"))             # 2
```

Em `CONTSES`, o primeiro argumento define o tamanho da base; os critérios vêm nos pares seguintes. Em `SOMASE`, a ordem é **intervalo de soma, intervalo de critério, critério**. Essas assinaturas preservam o script original e diferem das fórmulas digitadas no Excel.

### Datas e calendário de trabalho

```python
from datetime import date
import pandas as pd
from formulas_excel import SOMASES, FIMMES, DIATRABALHOTOTAL, DIATRABALHO

movimentos = pd.DataFrame({
    "Data": ["01/02/2024", "15/02/2024", "01/03/2024"],
    "Valor": [100, 200, 300],
})

print(SOMASES(
    movimentos, "Valor",
    "Data", (">=", date(2024, 2, 1)),
    "Data", ("<=", date(2024, 2, 29)),
))  # 300

print(FIMMES("10/02/2024"))  # 2024-02-29
print(DIATRABALHOTOTAL(
    "01/01/2024", "31/01/2024", feriados=["01/01/2024"]
))  # 22
print(DIATRABALHO("05/01/2024", 1))  # 2024-01-08
```

Os feriados precisam ser informados: o módulo não consulta calendários nacionais ou municipais automaticamente.

### Conversão, arredondamento e tratamento de erros

```python
from formulas_excel import VALOR, ARRED, SEERRO, SOMARPRODUTO

print(VALOR("R$ 1.234,56"))                 # 1234.56
print(VALOR("12,5%"))                      # 0.125
print(ARRED(2.675, 2))                     # 2.68
print(ARRED(-2.5))                         # -3.0
print(SEERRO(lambda: 1 / 0, 0))            # 0
print(SOMARPRODUTO([10, 20], [2, 3]))       # 80.0
```

Para capturar um erro de execução com `SEERRO`, passe uma função, como `lambda: 1 / 0`. Em `SEERRO(1 / 0, 0)`, a divisão falharia antes de a função receber o argumento.

## 📂 Organização e Catálogo de Funções

O módulo principal contém os exemplos e os testes; não exige arquivos auxiliares para esses recursos.

| Arquivo | Conteúdo |
| --- | --- |
| `formulas_excel.py` | Funções, documentação interna, demonstração e testes. |
| `README.md` | Apresentação, instalação, exemplos e convenções de uso. |

| Grupo | Funções públicas |
| --- | --- |
| Busca e relacionamento — 6 | `PROCV`, `PROCX`, `CORRESP`, `INDICE`, `INDICE_CORRESP`, `MERGE` |
| Agregações — 14 | `SOMASE`, `SOMASES`, `CONTSE`, `CONTSES`, `MEDIASE`, `MEDIASES`, `MAXIMOSE`, `MINIMOSE`, `MAXIMOSES`, `MINIMOSES`, `SOMA`, `MEDIA`, `SOMARPRODUTO`, `CONT_VALORES` |
| Datas — 14 | `HOJE`, `AGORA`, `ANO`, `MES`, `DIA`, `DATA`, `DATAM`, `FIMMES`, `FIMMES_DESLOCADO`, `DIATRABALHOTOTAL`, `DIATRABALHO`, `DIAS`, `DATADIF`, `INICIO_MES_ATE_HOJE_MENOS1` |
| Indicadores — 8 | `DIVIDIR`, `MARGEM`, `CRESCIMENTO`, `VARIACAO_M1`, `VARIACAO_Y1`, `TICKET_MEDIO`, `PARTICIPACAO`, `SHARE` |
| Complementos — 10 | `SE`, `SEERRO`, `VALOR`, `ARRED`, `ARRUMAR`, `ESQUERDA`, `DIREITA`, `EXT_TEXTO`, `UNICOS`, `FILTRO` |

Para consultar a assinatura e os parâmetros de uma função:

```python
from formulas_excel import PROCX

help(PROCX)
```

## 📐 Stack Utilizada

- **Python:** organização do módulo, validações e interface de linha de comando.
- **Pandas:** Series, DataFrames, máscaras, agregações e junções.
- **NumPy:** operações numéricas vetorizadas e calendários de dias úteis.
- **python-dateutil:** deslocamentos e diferenças de calendário com `relativedelta`.
- **Decimal:** arredondamento com `ROUND_HALF_UP`.
- **datetime, calendar, re e operator:** datas, expressões regulares e comparações.
- **argparse e unittest:** comandos de execução e testes de regressão.

## 🧪 Testes de Regressão

A suíte incorporada contém **16 testes**, aprovados no ambiente de validação da versão 2.0.0. Os cenários incluem:

- Índices diferentes ou duplicados nas buscas e agregações.
- Buscas aproximadas, curingas e ausência de correspondências.
- Critérios numéricos, textuais, de datas e de valores vazios.
- Validação de tamanhos e limites de posições.
- Anos bissextos, finais de mês, dias úteis e intervalos invertidos.
- Indicadores escalares e vetorizados, divisões por zero e valores ausentes.
- Variações sem preenchimento de lacunas.
- Validação de cardinalidade em junções.
- Conversão numérica, arredondamento, texto, filtros e tratamento de erros.

Execute `python formulas_excel.py --test` para verificar o comportamento no seu ambiente. A aprovação da suíte cobre os cenários implementados; não representa equivalência integral com todas as fórmulas e casos especiais do Excel.

## 📌 Escopo da Versão Atual

- O projeto é um módulo de funções e uma interface de terminal. Não possui interface gráfica nem leitura/exportação de planilhas incorporada.
- Os **32 nomes públicos originais foram mantidos**, com expansão para **52 funções**. As correções introduzem mudanças de comportamento documentadas no início do código.
- `CORRESP` usa base zero por padrão; `INDICE` usa base um e agora seleciona a primeira coluna quando ela é omitida. Posições zero ou negativas em `INDICE` são rejeitadas.
- As datas textuais aceitam os formatos ISO e brasileiro. Números seriais do Excel não são convertidos implicitamente; `DATA` exige uma data válida, sem normalizar meses ou dias fora do calendário.
- `DATADIF` possui convenções próprias e documentadas para `MD` e `YD`, especialmente em finais de mês e anos bissextos. Não pretende reproduzir todas as particularidades do Excel.
- `VARIACAO_M1` e `VARIACAO_Y1` trabalham por posição: os dados precisam estar ordenados e ter periodicidade regular. Meses ausentes não são detectados automaticamente.
- Na máscara `semana_util`, os sete caracteres representam segunda a domingo: `1` indica dia útil. O padrão é `1111100`; essa convenção não é a máscara de fins de semana do Excel.
- `MERGE` segue o Pandas: chaves nulas podem se relacionar e chaves duplicadas podem multiplicar linhas. Use `validar` quando a relação esperada precisar ser garantida.
- `HOJE` e `AGORA` usam o horário local do computador. `AGORA` retorna um objeto sem informação de fuso horário.
- `VALOR` utiliza separadores explícitos; não detecta a localidade automaticamente.
- `SE` recebe ramos já calculados. Para execução condicional preguiçosa, utilize `if/else` do Python.

## 📄 Licença

O código fornecido não declara uma licença. A licença de distribuição deverá ser definida pelo responsável pelo projeto e incluída no repositório em um arquivo `LICENSE`.
