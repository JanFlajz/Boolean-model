Toto je zaloha reseni moji semestralni prace v semestru B212 z predmetu Vyhledavani na Webu a Multimedialnich databazich na FIT CVUT.
Program byl pri vytvareni verzovan na fakultnim Gitlabu https://gitlab.fit.cvut.cz/ 

Jedna se o skupinovy projekt pro predmet vyhledavani na webu a v multimedialnich databazich. Ukolem bylo vytvorit
program pro vyhledavani v textech pisni s vyuzitim rozsireneho boolskeho modelu https://en.wikipedia.org/wiki/Extended_Boolean_model .

Aplikace je implementovana v jazyce python s vyuzitim frameworku django pro vytvareni webovych aplikaci. 
A vyuziva staticko kolekci dokumentu - textu pisni ulozenych v 1 textovem souboru. 

Program funguje nasledovne:
Nejdrive se samostatne stahnou texty pisni z externi webove stranky. Potom se tyto texty projedou scriptem pro upravu slov a odstraneni
stop-slov (slov, ktera se vyskytuji casto) pro dany jazyk.

Kdyz mame takto predzpracovana data, muzeme spustit uz vyslednou aplikaci, ktera si tato data predzpracuje do podoby potrebne pro boolsky model a
spusti se uzivatelske rozhrani. Uzivatel pak muze vyhledavat jednotliva slova, nebo jejich spojeni pomoci logickych spojek.   



