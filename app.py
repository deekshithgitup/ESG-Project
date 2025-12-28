import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("/Users/deekshithsathrasalagangadharaiah/Documents/Documents - Deekshith’s MacBook Air/Sem 3/Capstone Project/data.csv")

# -----------------------------
# Helper Functions
# -----------------------------
def risk_label(score):
    if score >= 75:
        return "Low Risk 🟢"
    elif score >= 50:
        return "Medium Risk 🟡"
    else:
        return "High Risk 🔴"

# -----------------------------
# App Title
# -----------------------------
st.set_page_config(page_title="ESG Score Analyzer", layout="wide")
st.title("🌱 ESG Company Score Analyzer")

st.write("AI-powered ESG analysis and sustainability benchmarking")

# -----------------------------
# Company Selection
# -----------------------------
company = st.selectbox(
    "Select a Company",
    sorted(df['name'].dropna().unique())
)

company_data = df[df['name'] == company].iloc[0]

# -----------------------------
# ESG Score Cards
# -----------------------------
st.subheader("📊 ESG Scorecard")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Environment", round(company_data['environment_score'], 2))
col2.metric("Social", round(company_data['social_score'], 2))
col3.metric("Governance", round(company_data['governance_score'], 2))
col4.metric("Total ESG", round(company_data['total_score'], 2))

st.write("**ESG Grade:**", company_data['total_grade'])
st.write("**Risk Level:**", risk_label(company_data['total_score']))

# -----------------------------
# Peer Benchmarking
# -----------------------------
st.subheader("🏭 Industry Benchmarking")

industry_avg = df[df['industry'] == company_data['industry']]['total_score'].mean()

st.write("Industry:", company_data['industry'])
st.write("Company ESG Score:", round(company_data['total_score'], 2))
st.write("Industry Average ESG Score:", round(industry_avg, 2))

# -----------------------------
# Top & Low ESG Companies
# -----------------------------
st.subheader("🏆 Top ESG Companies")
st.dataframe(
    df.sort_values(by='total_score', ascending=False)
      .head(10)[['name','industry','total_score','total_grade']]
)

st.subheader("⚠️ Low ESG Companies")
st.dataframe(
    df.sort_values(by='total_score')
      .head(10)[['name','industry','total_score','total_grade']]
)

# -----------------------------
# Visualization
# -----------------------------
st.subheader("📉 Top vs Low ESG Comparison")

top5 = df.nlargest(5, 'total_score')
low5 = df.nsmallest(5, 'total_score')

fig, ax = plt.subplots(figsize=(8,4))
ax.bar(top5['name'], top5['total_score'], label="Top ESG")
ax.bar(low5['name'], low5['total_score'], label="Low ESG")
ax.set_xticklabels(list(top5['name']) + list(low5['name']), rotation=45)
ax.legend()

st.pyplot(fig)

