import numpy as np
import pandas as pd


'''
Questo modulo serve a arricchire il dataset con una nuova feature ideate da noi, che rivaluta ogni libro in base al 
rating e al numero di recensioni
'''

book_df = pd.read_csv('final_datasetv2.csv')

book_df.drop('re_evaluation', axis=1, inplace=True)
book_df['re_evaluation'] = np.nan
avg_rating = book_df['average_rating'].mean()
avg_no_rating = book_df['rating_count'].mean()
offset_noratings = 1500
offset_rating = 0.25
print(avg_rating, avg_no_rating)

for i in range(book_df.shape[0]):

    if (float(book_df.average_rating[i]) >= avg_rating + offset_rating and
            float(book_df.rating_count[i]) >= float(avg_no_rating) + offset_noratings):

        book_df.re_evaluation[i] = "MOLTO POSITIVA"

    elif (float(book_df.average_rating[i]) <= float(avg_rating) - offset_rating and
          float(book_df.rating_count[i]) >= float(avg_no_rating) + offset_noratings):

        book_df.re_evaluation[i] = "MOLTO NEGATIVA"

    elif ((float(book_df.average_rating[i]) <= float(avg_rating) - offset_rating) and
          ((float(book_df.rating_count[i]) >= float(avg_no_rating)) or
          (float(book_df.rating_count[i]) <= float(avg_no_rating)))):
        book_df.re_evaluation[i] = "NEGATIVA"

    elif ((float(book_df.average_rating[i]) >= float(avg_rating) + offset_rating) and
          ((float(book_df.rating_count[i]) >= float(avg_no_rating)) or
          (float(book_df.rating_count[i]) <= float(avg_no_rating)))):

        book_df.re_evaluation[i] = "POSITIVA"

    elif ((float(book_df.rating_count[i]) >= float(avg_no_rating) + offset_noratings) and
          ((float(book_df.average_rating[i]) >= float(avg_rating)) or
          (float(book_df.average_rating[i]) <= float(avg_rating)))):

        book_df.re_evaluation[i] = "POSITIVA"

    else:
        book_df.re_evaluation[i] = "NELLA MEDIA"


book_df.to_csv('final_datasetv3.csv', index=False)
