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


st.divider()    
# lade mir alle gäste in ein dataframe und sortiere nach name
df = pd.DataFrame(list(collection.find()))
df = df.sort_values(by='name')
st.write(df)

# please sum all values with { confirmation: 'Ja' } in the the collection and display the result
# hint: use the $sum operator
st.write("Anzahl der Gäste die kommen: ")

number_of_guests = collection.aggregate([
    {
        "$group": {
            "_id": "$confirmation",
            "sum_val": {
                "$sum": "$guests"
            }
        }
    }
])

for answer in number_of_guests:
    if answer["sum_val"] == "Ja":
        st.write("Zusagen: " + answer["sum_val"])
    else:
        st.write("Absagen: " + answer["sum_val"])


# refresh button
if st.button("Refresh"):
    st.write("Refreshed!")
    # rerun the script
    st.experimental_rerun()

    


