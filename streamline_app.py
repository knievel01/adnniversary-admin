import streamlit as st
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# MongoDB Client erstellen

uri = "mongodb+srv://" + st.secrets["database"]["user"]+ ":" + st.secrets["database"]["password"] + "@cluster0.0vhlagu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
collection = client["wedding"]["guests"]


st.title("🎉 10 Jahre Roman und Denise 🎉")
st.caption("So sieht's bis jetzt aus!")


# Get sum_val:{ $sum: "$guests" } from collection
sum_val = collection.aggregate([{"$group": {"_id": None, "total": {"$sum": "$guests"}}}])

st.markdown(f"Anzahl der Gäste: {sum_val}")

st.divider()    
# lade mir alle gäste in ein dataframe und sortiere nach name
df = pd.DataFrame(list(collection.find()))
df = df.sort_values(by='name')
st.write(df)

# refresh button
if st.button("Refresh"):
    st.write("Refreshed!")
    # rerun the script
    st.experimental_rerun()

    


