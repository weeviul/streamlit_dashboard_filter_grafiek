import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Waterkwaliteitsdashboard")

uploaded_file = st.file_uploader("Laad een CSV-bestand op", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=None, engine="python")
    
    if "tijd" in df.columns:
        df["tijd"] = pd.to_datetime(df["tijd"], errors="coerce")
        df = df.dropna(subset=["tijd"])
        df = df.sort_values("tijd")

        # Toon kolomnamen behalve "tijd"
        parameter_opties = [col for col in df.columns if col != "tijd"]
        
        # Meerdere parameters selecteerbaar
        geselecteerde_parameters = st.multiselect("Kies parameters", parameter_opties)

        if geselecteerde_parameters:
            fig, ax = plt.subplots()
            for parameter in geselecteerde_parameters:
                ax.plot(df["tijd"], df[parameter], label=parameter)
            
            ax.set_xlabel("Tijd")
            ax.set_ylabel("Waarde")
            ax.set_title("Tijdsgrafiek van geselecteerde parameters")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)
            plt.xticks (rotation=45)
        else:
            st.info("Selecteer minstens één parameter om een grafiek te tonen.")
    else:
        st.error("Geen 'tijd'-kolom gevonden in de dataset.")

