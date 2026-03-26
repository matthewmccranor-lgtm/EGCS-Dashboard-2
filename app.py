import streamlit as st
import pandas as pd
from services.ais import get_ais_data
from services.schedules import get_schedule
from services.compliance import get_compliance

st.set_page_config(layout="wide")
st.title("🚢 EGCS Live Vessel Dashboard")

df = pd.read_csv("data/vessels.csv")

results = []

for _, row in df.iterrows():
    vessel = row["Vessel Name"]

    ais = get_ais_data(vessel)
    schedule = get_schedule(vessel)

    p1 = ais["next_port"]
    p2 = schedule[0]
    p3 = schedule[1]

    zone, action = get_compliance(p1)

    results.append({
        "Vessel": vessel,
        "P1": p1,
        "ETA": ais["eta"],
        "P2": p2,
        "P3": p3,
        "Compliance": zone,
        "Fuel Action": action,
        "Lat": ais["lat"],
        "Lon": ais["lon"]
    })

df_live = pd.DataFrame(results)

st.dataframe(df_live, use_container_width=True)
st.map(df_live.rename(columns={"Lat":"lat","Lon":"lon"}))
