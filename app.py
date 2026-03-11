import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI

client = OpenAI(api_key="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")

st.title("Talking Rabbitt 🐇")
st.subheader("Conversational AI for Business Data")

uploaded_file = st.file_uploader("Upload your sales CSV", type=["csv"])

if uploaded_file:
    
    df = pd.read_csv(uploaded_file)    
    st.write("Dataset Preview")
    st.dataframe(df)

    question = st.text_input("Ask a question about your data")

    if question:

        prompt = f"""
        You are a business data analyst.

        Dataset columns:
        {df.columns.tolist()}

        User question:
        {question}

        Provide:
        1. Clear answer
        2. Suggested chart
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}]
        )

        answer = response.choices[0].message.content

        st.write("AI Insight")
        st.write(answer)

        if "region" in df.columns and "revenue" in df.columns:
            chart_data = df.groupby("region")["revenue"].sum()

            fig, ax = plt.subplots()
            chart_data.plot(kind="bar", ax=ax)

            st.pyplot(fig)
