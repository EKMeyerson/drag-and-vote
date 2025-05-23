import streamlit as st
import pandas as pd
import datetime
import os
from streamlit_sortables import sort_items
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# List of items to rank
items = [
'neuro ai',
#'neuro chan',
#'neuro choice',
#'neuro core',
#'neuro dan',
#'neuro dec',
#'neuro dust',
#'neuro kat',
'neuro cao',
#'neuro mas',
#'neuro mind',
#'neuro oracle',
#'neuro pai',
#'neuro dms',
#'brain leaf',
#'cleric',
#'coda',
#'dec agent',
#'dec factory',
'dec foundry',
#'decoda',
#'decora',
#'fulcrum',
#'mind agent',
#'orch dec',
'orchid',
#'orchnet',
#'prophet',
#'synapse',
#'tarot',
#'tesseract',
'unileaf',
#'caid'
]

# Ensure the CSV exists
if not os.path.exists("responses.csv"):
    pd.DataFrame(columns=["timestamp", "name", "rank", "item"]).to_csv("responses.csv", index=False)

# Track submission state
if "submitted" not in st.session_state:
    st.session_state.submitted = False

st.title("Rank the Names")
st.write("Drag and drop the options into your preferred order.")

# Name input
name = st.text_input("Your name (to make sure everyone votes)")

# Drag-and-drop ranking interface
ranked_items = sort_items(items)

# Submit button
if not st.session_state.submitted:
    if st.button("Submit Ranking"):
        if not ranked_items:
            st.warning("Please drag and rank the items before submitting.")
        else:
            timestamp = datetime.datetime.now().isoformat()
            df = pd.DataFrame({
                "timestamp": [timestamp]*len(ranked_items),
                "name": [name]*len(ranked_items),
                "rank": list(range(1, len(ranked_items)+1)),
                "item": ranked_items,
            })
            df.to_csv("responses.csv", mode='a', header=False, index=False)

            # Update google sheet
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google"], scope)
            client = gspread.authorize(creds)
            sheet = client.open("Rank Names").sheet1

            # Append rows
            sheet.append_rows(
                [[timestamp, name, i+1, item] for i, item in enumerate(ranked_items)]
            )


            st.success("✅ Ranking submitted!")
            st.session_state.submitted = True
else:
    st.info("You have already submitted your ranking.")

# Download responses
if os.path.exists("responses.csv"):
    df = pd.read_csv("responses.csv")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download All Responses as CSV",
        data=csv,
        file_name="responses.csv",
        mime="text/csv",
    )

