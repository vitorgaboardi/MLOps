# Introdução

Este projeto consiste em realizar uma análise dos preços do Airbnb levando em consideração a cidade do Rio de Janeiro. A ideia final do projeto é, a partir de um conjunto de informações básicas da residência, poder estimar o preço médio por dia dessa residência. Isto é, resolver um problema de regressão.

Inicialmente, neste projeto, iremos realizar o pré-processamento dos dados, salvando diferentes versões do dataset no *wandb*, e realizando uma análise estatística para definir quais seriam as principais variáveis que podem ser utilizadas na solução do problema.

Em seguida, o dataset será separado em treinamento e teste, para então treinar um novo modelo e realizar o *deploy* do mesmo online.

# Instalação de dependências

Antes de realizar a execução dos scripts em Python, será necessário realizar a instalação de algumas dependências. 

Para facilitar este processo, iremos inicialmente criar um Ambiente Virtual (*Virtual Environment*) que será utilizado para executar todos os projetos envolvendo MLOps.

A vantagem da utilização desses ambientes virtuais é a possibilidade de instalar versões específicas das bibliotecas apenas dentro deste ambiente, sem alterar as configurações do computador como um todo. Assim, é possível criar ambientes específicos para cada aplicação desejada com diferentes versões.

Esse ambiente será criado através do [Anaconda](https://www.anaconda.com/products/distribution). Para instalar essa distribuição, deve-se seguir os passos fornecidos em seu website. Uma vez que o Anaconda estiver instalado, siga os seguintes passos:

1. Criar um ambiente virtual chamado *mlops* com as dependências descritas dentro do arquivo *environment.yml*:

```
conda env create --file environment.yml
```

Autorize a criação do ambiente, quando requisitado.

2. Ativar o ambiente:

```
conda activate mlops
```

# EDA (Exploratory Data Analysis)

Uma vez que o ambiente no conda já esteja instalado na sua máquina, será realizado uma análise dos dados com o objetivo de descobrir padrões, perceber anomalias, tratar dados faltantes e estabelecer as variáveis mais relevantes para solucionar o problema. Além disso, a medida que novas versões do dataset forem criadas, as mesmas serão salvas no *wandb*.

Os passos a serem tomados nesta seção foram baseados no curso de [MLOPS de Ivanovitch - Week 8](https://github.com/ivanovitchm/mlops). 



