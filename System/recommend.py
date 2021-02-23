import pandas as pd
import glob
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


def createdf():
    data = []
    for file_name in glob.glob(
            "Dataset/Labels/" + "*.txt"):
        # remove the filepath and just have the name
        nopath = file_name.split("\\")[1]
        # replace the . from .csv so it can be properly split
        parts = nopath.replace('.', '#').split('#')
        name = parts[0].replace("_", " ")
        f = open(file_name, "r")
        text = f.readline()
        # remove capitalisation and spaces between words
        cleanlist = text.replace(" ", "").lower()
        cleanlist = text.replace(",", " ").lower()

        data.append((name, cleanlist))

    dataframe = pd.DataFrame(data, columns=("Name", "Labels"))
    return dataframe


#  defining the function that takes in recipe name
# as input and returns the top 5 recommended recipes
def recommendations(Name, cosine_sim, df, indices):
    # initializing the empty list of recommended recipes
    recommended_recipes = []

    # get the index of the recipe that matches the name
    idx = indices[indices == Name].index[0]

    # creating a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending=False)

    # getting the indexes of the 10 most similar recipes
    top_5_indexes = list(score_series.iloc[1:6].index)

    # populating the list with the titles of the best 10 matching recipes
    for i in top_5_indexes:
        recommended_recipes.append(list(df.Name)[i])

    return recommended_recipes


def runreccomend(info):

    ingredients = info['ingredients']
    categories = info['categories']
    time = int(info['time'])
    labels = ingredients + ', ' + categories

    df = createdf()

    if time != 120:
        # #remove the recipes that dont fit the time frame
        info = pd.read_excel("Dataset/nutritional_info.xlsx")

        for index, row in info.iterrows():
            if row.preptime > time:
                df.drop(df.index[df['Name'] == row["name"]], inplace=True)

    df = df.append({"Name": "Likes", "Labels": labels.lower()}, ignore_index=True)

    # vectorise the data using the labels
    count = CountVectorizer()
    count_matrix = count.fit_transform(df['Labels'])

    # generating the cosine similarity matrix
    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    # creating a Series for the recipe titles so they are associated to an ordered numerical
    # list I will use in the function to match the indexes
    indices = pd.Series(df.Name)

    suggestions = recommendations("Likes", cosine_sim, df, indices)

    return suggestions

