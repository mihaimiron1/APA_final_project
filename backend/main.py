from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

# Încărcăm matricea interacțiunilor și datele procesate
def load_data():
    interactions_matrix = pd.read_csv('APA_PR\interact.csv', index_col=0)
    data = pd.read_csv('APA_PR\procesed_data.csv')
    data_orig = pd.read_csv('APA_PR\dating_data.csv')
    mlb = MultiLabelBinarizer()
    interests_matrix = mlb.fit_transform(data_orig['Interests'].str.split())  # Split pe spațiu pentru a crea lista de interese
    interests_df = pd.DataFrame(interests_matrix, columns=mlb.classes_)
    return data, interactions_matrix, interests_df

def update_interaction_matrix(new_interaction):
    new_interaction.to_csv('APA_PR/interact.csv', index=False)


# Funcția de recomandare a utilizatorilor
def recommend_users_by_id(user_id, data, similarity_matrix, interactions_matrix, top_n=2):
    if user_id not in interactions_matrix.index:
        return "ID-ul utilizatorului nu există în matricea de interacțiuni."

    user_index = data[data['ID'] == user_id].index[0]
    similarity_scores = similarity_matrix[user_index]

    preferred_gender = data.loc[user_index, 'Preferred_Gender']
    age_min = data.loc[user_index, 'Age_Min']
    age_max = data.loc[user_index, 'Age_Max']

    # Filtrare pe baza preferințelor de gen și vârstă
    filtered_data = data[(data['Gender'] == preferred_gender) & 
                         (data['Age'] >= age_min) & 
                         (data['Age'] <= age_max)]

    if filtered_data.empty:
        return "Nu există utilizatori care să se potrivească pe baza preferințelor."
    
    # Excludem utilizatorii deja interacționați
    interacted_users = interactions_matrix.iloc[user_index]
    
    interacted_users = interacted_users[interacted_users > 0].index.tolist()
    #print("uSeR_Iassadada::::::::::::::::",interacted_users)
    interacted_users = [int(user_id) for user_id in interacted_users]

    filtered_data = filtered_data[~filtered_data['ID'].isin(interacted_users)]

    #print("filtered_data_secod::::::::::::::::",filtered_data['ID'])

    if filtered_data.empty:
        print("Nu există utilizatori noi de recomandat.")
        return "Nu există utilizatori noi de recomandat."
        
    

    #persoane asemanataore cu useul logat
    find_like_pers=data[
        (data['Gender'] == data.loc[user_index, 'Gender']) &  
        (data['Preferred_Gender'] == data.loc[user_index, 'Preferred_Gender'])
    
    ]
    if find_like_pers.empty:
        pass
    else:
        
        #cel mai asemanator user cu cel curent
        like_pers_user = similarity_scores[filtered_data.index].argsort()[::-1][:1]
        
        #transformam in int
        like_pers_user=int(like_pers_user)


        #extragem persoanele la care userul a dat like
        like_pers_interact=interactions_matrix.iloc[like_pers_user-1]
        like_pers_interact = like_pers_interact[like_pers_interact > 0].index.tolist()

        like_interact=[]
        for s in like_pers_interact:
            like_interact.append(int(s))
        like_interact = [i - 1 for i in like_interact]
        #marim scorul pers la care userul asemanator a dat like
        similarity_scores[like_interact] += 0.07


    # Calculăm cei mai similari utilizatori
    similar_users = similarity_scores[filtered_data.index].argsort()[::-1][:top_n]
    recommended_user_ids = filtered_data.iloc[similar_users]

    # Return a list of user dictionaries with necessary information
    return recommended_user_ids.to_dict(orient='records')

# Funcția pentru interacțiuni cu utilizatorii recomandați
def interact_with_recommended_users(user_id, recommended_user, interactions_matrix, interaction):
    interactions_matrix.iloc[user_id-1, recommended_user-1] = interaction
    interactions_matrix.to_csv('APA_PR\interact.csv')
 
# Funcția pentru a vedea prietenii
def give_friends(user_id, interactions_matrix):
    a = interactions_matrix.iloc[:, user_id - 1].tolist()  # Extrage coloana
    choise_1 = [i for i, val in enumerate(a) if val == 1]
    interact = [int(s) for s in choise_1]
    friend_user = []

    for s in interact:
        if interactions_matrix.iloc[user_id - 1, s] == 1:
            print(f"Utilizatorul {s+1} este prieten cu utilizatorul {user_id}.")
            friend_user.append(s+1)
            
    
    return friend_user

def calculate_similarity(data, interests_df):
    feature_columns = ['Vector_X', 'Vector_Y', 'Vector_Z'] + list(interests_df.columns)
    feature_matrix = data[feature_columns]
    scaler = StandardScaler()
    feature_matrix_scaled = scaler.fit_transform(feature_matrix)
    similarity_matrix = cosine_similarity(feature_matrix_scaled)
    return similarity_matrix


