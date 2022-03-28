# Rapport de projet

## Groupe 3
* 28609129 Mohamed Djamila

## Description des choix importants d'implémentation

1 fichier main par semaine car plus facile pour comprendre l'acheminement du code.

Les stratégies ont été séparées en 2 types :

- stratégies de base (aléatoire, équitable, deux premiers) : elles sont appelées dans une fonction repartir_strategies qui sert à répartir les stratégies en fonction de ce que les militants ont choisi.

- stratégies dépendantes des autres (tétu, stochastique expert, meilleure réponse, fictitious play) : ces stratégies utilisent les 3 stratégies de base pour calculer une nouvelle stratégie ou utiliser une stratégie de base déjà implémentée.

_Stratégies:_
aléatoire: fait
tétu: fait
stochastique expert: pas fait
meilleure réponse: pas fini
fictitious play: pas fait

_Autres stratégies:_
équitable: fait
deux premiers: fait

## Description des résultats

Stratégies aléatoire et tétu(équitable) ensemble:
  - lorsqu'on lance le programme sur plusieurs jours et ceci plusieurs fois, on remarque la stratégie équitable a tendance à remporter le plus de voix et donc à gagner le plus parties.
