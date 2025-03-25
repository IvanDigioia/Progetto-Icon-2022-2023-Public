from warnings import simplefilter
import pandas as pd
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split, RepeatedKFold, RandomizedSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder

"""
In questo modulo vengono gestiti metodi e funzioni per finetuning, preprocessing e training del KNN, utilizzato per
eseguire una previsione sulla classe già esistente average_rating
"""

simplefilter(action='ignore', category=UserWarning)


def df_elaboration():
    """
    metodo che carica il dataset in un dataframe per poi elaborarlo, rendendolo più adeguato per l'apprendimento
    """
    # Carica il dataset
    book_df = pd.read_csv('final_dataset.csv')
    book_df.dropna(inplace=True)

    return book_df


def randomized_search(hyperparameters, x_train, y_train):
    """
    Implementazione random search per fare finetuning degli iperparametri con cui addestrare il KNN
    """
    KNN = KNeighborsClassifier()

    # utilizzo della cross validation per trovare il numero di fold
    cvFold = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
    randomSearch = RandomizedSearchCV(estimator=KNN, cv=cvFold, param_distributions=hyperparameters)

    best_model = randomSearch.fit(x_train, y_train)

    return best_model


def model_evaluation(y_test, y_pred, pred_prob):
    """
    funzione che restituisce il roc score del modello
    """
    # controllo metriche di valutazione
    print('Classification report: \n', classification_report(y_test, y_pred, zero_division=1))

    # valutazione modello attraversoì ROC Score.
    roc_score = roc_auc_score(y_test, pred_prob, multi_class='ovr')
    print('ROC score: ', roc_score)

    return roc_score


def hyperparameters_search(x_train, x_test, y_train, y_test):
    """
    funzione di ricerca degli iperparametri migliori
    """

    result = {}
    n_neighbors = list(range(1, 31))
    weights = ['uniform', 'distance']
    metric = ['euclidean', 'manhattan', 'hamming']

    # Conversione a dizionario
    hyperparameters = dict(metric=metric, weights=weights, n_neighbors=n_neighbors)

    i = 0
    while i < 15:
        best_model = randomized_search(hyperparameters, x_train, y_train)

        bestweights = best_model.best_estimator_.get_params()['weights']

        bestMetric = best_model.best_estimator_.get_params()['metric']

        bestNeighbours = best_model.best_estimator_.get_params()['n_neighbors']

        knn = KNeighborsClassifier(n_neighbors=bestNeighbours, weights=bestweights, algorithm='auto', metric=bestMetric,
                                   metric_params=None, n_jobs=None)

        knn.fit(x_train, y_train)

        pred_prob = knn.predict_proba(x_test)

        # valutiamo il nostro modello
        roc_score = roc_auc_score(y_test, pred_prob, multi_class='ovr')

        result[i] = {
            'n_neighbors': bestNeighbours,
            'metric': bestMetric,
            'weights': bestweights,
            'roc_score': roc_score
        }

        i += 1

    result = dict(sorted(result.items(), key=lambda x: x[1]['roc_score'], reverse=True))

    first_el = list(result.keys())[0]

    result = list(result[first_el].values())

    return result


def searching_best_model_stats(x_train, x_test, y_train, y_test):
    """
    Questa funzione restituisce il knn dopo aver eseguito finetuning sugli iperparametri, trovando la combinazione
    che garantisce le prestazioni migliori
    """
    print('\n\nIniziale composizione del modello con hyperparameters basici...')
    knn = KNeighborsClassifier(n_neighbors=5, weights='uniform', algorithm='auto', p=2, metric='minkowski',
                               metric_params=None, n_jobs=None)

    knn.fit(x_train, y_train)

    # vengono mostrati i primi 5 elementi della predizionew
    print('\nPredizioni dei primi 5 elementi: ', knn.predict(x_test)[0:5], 'Valori effettivi:\n ', y_test[0:5])

    y_pred = knn.predict(x_test)

    pred_prob = knn.predict_proba(x_test)

    # valutiamo il nostro modello
    print('\nValutazione del modello...\n')
    model_evaluation(y_test, y_pred, pred_prob)

    print('\nLa nostra accuratezza è bassa, dobbiamo migliorare la qualità delle nostre predizioni\n')

    result = hyperparameters_search(x_train, x_test, y_train, y_test)

    print('\nWITH RANDOMIZED SEARCH:\n')

    bestweights = result[2]
    print('Best weights:', bestweights)

    bestMetric = result[1]
    print('Best metric:', bestMetric)

    bestNeighbours = result[0]
    print('Best n_neighbors:', bestNeighbours)

    # ricomposizione del modello con i nuovi parametri e valutazione dello stesso

    print('\nRicomponiamo il modello utilizzando i nuovi iperparametri...')

    knn = KNeighborsClassifier(n_neighbors=bestNeighbours, weights=bestweights, algorithm='auto', metric=bestMetric,
                               metric_params=None, n_jobs=None)

    knn.fit(x_train, y_train)

    # show first 5 model predictions on the test data
    print('\nPredizioni dei primi 5 elementi sulla categoria star: ', knn.predict(x_test)[0:5], 'Valori effettivi: ',
          y_test[0:5])

    y_pred = knn.predict(x_test)

    pred_prob = knn.predict_proba(x_test)

    # valutiamo il nostro modello
    model_evaluation(y_test, y_pred, pred_prob)

    print('\nAbbiamo incrementato la accuratezza del nostro modello')
    print('\nOra possiamo procedere alla fase di recommendation...')

    return knn


def prepare_dataset(book_df):
    """
    Preparazione del dataset per la suddivisione in training set e test set
    """

    # Seleziona le feature e il target
    selected_features = ['id', 'rating_count', 'number_of_pages', 'published_year', 'average_rating']
    data = book_df[selected_features]

    # Dividi i dati in addestramento e test
    x = data
    y = book_df["reeval_int"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1, stratify=y)

    return x_train, x_test, y_train, y_test


def knn_classification(corr, corr_index):
    """
    Funzione di costruzione del KNN e di restituzione della predizione solo per i libri restituiti dal recommender
    system
    """
    book_df = df_elaboration()
    label_encoder = LabelEncoder()
    book_df["reeval_int"] = label_encoder.fit_transform(book_df["re_evaluation"])
    x_train, x_test, y_train, y_test = prepare_dataset(book_df)
    # knn già perfezionato
    knn = KNeighborsClassifier(n_neighbors=20, weights="distance", metric="hamming")
    # Crea il classificatore KNN con ricerca parametri migliori
    # knn = searching_best_model_stats(x_train, x_test, y_train, y_test)

    knn.fit(x_train, y_train)

    for i in range(len(corr_index)):
        corr_index[i] = corr_index[i] - 1

    pred_value = book_df[['id', 'rating_count', 'number_of_pages',
                          'published_year', 'average_rating']].iloc[corr_index]

    reeval_prediction = knn.predict(pred_value)
    corr["re_evaluation_prediction"] = label_encoder.inverse_transform(reeval_prediction)
    return corr
