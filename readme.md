This projected was made to perform a naive opinion identification in texts about cellphones and cameras written in Portuguese. It is intended to be used in semi-automatic opinion labeling. 

# Methodology

Opinions are identified by their polarity and aspect. Aspects are found based on a list of words that are used as clues (`opinion_mining/aspects.json`). Polarities are guessed based on the rating that the review writer gave to the product.
 
# To execute

Run `mine_opinions.py` with Python 3.6.

# Input set

The input set must be placed in the directory `input`. Each file in that directory contains opinative text about a single product. 

The format of the files is: lines starting with `>` are meta information (any relevant information about the product). Each opinative review starts with the date it was published, followed by a line containing the recommendation (the letter 'Y' if the reviewer recommends the product and the letter 'N' if not), the upvotes and downvotes of the comment (given to the review by readers). Below is a template; things in brackets are variables.

```
> [meta information]: [value]
> [meta information]: [value]

@ [date]
* [recommendation]     
[sentence ID]   ::  [SENTENCE 1 OF REVIEW 1]

@ [date]
* [recommendation]    
[sentence ID]   ::  [SENTENCE 1 OF REVIEW 2]
[sentence ID]   ::  [SENTENCE 2 OF REVIEW 2]
```

An example of an input file is: 

```
> ID:  31
> Type:  Celular
> Product:  Smartphone Motorola Moto G 5 Plus XT1683
> Average rating:  9/10
> Number of reviews:  233
> Collection date:  2018-11-13
> Source:  https://www.buscape.com.br/avaliacoes/smartphone-motorola-moto-g-5-plus-xt1683

@ 2017/05/29
* Y
020.083 ::  Exelente produto.
020.084 ::  Produto de alta qualidade, com espaço interno de bom tamanho.
020.085 ::  Para jogos não se discute roda qualquer jogo e com uma tela de ótimo tamanho.


@ 2017/07/06
* N
019.078 ::  Produto Ruim.
019.079 ::  Recebi o produto mas o mesmo não carregava.

``` 


# Output files

For each input file, an output file with the same name will be generated in the directory `output`. 

Each output file starts with a copy of the meta information found on the input file. It adds to the meta information the date when the file was generated. Then, it shows a table with quantitative information about opinions found. After the table, all the sentences from the input set appear with their aspects and polarities identified. Each sentence has the format: 

```
[sentence ID]  [polarity][[aspects]]     ::  [SENTENCE]
```
For example:
```
> ID:  31
> Type:  Celular
> Product:  Smartphone Motorola Moto G 5 Plus XT1683
> Average rating:  9/10
> Number of reviews:  233
> Collection date:  2018-11-13
> Processing date:  2019-09-13
> Source:  https//www.buscape.com.br/avaliacoes/smartphone-motorola-moto-g-5-plus-xt1683

#_aspects____________positive__negative___neutral_____total
# ARMAZENAMENTO            15         3                  18
# ÁUDIO _  _  _  _  _  _  _ 1 _  _  _  _  _  _  _  _  _   1
# BATERIA                  25         4                  29
# CÂMERA _  _  _  _  _  _  32 _  _  _ 2 _  _  _  _  _  _ 34
# DESEMPENHO               30         3                  33
# DESIGN _  _  _  _  _  _  22 _  _  _ 2 _  _  _  _  _  _ 24
# EMPRESA                  10         2                  12
# FUNCIONALIDADE _  _  _  _ 5 _  _  _  _  _  _  _  _  _   5
# PESO                      4                             4
# PREÇO _  _  _  _  _  _   70 _  _  _ 3 _  _  _  _  _  _ 73
# PRODUTO                 367         7                 374
# RÁDIO _  _  _  _  _  _  _ 1 _  _  _  _  _  _  _  _  _   1
# RESISTÊNCIA               5                             5
# SO _  _  _  _  _  _  _   11 _  _  _ 1 _  _  _  _  _  _ 12
# TAMANHO                   5                             5
# TELA _  _  _  _  _  _  _ 12 _  _  _ 1 _  _  _  _  _  _ 13
# TELEVISÃO                 7         1                   8
# USABILIDADE _  _  _  _   18 _  _  _ 1 _  _  _  _  _  _ 19
# _TOTAL__________________640________30_________________670


069.167  +[ARMAZENAMENTO]     ::  Memória.

178.457  +[ARMAZENAMENTO]     ::  Pena não vender no Brasil a versão americana com 4GB de RAM e 64GB de memória interna (o meu é esse)

048.116  +[BATERIA]           ::  Gostei muito a bateria dura bastante,!

174.440  -[ARMAZENAMENTO SO]  ::  Para mim, a memória interna deveria ser aumentada, pois o Android quase ocupa toda ela.

098.243  -[BATERIA DESIGN]    ::  Só a duração da bateria e o design que poderiam ser melhores.
```

# Developers 

Raphael Rocha da Silva _(May 2018 -- September 2019)_