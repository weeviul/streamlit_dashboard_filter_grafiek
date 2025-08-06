import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Meetwaarden Dashboard – Filter & Grafiek")

# Bestand uploaden
uploaded_file = st.file_uploader("📁 Upload een CSV-bestand", type=["csv"])

if uploaded_file:
    # Data inlezen
    df = pd.read_csv(uploaded_file, sep=None, engine="python")

    # Datumkolom automatisch detecteren
    for col in df.columns:
        try:
            df[col] = pd.to_datetime(df[col])
            tijd_kolom = col
            break
        except:
            continue
    else:
        tijd_kolom = None

    # Toon tabel
    st.subheader("📋 Tabeloverzicht")
    st.dataframe(df)

    # Kies numerieke parameter
    numerieke_kolommen = df.select_dtypes(include=["number"]).columns.tolist()

    if numerieke_kolommen:
        param = st.multiselect("📌 Kies parameters voor analyse", numerieke_kolommen)

        # Filter op waarden
        min_val, max_val = float(df[param].min()), float(df[param].max())
        gekozen_range = st.slider("Filter op waarde", min_val, max_val, (min_val, max_val))
        df_filtered = df[(df[param] >= gekozen_range[0]) & (df[param] <= gekozen_range[1])]

        # Sorteer indien tijd beschikbaar
        if tijd_kolom:
            df_filtered = df_filtered.sort_values(by=tijd_kolom)

        # Plot
        st.subheader(f"📈 Grafiek van '{param}'")
        fig, ax = plt.subplots()
        if tijd_kolom:
            ax.plot(df_filtered[tijd_kolom], df_filtered[param], marker='o')
            ax.set_xlabel("Tijd")
        else:
            ax.plot(df_filtered[param], marker='o')
            ax.set_xlabel("Index")
        ax.set_ylabel(param)
        ax.grid(True)
        st.pyplot(fig)
    else:
        st.warning("⚠️ Geen numerieke kolommen gevonden.")
else:
    st.info("📥 Upload een CSV-bestand om te beginnen.")
