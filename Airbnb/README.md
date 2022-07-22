# Introdução

Este projeto consiste em realizar uma análise dos preços do Airbnb levando em consideração a cidade do Rio de Janeiro. A ideia final do projeto é, a partir de um conjunto de informações básicas da residência, poder estimar o preço médio por dia dessa residência. Isto é, resolver um problema de regressão.

Inicialmente, neste projeto, iremos realizar o pré-processamento dos dados, salvando diferentes versões do dataset no *wandb*, e realizando uma análise estatística para definir quais seriam as principais variáveis que podem ser utilizadas na solução do problema.

Em seguida, o dataset será separado em treinamento e teste, para então treinar um novo modelo e realizar o *deploy* do mesmo online.

Os passos a serem tomados para a solução desse problema e descritos nesse arquivo foram baseados no curso de [MLOPS de Ivanovitch](https://github.com/ivanovitchm/mlops). 

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

Uma vez que o ambiente no conda já esteja instalado e ativado na sua máquina, será realizado uma análise dos dados com o objetivo de descobrir padrões, perceber anomalias, tratar dados faltantes e estabelecer as variáveis mais relevantes para solucionar o problema. Além disso, a medida que novas versões do dataset forem criadas, as mesmas serão salvas no *wandb*. 

Inicialmente, é necessário executar o *mlflow* levando em consideração os arquivos nesta pasta. Isto é feito através do seguinte comando:

```
mlflow run .
```

Ao executar este comando, os comandos dentro do arquivo *MLproject* serão executados. Neste momento, temos apenas a instrução para executar o *Jupyter*, assim, uma nova aba no seu navegador será aberta mostrando todos os arquivos do projeto. O EDA foi desenvolvido utilizando o notebook *EDA.ipynb*. Toda a discussão a seguir leva em consideração este arquivo.

Inicialmente, foi necessário instalar algumas outras bibliotecas adicionais utilizando o pip, sendo elas o *seaborn*, *sklearn*, *pandas_profiling* e *ipywidgets*. Após a instalação deles, importamos todas as bibliotecas que serão utilizadas neste programa.

O próximo passo envolve realizar a leitura do dataset *listings.csv*, que está incluído na pasta do projeto, utilizando o *Pandas*. Este dataset está disponibilizado em [Ivanovitch Silva, Google Drive](https://drive.google.com/file/d/16zF4MHEP_bBxAEWpQgVocPupTjRRAgfP/view). Em seguida, este dataset completo é salvo no *wandb* como um artefato, conforme mostra a figura abaixo.

![Figura 1: Carregando o dataset original no wandb](./figures/figure1.png)

Dessa forma, já é possível carregar o dataset completo em alguma outra seção e por outra pessoa utilizando o *wandb*. Esse processo pode demorar dependendo do tamanho do dataset e da velocidade da internet.






