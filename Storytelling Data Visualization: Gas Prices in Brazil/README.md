# Introdução

Neste projeto, será realizado a implementação de um programa que cria uma imagem a partir de uma base de dados comparando o preço da **gasolina comum** no estado do Rio Grande do Norte entre os anos de 2004 a 2021, destacando os governos de cada período.

# Dataset

A criação da figura foi feita com base no dataset disponibilizado por [Matheus Eduardo Freitag](https://www.kaggle.com/datasets/matheusfreitag/gas-prices-in-brazil?resource=download). Esse dataset possui dezoito colunas com informações que incluem data, preço médio, região e estado.


# Principios de código limpo

O código foi desenvolvido levando em consideração boas práticas de programação. 

## Pylint

Obteve-se uma nota de 10.0/10.0 no *pylinu*, conforme mostrado na figura abaixo.

![pylint result](./images/pylint_result.png)


* Para verificar a nota do código seguindo o *pylint*, basta digitar o seguinte comando:

```
pylint gas_prices_brazil.py
```

# Execução


* Para executar o código e criar a imagem, basta executar o comando abaixo:

```
python3 gas_prices_brazil.py
```

# Resultado

Ao executar o programa, obtem-se a figura mostrado abaixo, que mostra a média de preço da gasolina comum entre os anos de 2014 a 2021 destacando o mandato dos respectivos presidentes.


![gasolina](./images/gas_prices_brazil.png)

Considerou-se uma média móvel igual a quatro para a criação da imagem. Tal valor foi escolhido para que cada ponto da figura representasse uma média mensal, visto que cada valor da base de dados representa a média semanal.

Além disso, após aplicar o valor médio do preço para cada presidente, obteve-se os seguintes resultados:

* Lula: R$ 2.52 
* Dilma: R$ 3.07
* Temer: R$ 4.13
* Bolsonaro: R$ 4.60

*OBS: Valores computados considerados foram entre Maio de 2004 e Abril de 2021 no estado do Rio Grande do Norte.*


