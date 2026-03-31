import streamlit as st
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv("data.csv", header=None, nrows=2000)
df.columns = ['userId', 'productId', 'rating', 'timestamp']
df = df[['userId', 'productId', 'rating']]

st.set_page_config(page_title="E-commerce Recommender", layout="wide")

# Title
st.title("🛒 Smart E-commerce Recommendation System")

# Select user
user_id = st.selectbox("Select User", df['userId'].unique())

# Create matrix
user_item = df.pivot_table(index='userId', columns='productId', values='rating').fillna(0)

# Similarity
similarity = np.dot(user_item, user_item.T)
sim_df = pd.DataFrame(similarity, index=user_item.index, columns=user_item.index)

# Recommendation function
def recommend(user):
    similar_users = sim_df[user].sort_values(ascending=False)[1:4]
    recs = user_item.loc[similar_users.index].mean().sort_values(ascending=False)
    
    bought = user_item.loc[user]
    recs = recs[bought == 0]
    
    return recs.head(6)

# Button
if st.button("Get Recommendations"):

    st.subheader("Recommended Products")

    recs = recommend(user_id)

    cols = st.columns(3)

    for i, (product, score) in enumerate(recs.items()):
        with cols[i % 3]:
            st.image("https://via.placeholder.com/150", width=150)
            st.markdown(f"**Product ID:** {product}")
            st.markdown(f"⭐ Score: {round(score,2)}")