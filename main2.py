import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

st.title('<title>')


url = 'https://raw.githubusercontent.com/esnt/Data/refs/heads/main/Names/popular_names.csv'
df = pd.read_csv(url)

noi = st.text_input('Ener a name:')
soi = st.radio('Choose the sex to plot', ['M', 'F'])
name_df = df[(df['name']==noi) & (df['sex']==soi)]

fig = plt.figure()
sns.lineplot(x=name_df['year'], y=name_df['n'], hue=name_df['sex'])
plt.title(noi)
plt.xlabel('year')
plt.ylabel('count')
plt.show()

st.pyplot(fig)

top10f = ['Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Barbara', 'Susan', 'Jessica', 'Karen', 'Sarah']
top10f_df = df[(df['name'].isin(top10f)) & (df['sex']=='F')]
top10f_df = top10f_df.drop('sex', axis=1)

fig2 = plt.figure()
sns.lineplot(x=top10f_df['year'], y=top10f_df['n'], hue=top10f_df['name'])
plt.show()

st.pyplot(fig2)

# streamlit run main.py