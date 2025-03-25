import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.stats import pearsonr
import KNN

"""
In questo modulo, vengono gestiti tutti i metodi e le funzioni per il funzionamento del recommender system
"""


def get_info():
    """
    Funzione introduttiva che richiede all'utente di inserire i dati inerenti alla raccomandazione
    """
    print("**Books Recommender**\nInserire dati del libro\n")
    print(
        "Attenzione: Per garantire una ricerca accurata,"
        " inserire piu' informazioni possibili (compilare almeno due campi).\n")
    titolo = input("Titolo: ").lower()
    autore = input("Autore: ").lower()
    editore = input("Casa editrice: ").lower()
    data_pubblicazione = input("Data di pubblicazione: ").lower()
    categoria = input("Genere: ").lower()
    nro_pagine = input("Numero di pagine: ").lower()

    # con i dati forniti in input, viene creato un dataframe apparte per i suggerimenti dell'utente
    user_suggestion = pd.DataFrame(
        {'title': titolo, 'author': autore, 'publisher': editore, 'published_year': data_pubblicazione,
         'genre': categoria, 'number_of_pages': nro_pagine}, index=[0])

    return user_suggestion


def recommendation(dataset_path, user_suggestion):
    """
    Funzione kernel del recommender system, in cui attraverso il path con cui caricare il dataset e le info
    fornite dall'utente, crea il dataframe contenente i libri più simili da raccomandare e restituire in output
    """

    # lettura dataset
    books = pd.read_csv(dataset_path)
    books.dropna(inplace=True)

    # controllo presenza libro nel dataset
    check_if_not_present = 0

    for title in books['title']:
        if title != user_suggestion['title'][0]:
            check_if_not_present = 1
            book_index = 0
        else:
            book_index = books.index[books['title'] == title].values[0]
            check_if_not_present = 0
            break

    if check_if_not_present == 1:
        books = pd.concat([user_suggestion, books], ignore_index=True)

    books['comp_features'] = books['title'] + '|' + books['author'] + '|' + books['publisher'] + '|' + str(
        books['published_year']) + '|' + books['genre'] + '|' + str(books['number_of_pages'])

    # calcolo tf-idf e vettorizzazione delle feature utili al confronto
    vectorizer = TfidfVectorizer(analyzer='word')
    tfidf_matrix = vectorizer.fit_transform(books['comp_features'])
    tfidf_matrix_array = tfidf_matrix.toarray()

    indices = pd.Series(books['title'].index)

    id = indices[book_index]

    # calcolo correlazione di pearson per ogni libro all'interno del dataset rispetto al suggerimento
    corr = []
    for i in range(len(tfidf_matrix_array)):
        corr.append(pearsonr(tfidf_matrix_array[id], tfidf_matrix_array[i])[0])
    corr = list(enumerate(corr))
    sorted_corr = sorted(corr, reverse=True, key=lambda x: x[1])[1:6]
    corr_index = [i[0] for i in sorted_corr]
    correlated_books = \
        books[['title', 'author', 'publisher', 'published_year', 'genre', 'number_of_pages', 'average_rating']].iloc[
            corr_index]
    return correlated_books, corr_index


def output_recommendation():
    """
    funzione che stampa l'output della raccomandazione, richiamando il modulo KNN.py e allgando l'esito della previsione
    """
    user_recommendation = get_info()

    print("\nricerca libri in corso...\n")

    while True:
        corr, corr_index = recommendation('final_dataset.csv', user_recommendation)
        corr = KNN.knn_classification(corr, corr_index)
        print(corr)
        risp = input("I risultati ti soddisfano?").lower()

        if (risp == 'no') or (risp == 'n'):
            user_recommendation = get_info()
        else:
            break

    return corr
