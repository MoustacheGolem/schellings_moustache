--> Esse projeto foi feito com base no modelo exemplo Schellings. 

### Apresentação do novo modelo, em sua relação ao modelo original: ###########################################

O modelo original explora um campo com dois tipos de agente, onde cada agente fica na mesma posição, se esta feliz, 
ou seja com um número suficiente de agentes similares estiverem próximos. 

O modelo novo adiciona novo funcionamento:
Distaste: Que denota o quanto um agente diferente proximo affeta a felicidade de um agente.


### Descrição da hipótese causal que você deseja comprovar: ###################################################

No modelo original agentes acham com facilidade posições felizes, 
e nunca mudam de posição depois disso, resultando em configurações finais onde os agentes,
principalmente os da minoria, ficam em vários clusters separados um do outro. 
Teorizo que permitir que os agentes mudem mesmo felizes e que evitem posições próximas a agentes diferentes 
fara com que todos os agentes incluindo a minoria se juntem em menos clusters maiores. 

### Justificativa para as mudanças que você fez, em relação ao código original: ###############################

Duas Variáveis, adversity e distaste, para uso dessas mudanças foram feitas mudanças no arquivo movel.py

"adversity" para permitir que agentes mudem de posição mesmo estando felizes e 
"distate" que causa agentes a desgostarem de agentes diferentes.

Para adicionar as novas variáveis como parâmetros modificáveis foram feitas mudanças no arquivo server.py

 
### Orientação sobre como usar o simulador: ###################################################################

Exatamente como o modelo exemplo original.
 - Rodar run.py como um arquivo python executavel por exemplo.
 

### Descrição das variáveis armazenadas no arquivo CSV: #######################################################
 

density : Densidade de agentes no campo.

minority_pc: porcentagem de agentes com tipo menoria .

homophily: quantos agentes similares proximos são necessários para um agente ficar feliz, se distaste for True agentes diferentes próximos subtrairão de homophily

run: Núero do teste.

minority_clusters: Quantidade de clusters formados por agentes do tipo minoria (agentes azul).

happy: Quantidade de agentes felizes.

neighborhood_mean: Media de visinhos do mesmo tipo que cada agente tem.

height: Altura do campo.

width: Largura do campo.

distaste: Se os agentes desgostaram de ter agentes diferentes próximos ou não.

Parametros fixos:

"height"
"width"
"distaste" 

Parametros variaveis:

"density" 
"minority_pc"
"homophily"
"adversity"

Valores de modelo reportados:
"happy" 			happy tecnicamente é valor de agente, mas a logica do modelo o calcula como valor de modelo.
"Minority_clusters" 
"neighborhood_mean" 



 