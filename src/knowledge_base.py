import pandas as pd
import pytholog as pl

'''
Modulo per la creazione e popolazione della knowledge base con fatti e regole riguardanti le relazioni fra tutte le 
entità
'''
book_kb = pl.KnowledgeBase("Books")
book_df = pd.read_csv('final_dataset.csv')
book_df.dropna(inplace=True)


def average_of_ratings():
    """
    Funzione per restituire il rating medio e il numero di recensioni
    """
    rating_mean = book_df['average_rating'].mean()
    average_no_ratings = book_df['rating_count'].mean()

    return rating_mean, average_no_ratings


def output_string(s):
    """
    Funzione per ritrasformare le stringhe date in input alla funzione input_string
    """
    sx_offset = 10
    dx_offset = -2
    s = s.replace("|", ",")
    s = s.replace("+", " ")
    new_s = s[sx_offset:dx_offset]
    return new_s.title()


def input_string(s):
    """
    Funzione per trasformare le stringhe date in input
    """
    if isinstance(s, float) or isinstance(s, int):
        s = str(s)
    s = s.lower()
    s = s.replace(" ", "+")
    s = s.replace(",", "|")

    return s


'''
FATTI e REGOLE per popolare la knowledge base
'''


def populate_kb_written_by(kb, df, check_comma):
    """
    Metodo per popolare gli attributi titolo e autore della knowledge base
    """
    df1 = df[['title', 'author']]
    if check_comma:
        for i in range(df1.shape[0]):
            kb([f"author({input_string(df1.title[i].lower())},{input_string(df1.author[i])})"])
    else:
        for i in range(df1.shape[0]):
            kb([f"author({df1.title[i].lower()},{input_string(df1.author[i])})"])

    kb(["is_written_by(X,Y) :- author(Y,X)"])


def populate_kb_reevaluation(kb, df, check_comma):
    """
    Metodo per popolare gli attributi titolo e la valutazione calcolata in base al rating medio e al numero di ratings della knowledge base
    """
    df1 = df[['title', 're_evaluation']]
    if check_comma:
        for i in range(df1.shape[0]):
            kb([f"eval({input_string(df1.title[i].lower())},{input_string(df1.re_evaluation[i])})"])
    else:
        for i in range(df1.shape[0]):
            kb([f"eval({df1.title[i].lower()},{input_string(df1.re_evaluation[i])})"])

    kb(["re_evaluation(X,Y) :- eval(Y,X)"])


def populate_kb_published_by(kb, df, check_comma):
    """
    Metodo per popolare gli attributi titolo e publisher della knowledge base
    """
    df1 = df[['title', 'publisher']]
    if check_comma:
        for i in range(df1.shape[0]):
            kb([f"publisher({input_string(df1.title[i].lower())},{input_string(df1.publisher[i])})"])
    else:
        for i in range(df1.shape[0]):
            kb([f"publisher({df1.title[i].lower()},{input_string(df1.publisher[i])})"])

    kb(["published_by(X,Y) :- publisher(Y,X)"])


def populate_kb_rating(kb, df, check_comma):
    """
    Metodo per popolare gli attributi titolo e rating della knowledge base
    """
    df1 = df[['title', 'average_rating']]
    if check_comma:
        for i in range(df1.shape[0]):
            kb([f"rating({input_string(df1.title[i].lower())},{input_string(df1.average_rating[i])})"])
    else:
        for i in range(df.shape[0]):
            kb([f"rating({df1.title[i].lower()},{input_string(df1.average_rating[i])})"])

    kb(["rated(X,Y) :- rating(Y,X)"])


def populate_kb_genre(kb, df, check_comma):
    """
    Metodo per popolare gli attributi titolo e genere della knowledge base
    """
    df1 = df[['title', 'genre']]
    if check_comma:
        for i in range(df1.shape[0]):
            kb([f"genre({input_string(df1.title[i].lower())},{input_string(df1.genre[i])})"])
    else:
        for i in range(df1.shape[0]):
            kb([f"genre({df1.title[i].lower()},{input_string(df1.genre[i])})"])

    kb(["is_genre(X,Y) :- genre(Y,X)"])


def populate_kb_publishing_year(kb, df, check_comma):
    """
    Metodo per popolare gli attributi titolo e l'anno di pubblicazione della knowledge base
    """
    df1 = df[['title', 'published_year']]
    if check_comma:
        for i in range(df1.shape[0]):
            kb([f"published({input_string(df1.title[i].lower())},{input_string(int(df1.published_year[i]))})"])
    else:
        for i in range(df1.shape[0]):
            kb([f"published({df1.title[i].lower()},{input_string(int(df1.published_year[i]))})"])

    kb(["is_published_in(X,Y) :- published(Y,X)"])


def populate_kb_number_of_pages(kb, df, check_comma):
    """
    Metodo per popolare gli attributi titolo e numero di pagine della knowledge base
    """
    df1 = df[['title', 'number_of_pages']]
    if check_comma:
        for i in range(df1.shape[0]):
            kb([f"pages({input_string(df1.title[i].lower())},{input_string(int(df1.number_of_pages[i]))})"])
    else:
        for i in range(df1.shape[0]):
            kb([f"pages({df1.title[i].lower()},{input_string(int(df1.number_of_pages[i]))})"])

    kb(["number_of_pages(X,Y) :- pages(Y,X)"])


def populate_kb_rating_counts(kb, df, check_comma):
    """
    Metodo per popolare gli attributi titolo e numero di valutazioni della knowledge base
    """
    df1 = df[['title', 'rating_count']]
    if check_comma:
        for i in range(df1.shape[0]):
            kb([f"no_of_ratings({input_string(df1.title[i].lower())},{input_string(int(df1.rating_count[i]))})"])
    else:
        for i in range(df1.shape[0]):
            kb([f"no_of_ratings({df1.title[i].lower()},{input_string(int(df1.rating_count[i]))})"])

    kb(["rating_count(X,Y) :- no_of_ratings(Y,X)"])


def populate_kb_rating_star(kb, df):
    """
    Metodo per popolare gli attributi titolo e il rating calcolato in stelle della knowledge base
    """
    df1 = df[['title', 'average_rating']]

    for i in range(df1.shape[0]):
        kb([f"rating({input_string(df1.title[i].lower())},{input_string(df1.average_rating[i])})"])

    kb(["rated(X,Y) :- rating(Y,X)"])


def populate_kb_all_written_by(kb, df):
    """
    Metodo per popolare gli attributi titolo e tutti gli autori della knowledge base
    """
    df1 = df[['title', 'author']]

    for i in range(df1.shape[0]):
        kb([f"author({input_string(df1.title[i].lower())},{input_string(df1.author[i])})"])

    kb(["is_written_by(X,Y) :- author(Y,X)"])


def populate_kb_best_genre(kb, df):
    """
    Metodo per popolare gli attributi titolo e genere della knowledge base
    """
    df1 = df[['title', 'genre']]

    for i in range(df1.shape[0]):
        kb([f"genre({input_string(df1.title[i].lower())},{input_string(df1.genre[i])})"])

    kb(["is_genre(X,Y) :- genre(Y,X)"])


def main_kb():
    print("\nKNOWLEDGE BASE\n")
    print("Benvenuto, qui puoi eseguire ricerche sui libri e sulle loro caratteristiche")
    while True:
        print("\nEcco le ricerche che puoi eseguire:")
        print("1) Ricerche sulle caratteristiche di un libro ")
        print("2) Confronti e ricerca di libri in base ad una caratteristica ")
        print("3) Rivalutazione di un libro in base al rating medio e al suo numero di recensioni ")
        print("4) Ritorna al main")
        choice1 = input("Inserisci il numero corrispondente alla tua scelta: ")
        # Controllo sull'input dell'utente per accettare solo valori numerci
        if choice1.isnumeric():
            c1 = int(choice1)
            if c1 == 1:
                check = False
                while not check:
                    book_name = input("Dammi il nome di un libro: ").lower()
                    # Controllo sul titolo del libro inserito dall'utente per vedere se contiene una virgola
                    virgola = "," in book_name
                    for i in range(book_df.shape[0]):
                        # Controllo per trovare il libro all'interno del dataset
                        if book_name == book_df.title[i].lower():
                            check = True
                    if not check:
                        print("Libro non trovato, inseriscine un altro\n")

                while True:
                    print("\nQueste sono le caratteristiche che puoi cercare: ")
                    print("1) Chi lo ha scritto ")
                    print("2) Chi lo ha pubblicato ")
                    print("3) Qual'è il suo rating medio ")
                    print("4) Quanti rating ha ricevuto ")
                    print("5) Di che genere è ")
                    print("6) In che anno è uscito ")
                    print("7) Quante pagine ha ")
                    print("Puoi anche: ")
                    print("8) Cambia libro ")
                    print("9) Cambia tipo di ricerca ")
                    choice2 = input("Selezionane una: ")
                    # Controllo sull'input dell'utente per accettare solo valori numerci
                    if choice2.isnumeric():
                        c2 = int(choice2)
                        if virgola:
                            # Se è presente una virgola nel titolo del libro bisogna convertire la stringa
                            book_final = input_string(book_name).lower()
                        else:
                            book_final = book_name

                        # Gestore delle opzioni di ricerca sulle caratteristiche
                        if c2 == 1:
                            populate_kb_written_by(book_kb, book_df, virgola)
                            result = book_kb.query(pl.Expr(f"is_written_by(What,{book_final})"))
                            print("\n", book_name.title(), "è stato scritto da:", output_string(str(result[0])))

                        elif c2 == 2:
                            populate_kb_published_by(book_kb, book_df, virgola)
                            result = book_kb.query(pl.Expr(f"published_by(What,{book_final})"))
                            print("\n", book_name.title(), "è stato rilasciato da:", output_string(str(result[0])))

                        elif c2 == 3:
                            populate_kb_rating(book_kb, book_df, virgola)
                            result = book_kb.query(pl.Expr(f"rated(What,{book_final})"))
                            print("\n", book_name.title(), "ha:", output_string(str(result[0])), "stelle")

                        elif c2 == 4:
                            populate_kb_rating_counts(book_kb, book_df, virgola)
                            result = book_kb.query(pl.Expr(f"rating_count(What,{book_final})"))
                            print("\n", book_name.title(), "ha:", output_string(str(result[0])), "rating")

                        elif c2 == 5:
                            populate_kb_genre(book_kb, book_df, virgola)
                            result = book_kb.query(pl.Expr(f"is_genre(What,{book_final})"))
                            print("\nI generi di", book_name.title(), "sono:", output_string(str(result[0])))

                        elif c2 == 6:
                            populate_kb_publishing_year(book_kb, book_df, virgola)
                            result = book_kb.query(pl.Expr(f"is_published_in(What,{book_final})"))
                            print("\nIl libro", book_name.title(), "è uscito nel:", output_string(str(result[0])))

                        elif c2 == 7:
                            populate_kb_number_of_pages(book_kb, book_df, virgola)
                            result = book_kb.query(pl.Expr(f"number_of_pages(What,{book_final})"))
                            print("\nIl libro", book_name.title(), "ha:", output_string(str(result[0])), "pagine")

                        elif c2 == 8:
                            check = False
                            while not check:
                                book_name = input("Dammi il nome di un libro: ").lower()
                                virgola = "," in book_name
                                for i in range(book_df.shape[0]):
                                    if book_name == book_df.title[i].lower():
                                        check = True
                                if not check:
                                    print("Libro non trovato, inseriscine un altro\n")
                        elif c2 == 9:
                            break

                        elif c2 < 1 or c2 > 9:
                            print("il valore inserito non è valido, inseriscine un'altro")

                    else:
                        print("il valore inserito non è un numero, inserisci un valore numerico")

            elif c1 == 2:
                print("\nQueste sono ricerche che puoi eseguire sulle caratteristiche:")
                while True:
                    print("\n1) Confronto di qualità tra 2 libri")
                    print("2) Ricerca libri con un determinato rating")
                    print("3) Ricerca tutti i libri pubblicati da un autore")
                    print("4) I migliori 10 libri di un genere specifico")
                    print("Puoi anche: ")
                    print("5) Cambia tipo di ricerca ")
                    choice3 = input("Selezionane una: ")
                    if choice3.isnumeric():
                        c3 = int(choice3)

                        # Gestore delle opzioni di ricerca baata su una caratteristica
                        if c3 == 1:
                            check = False
                            check1 = False
                            check2 = False
                            while not check:
                                book1 = input("Dimmi il nome del primo libro: ").lower()
                                book2 = input("Dimmi il nome del secondo libro: ").lower()

                                virgola1 = "," in book1
                                virgola2 = "," in book2

                                for i in range(book_df.shape[0]):
                                    # Controllo per trovare il libro all'interno del dataset
                                    if book1 == book_df.title[i].lower():
                                        check1 = True
                                    if book2 == book_df.title[i].lower():
                                        check2 = True
                                if check1 == True and check2 == True:
                                    check = True
                                else:
                                    print("Uno dei libri non è presente, inseriscine altri esistenti o controlla di aver scritto correttamente\n")

                            if virgola1 or virgola2:
                                virgola = True
                            else:
                                virgola = False

                            populate_kb_rating(book_kb, book_df, virgola)

                            if virgola1:
                                book1_final = input_string(book1).lower()
                                result_book1 = book_kb.query(pl.Expr(f"rated(What,{book1_final})"))
                            else:
                                result_book1 = book_kb.query(pl.Expr(f"rated(What,{book1})"))

                            if virgola2:
                                book2_final = input_string(book2).lower()
                                result_book2 = book_kb.query(pl.Expr(f"rated(What,{book2_final})"))
                            else:
                                result_book2 = book_kb.query(pl.Expr(f"rated(What,{book2})"))

                            new_result1 = output_string(str(result_book1[0]))
                            new_result2 = output_string(str(result_book2[0]))

                            if float(new_result1) > float(new_result2):
                                print("\nIl libro migliore è:", book1, "perché la sua media di recensioni è:",
                                      new_result1,
                                      "; e la qualità di", book2, "è", new_result2)
                            elif float(new_result1) < float(new_result2):
                                print("\nIl libro migliore è:", book2, "perché la sua media di recensioni è:",
                                      new_result2,
                                      "; e la qualità di", book1, "è", new_result1)
                            elif float(new_result1) == float(new_result2):
                                print("\nI due libri hanno la stessa qualità, perché la qualità di", book1, "è",
                                      new_result1,
                                      "; e la qualità di", book2, "è", new_result2)
                            print("\nPuoi selezionare una nuova ricerca: ")

                        if c3 == 2:
                            star = input("\nI libri con quale valutazione vuoi ricercare? (5)(4)(3)(2)(1): ")
                            populate_kb_rating_star(book_kb, book_df)
                            book_dict = {}
                            for index in range(book_df.shape[0]):
                                book = input_string(book_df.title[index])
                                result_book = book_kb.query(pl.Expr(f"rated(What,{book})"))
                                res = output_string(str(result_book[0]))
                                if int(star) + 1 > float(res) >= int(star):
                                    book_dict[book_df.title[index]] = res

                            print(book_dict)

                        if c3 == 3:
                            check = False
                            while not check:
                                autore = input("\nI libri con quale autore vuoi ricercare?: ").lower()
                                for i in range(book_df.shape[0]):
                                    # Controllo per trovare l'autore all'interno del dataset
                                    if autore == book_df.author[i].lower():
                                        check = True
                                if not check:
                                    print("Autore non presente, inseriscine un altro esistente o controlla di aver scritto correttamente\n")

                            populate_kb_all_written_by(book_kb, book_df)
                            auth_dict = {}
                            for index in range(book_df.shape[0]):
                                book = input_string(book_df.title[index])
                                result_book = book_kb.query(pl.Expr(f"is_written_by(What,{book})"))
                                res = output_string(str(result_book[0]))
                                if str(autore.title()) in str(res):
                                    auth_dict[book_df.title[index]] = res

                            print(auth_dict)

                        if c3 == 4:
                            check = False
                            while not check:
                                genere = input("\nDi quale genere vuoi ricercare il miglior rating?: ").lower()
                                for i in range(book_df.shape[0]):
                                    # Controllo per trovare il genere all'interno del dataset
                                    if genere in book_df.genre[i].lower():
                                        check = True
                                if not check:
                                    print("Genere non presente, inseriscine un altro esistente o controlla di aver scritto correttamente\n")

                            populate_kb_best_genre(book_kb, book_df)
                            populate_kb_rating_star(book_kb, book_df)
                            gen_dict = {}
                            for index in range(book_df.shape[0]):
                                book = input_string(book_df.title[index])
                                genre_book = book_kb.query(pl.Expr(f"is_genre(What,{book})"))
                                res = output_string(str(genre_book[0]))
                                if str(genere.title()) in str(res):
                                    gen_dict[book_df.title[index]] = res
                                    rating_book = book_kb.query(pl.Expr(f"rated(What,{book})"))
                                    result = output_string(str(rating_book[0]))
                                    gen_dict[book_df.title[index]] = result
                            Top10 = sorted(gen_dict.items(), key=lambda x: x[1], reverse=True)
                            print(Top10[:10])

                        elif c3 == 5:
                            break

                        elif c3 < 1 or c3 > 5:
                            print("il valore inserito non è valido, inseriscine un'altro")

                    else:
                        print("il valore inserito non è un numero, inserisci un valore numerico")

            elif c1 == 3:
                print(
                    "\nIn questa sezione della knowledge base vengono rivalutati i libri,\n"
                    "non solo in base al rating medio ma anche in base al numero di recensioni")

                check = False
                while not check:
                    book_title = input("Dammi il nome di un libro: ").lower()
                    # Controllo sul titolo del libro inserito dall'utente per vedere se contiene una virgola
                    v = "," in book_title
                    for i in range(book_df.shape[0]):
                        # Controllo per trovare il libro all'interno del dataset
                        if book_title == book_df.title[i].lower():
                            check = True
                    if not check:
                        print("Libro non trovato, inseriscine un altro\n")

                s = f"\nConsiderando il numero di recensioni di {book_title.title()}, ovvero: "

                populate_kb_rating_counts(book_kb, book_df, v)
                populate_kb_rating(book_kb, book_df, v)
                populate_kb_reevaluation(book_kb, book_df, v)
                avg_rating, avg_no_rating = average_of_ratings()
                avg_rating = "{:.2f}".format(avg_rating)

                if v:
                    reeval_book = book_kb.query(pl.Expr(f"re_evaluation(What,{input_string(book_title.lower())})"))
                    rating_book = book_kb.query(pl.Expr(f"rated(What,{input_string(book_title.lower())})"))
                    no_rating_book = book_kb.query(pl.Expr(f"rating_count(What,{input_string(book_title.lower())})"))
                else:
                    reeval_book = book_kb.query(pl.Expr(f"re_evaluation(What,{book_title.lower()})"))
                    rating_book = book_kb.query(pl.Expr(f"rated(What,{book_title.lower()})"))
                    no_rating_book = book_kb.query(pl.Expr(f"rating_count(What,{book_title.lower()})"))

                ratings = output_string(str(no_rating_book[0]))
                rate = output_string(str(rating_book[0]))
                reevaluation = output_string(str(reeval_book[0])).lower()

                if reevaluation == "molto positva":
                    s += (f"\n{ratings},\nal momento molto sopra la media generale ({int(avg_no_rating)}) "
                          f"e considerando il rating medio ricevuto: \n{rate}\nanch'esso sopra la media ({avg_rating}), "
                          f"la valutazione finale della community è: \nMOLTO POSITIVA\n")

                elif reevaluation == "molto negativa":
                    s += (f"\n{ratings},\nal momento molto sopra la media generale ({int(avg_no_rating)}) "
                          f"e considerando il rating medio ricevuto: \n{rate}\nche risulta sotto la media ({avg_rating}), "
                          f"la valutazione finale della community è: \nMOLTO NEGATIVA\n")

                else:
                    s += (f"\n{ratings},\nin relazione con la media del numero di recensioni, ovvero:"
                          f" ({int(avg_no_rating)}), "
                          f"e considerando il rating medio ricevuto: \n{rate}\ne ponendo anch'esso in relazione "
                          f"alla media: ({avg_rating}), "
                          f"la valutazione finale della community è: \n{reevaluation.upper()},\n"
                          f"ma può variare all'aumentare dei rating ricevuti")

                print(s)

            elif c1 == 4:
                break

            elif c1 < 1 or c1 > 4:
                print("il valore inserito non è valido, inseriscine un'altro")

        else:
            print("il valore inserito non è un numero, inserisci un valore numerico")
