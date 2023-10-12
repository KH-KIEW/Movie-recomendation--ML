import pickle
import pandas as pd
import os
import ast
import re
from flask import Flask, redirect, request, render_template, jsonify

app = Flask(__name__)

# Load your pre-trained movie recommendation model using pickle
file_path = 'movies_list1.pkl'  # Adjust the file path as needed
with open(file_path,'rb') as f:
    load_data = pickle.load(f)
    
    
#collect title and link from dataset as dictionary
mov_link = {}
for i in range(0,len(load_data)):
   movi_name = load_data['title']
   key = load_data['homepage']
   mov_link[movi_name[i]] = key[i]



#collect list of  lists of genre
genre_name=[]
s=""
for i in range(0,len(load_data)):
    genres = load_data['genres']
    s=genres[i]
    # Safely evaluate the string as a Python list
    parsed_list = ast.literal_eval(s)
    # Extract "name" values without special characters
    result_list = []
    for item in parsed_list:
        if 'name' in item:
            name = item['name']
            # Remove special characters (non-alphanumeric and spaces) using regex
            name_list = re.sub(r'[^a-zA-Z0-9\s]', '', name)
            result_list.append(name_list)
    genre_name.append(result_list)
 



@app.route('/')
def home():
    return render_template('submit.html')



@app.route('/search', methods=['GET'])
def search():
    user_input = request.form
    query = request.args.get('query')
    # Your search logic here
    if query in mov_link.keys():
        image_url = mov_link[query]
        if image_url=="":
            return "Image URL not available for this movie in the given dataset."
        else:
            return redirect(image_url)
    return "Movie not found in the dataset."
    
    
    
@app.route('/filter-by-rating', methods=['POST'])
def recommend_movies():
    user_input = request.form
    user_genre = user_input.get('genre')
    user_rating = int(user_input.get('rating'))
    # Filter movies based on user input (genre and rating)
    recommended_movies = []
    ratings = []
    for i in range(0,len(load_data)):
        ratings = list(load_data['vote_average'])
        rate = ratings[i]
        titles=load_data['title']
        if (user_rating<=(rate//2)) and (user_genre=='all' or (user_genre in genre_name[i])):
            recommended_movies.append(str(titles[i]))
    return jsonify({'movies': recommended_movies})


if __name__ == '__main__':
    app.run(debug=True)
