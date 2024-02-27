This program implements AI to parse sentences and extract noun phrases.
The noun phrases are extracted to get understanding of the whole sentence. 

The parsing is done by using contex-free grammar. The goal is to apply set of rules
repeatedly to generate patterns of strings.

The contex-free grammar needs the following:
Terminal symbols, for example N for nouns, V for verbs.
Nonterminal symbols, for example NP for noun phrase. 
Production rules to replace nonterminal symbols, for example S -> NP VP.
Start symbol, in this program S (sentence).

Example:

For sentence "Holmes sat", the parsing tree looks like the following:

                     S     
                _____|_____ 
                NP        VP
                |         |  
                N         V 
                |         |  
               holmes    sat

