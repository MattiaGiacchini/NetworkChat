# *Programmazione di Reti* - *Giacchini Mattia*
La mia interpretazione della traccia consiste nella realizzazione di una pseudo-chat in cui ciascun client può mandare messaggi ai vari client connessi al server.

I file contenuti in questo repository sono basati sui documenti forniti dal prof. Piroddi, apportando le opportune modifiche al fine di rispettare la consegna della traccia n. 1.

# Lancio del programma:

 1. Lanciare lo script `server.py`
 2. Lanciare uno o entrambe i `router_*.py`
 3. Infine lanciare, a piacere, i `client_**.py`. Non è necessario che questi vengano lanciati tutti quanti poiché il programma si adatta ai client presenti in rete.
 
# Note:
Il programma permette di inviare messaggi tra tutti i client presenti in rete, nel caso in cui uno di questi non fosse online, verrà recapitata tale informazione al mittente.

Mandando un semplice messaggio a uno qualsiasi dei client, anche essi stessi, con scritto "***quit***" interromperà la connessione del client mittente. Altre interruzioni forzate dello script causeranno una serie di errori a cascata anche negli altri file in esecuzione del progetto.

Il servere mantiene un registro all'interno di un file di testo chiamato "***connecionLog.txt***", dentro il quale vengono inserite connessioni e disconnessioni, di ciascun client con i relativi orari.

# Strategie e implementazioni:

