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

st.write("Anzahl der Gäste die kommen: ")
for answer in number_of_guests:
    if answer["_id"] == "Ja":
        st.write("Zusagen: ")
        st.write(answer["sum_val"])
    else:
        st.write("Absagen:")
        st.write(answer["sum_val"])
st.divider()    

st.write("Anmeldungen:")

# mach ein find() auf der collection und gib die spalten name, confirmation und guests aus
guest_list = collection.find({}, {"name": 1, "confirmation": 1, "guests": 1})


df = pd.DataFrame(list(guest_list))
df = df.sort_values(by='name')
st.write(df)








# refresh button
if st.button("Refresh"):
    st.write("Refreshed!")
    # rerun the script
    st.experimental_rerun()

    


