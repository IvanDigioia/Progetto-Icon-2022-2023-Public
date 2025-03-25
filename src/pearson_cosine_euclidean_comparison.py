import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import euclidean_distances
import time
'''
modulo per la ricerca della procedura più efficiente a livello temporale per il calcolo della similarità
'''
books_df = pd.read_csv('final_dataset.csv')
books_df.dropna(inplace=True)
book_title = "Take Two"
index = books_df.index[books_df['title'] == book_title].values[0]

books_df['comp_features'] = books_df['title'] + '|' + books_df['author'] + '|' + books_df['publisher'] + '|' + str(
    books_df['published_year']) + '|' + books_df['genre'] + '|' + str(books_df['number_of_pages'])


def cosine_similarity_time():
    """
    calcolo similarità del coseno
    """
    begin = time.time()

    vectorizer = TfidfVectorizer(analyzer='word')
    tfidf_matrix = vectorizer.fit_transform(books_df['comp_features'])

    cosine_similarity = linear_kernel(tfidf_matrix, tfidf_matrix)

    indices = pd.Series(books_df['title'].index)
    idx = indices[index]

    cosine_similarity_scores = list(enumerate(cosine_similarity[idx]))
    cosine_similarity_scores = sorted(cosine_similarity_scores, key=lambda x: x[1], reverse=True)
    cosine_similarity_scores = cosine_similarity_scores[1:6]
    books_index = [i[0] for i in cosine_similarity_scores]

    # Return the top 5 most similar games using integer-location based indexing (iloc)
    books = books_df[['title', 'author', 'publisher', 'published_year', 'genre', 'number_of_pages']].iloc[books_index]
    end = time.time()

    return end - begin


def pearson_similarity_time():
    """
    calcolo coefficiente di pearson
    """
    begin = time.time()

    vectorizer = TfidfVectorizer(analyzer='word')
    tfidf_matrix = vectorizer.fit_transform(books_df['comp_features'])
    tfidf_matrix_array = tfidf_matrix.toarray()

    indices = pd.Series(books_df['title'].index)
    idx = indices[index]

    correlation = []
    for i in range(len(tfidf_matrix_array)):
        correlation.append(pearsonr(tfidf_matrix_array[idx], tfidf_matrix_array[i])[0])
    correlation = list(enumerate(correlation))
    sorted_corr = sorted(correlation, reverse=True, key=lambda x: x[1])[1:6]

    books_index = [i[0] for i in sorted_corr]

    # Return dei top 5 libri più simili
    books = books_df[['title', 'author', 'publisher', 'published_year', 'genre', 'number_of_pages']].iloc[books_index]

    end = time.time()

    return end - begin


def euclidean_distance_time():
    """
    calcolo distanza euclidea
    """

    begin = time.time()

    vectorizer = TfidfVectorizer(analyzer='word')
    tfidf_matrix = vectorizer.fit_transform(books_df['comp_features'])
    distance = euclidean_distances(tfidf_matrix)

    indices = pd.Series(books_df['title'].index)
    idx = indices[index]

    euclidean_distances_scores = list(enumerate(distance[idx]))
    euclidean_distances_scores = sorted(euclidean_distances_scores, key=lambda x: x[1], reverse=True)
    euclidean_distances_scores = euclidean_distances_scores[1:6]

    books_index = [i[0] for i in euclidean_distances_scores]

    # Return dei top 5 libri più simili
    books = books_df[['title', 'author', 'publisher', 'published_year', 'genre', 'number_of_pages']].iloc[books_index]

    end = time.time()

    return end - begin


def calculating_sparsity(b_df):
    book_df = b_df.to_numpy()

    sparsity = 1.0 - (np.count_nonzero(book_df) / float(book_df.size))

    print('\nSparsità del dataset:', sparsity * 100, "%\n")


coseno = cosine_similarity_time()
pearson = pearson_similarity_time()
euclidean_distance = euclidean_distance_time()

print(f"Tempo di esecuzione per la similarità del coseno: {coseno}\n"
      f"Tempo di esecuzione per il calcolo della coorelazione di Pearson: {pearson}\n"
      f"Tempo di esecuzione per il calcolo della distanza euclidea: {euclidean_distance}\n\n")

calculating_sparsity(books_df)

