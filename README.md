
# *Programmazione di Reti* - *Giacchini Mattia*
La mia interpretazione della traccia consiste nella realizzazione di una pseudo-chat in cui ciascun client può mandare messaggi ai vari client connessi al server.

I file contenuti in questo repository prendono ispirazione dai documenti forniti dal prof. Piroddi, apportando diverse e opportune modifiche al fine di rispettare la consegna della **traccia n. 1**.

# Lancio del programma:

 1. Lanciare lo script `server.py`
 2. Lanciare uno o entrambe i `router_*.py`
 3. Infine lanciare, a piacere, i `client_**.py`. Non è necessario che questi vengano lanciati tutti quanti, nè tantomeno in ordine, poiché il programma si adatta ai client presenti in rete. Nonostante ciò i client_a* si connettono solamente al router_a, cosa equivalente per i client_b*.
 
# Note:
Il programma permette di inviare messaggi tra tutti i client presenti in rete, nel caso in cui uno di questi non fosse online, verrà recapitata tale informazione al mittente.
Se si scegliesse di attivare uno solo dei router non sarà possibile sapere se i client connessi all'altro router sono online o meno.

Mandando un semplice messaggio a uno qualsiasi dei client, anche essi stessi, con scritto "***quit***" interromperà la connessione del client mittente. Altre interruzioni forzate dello script causeranno una serie di errori a cascata anche negli altri file in esecuzione del progetto.

Il server mantiene un registro all'interno di un file di testo chiamato "***connecionLog.txt***", dentro il quale vengono inserite connessioni e disconnessioni, di ciascun client con i relativi orari.

# Strategie e implementazioni:
Ogni nodo all'interno della rete è abbinato ad un indirizzo IP (in questo caso statico e impostato a priori) e ad un indirizzo MAC. 
Ho voluto anche collegare ciascun nodo ad una porta specifica per le comunicazioni.

## Server
Per il server ho pensato di utilizzare due thread, uno per ciascun router, per gestire ricezione e invio di messaggi ai destinatari.
Rimane inoltre attivo costantemente un ciclo infinito che permette di collegare ulteriori router anche in corso d'opera.

## Router
Per i due router, creati in file separati ma sulla medesima struttura, ho definito alcune funzioni lanciate tramite thread appositi per la ricezione e invio di messaggi su ciascun client. Inoltre un thread apposito è utilizzato per gestire eventuali messaggi in arrivo dal server. Questi ultimi sarebbero messaggi in arrivo da client esterni al router in analisi.
Ciascun thread, nel momento in cui dovrà inoltrare un messaggio, si avvarrà di una funzione comune apposita, che si occupa di smistare i messaggi in uscita.

Ho preferito gestire il fatto che un messaggio in partenza da un nodo interno al router, destinato ad un altro (o allo stesso) nodo sempre interno alla sotto-rete del router, non verrà recapitato al server, ma verrà inoltrato direttamente al destinatario.

## Client
Per ciascun client ho creato un file separato, in modo tale che questo contenesse le informazioni relative al suo nodo (IP, MAC e porta).

Come anche per le altre componenti della rete, anche per il client ho gestito le varie operazioni tramite thread dedicati.
In particolare in ogni client sono presenti due thread: uno per l'invio di messaggi, l'altro per la ricezione degli stessi.

