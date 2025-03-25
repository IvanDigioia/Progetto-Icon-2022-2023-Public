from owlready2 import *

'''
Modulo di implementazione dell'ontologia interrogabile
'''


def main_ontology():
    print("\nBENVENUTO NELLA BOOK-ONTOLOGY\n")
    while True:
        print(
            "Seleziona cosa vorresti esplorare:\n\n1) Visualizzazione Classi\n2) Visualizzazione proprietà d'oggetto\n"
            "3) Visualizzazione proprietà dei dati\n4) Visualizzazione query d'esempio\n5) Exit Ontologia\n")

        risposta_menu = input("Inserisci qui la tua scelta:\t")

        ontology = get_ontology('BookOntology.owx').load()

        if risposta_menu == '1':
            print("\nClassi presenti nell'ontologia:\n")
            print(list(ontology.classes()))

            while True:
                print(
                    "\nVorresti esplorare meglio qualche classe in particolare?\n\n1) Book\n2) Author\n3) Genre\n"
                    "4) Consumer\n5) Publisher\n6) Shop\n7) Indietro")
                risposta_class = input("Inserisci qui la tua scelta:\t")

                if risposta_class == '1':
                    print("\nLista di Libri presenti:\n")
                    books = ontology.search(is_a=ontology.Book)
                    print(books)

                elif risposta_class == '2':
                    print("\nLista degli Autori presenti:\n")
                    authors = ontology.search(is_a=ontology.Author)
                    print(authors)

                elif risposta_class == '3':
                    print("\nLista delle Categorie presenti:\n")
                    genres = ontology.search(is_a=ontology.Genre)
                    print(genres)

                elif risposta_class == '4':
                    print("\nLista dei clienti presenti:\n")
                    costumers = ontology.search(is_a=ontology.Costumer)
                    print(costumers)

                elif risposta_class == '5':
                    print("\nLista delle Case Pubblicatrici presenti:\n")
                    publishers = ontology.search(is_a=ontology.Publisher)
                    print(publishers)

                elif risposta_class == '6':
                    print("\nLista dei Negozi presenti:\n")
                    shops = ontology.search(is_a=ontology.Shop)
                    print(shops)

                elif risposta_class == '7':
                    break

                else:
                    print("\nInserisci il numero correttamente tra quelli presentati")

        elif risposta_menu == '2':
            print("\nProprietà d'oggetto presenti nell'ontologia:\n")
            print(list(ontology.object_properties()), "\n")

        elif risposta_menu == '3':
            print("\nProprietà dei dati presenti nell'ontologia:\n")
            print(list(ontology.data_properties()), "\n")

        elif risposta_menu == '4':
            print("\nQuery d'esempio:")
            print("\n-Lista di libri che presentano la categoria 'Romance':\n")
            books = ontology.search(is_a=ontology.Book, has_genre=ontology.search(is_a=ontology.Romance))
            print(books, "\n")
            print("\n-Lista di libri che presentano la scrittrice 'Karen Kingsbury':\n")
            books = ontology.search(is_a=ontology.Book, is_written_by=ontology.search(is_a=ontology.Karen_Kingsbury))
            print(books, "\n")
            print("\n-Lista di libri che presentano la pubblicazione da 'Tor Books':\n")
            books = ontology.search(is_a=ontology.Book, is_published_by=ontology.search(is_a=ontology.Tor_Books))
            print(books, "\n")

        elif risposta_menu == '5':
            break
