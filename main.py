import pandas as pd
import zipfile
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from io import BytesIO
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# from my_plots import *
import streamlit as st
import time

## LOAD DATA DIRECTLY FROM SS WEBSITE
@st.cache_data
def load_name_data():
    names_file = 'https://www.ssa.gov/oact/babynames/names.zip'
    response = requests.get(names_file)
    with zipfile.ZipFile(BytesIO(response.content)) as z:
        dfs = []
        files = [file for file in z.namelist() if file.endswith('.txt')]
        for file in files:
            with z.open(file) as f:
                df = pd.read_csv(f, header=None)
                df.columns = ['name','sex','count']
                df['year'] = int(file[3:7])
                dfs.append(df)
        data = pd.concat(dfs, ignore_index=True)
    data['pct'] = data['count'] / data.groupby(['year', 'sex'])['count'].transform('sum')
    return data

## LOAD DATA FROM A SAVED FILE
# df = pd.read_csv('all_names.csv')
# df['total_births'] = df.groupby(['year', 'sex'])['count'].transform('sum')
# df['prop'] = df['count'] / df['total_births']

df = load_name_data()

## LOAD DATA FROM A SMALLER NAME DATASET ON GITHUB
# url = 'https://raw.githubusercontent.com/esnt/Data/refs/heads/main/Names/popular_names.csv'
# df = pd.read_csv(url)
df['total_births'] = df.groupby(['year', 'sex'])['count'].transform('sum')
df['prop'] = df['count'] / df['total_births']

st.title('My Name App')


tab1, tab2, tab3 = st.tabs(['Overall', 'By Name', 'By Year'])

with tab1:
    st.write('Here is stuff about all the data')

    with st.sidebar:
        with st.spinner("Loading..."):
            time.sleep(5)

    color_m = st.color_picker("Pick a color for male")
    color_f = st.color_picker("Pick a color for female")

    fig = plt.figure(figsize=(15, 8))

    births_by_sex = df.groupby(['year', 'sex'])['count'].sum().unstack().fillna(0)
    births_by_sex['Total'] = births_by_sex['F'] + births_by_sex['M']
    births_by_sex['Male Ratio'] = births_by_sex['M'] / births_by_sex['Total']
    births_by_sex['Female Ratio'] = births_by_sex['F'] / births_by_sex['Total']

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(births_by_sex.index, births_by_sex['Male Ratio'], label='Male', color=color_m)
    ax.plot(births_by_sex.index, births_by_sex['Female Ratio'], label='Female', color=color_f)
    ax.set_title('Gender Ratio Over Time')
    ax.set_ylabel('Proportion')
    ax.set_xlabel('Year')
    ax.legend()

    st.pyplot(fig)
    


with tab2:
    st.write('Name')

    # pick a name
    noi = st.text_input('Enter a name')
    plot_female = st.checkbox('Plot female line')
    plot_male = st.checkbox('Plot male line')
    name_df = df[df['name']==noi]

    fig = plt.figure(figsize=(15, 8))

    if plot_female:
        sns.lineplot(data=name_df[name_df['sex'] == 'F'], x='year', y='count', label='Female')

    if plot_male:
        sns.lineplot(data=name_df[name_df['sex'] == 'M'], x='year', y='count', label='Male')

    plt.title(f'Popularity of {noi} over time')
    plt.xlim(1880, 2025)
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.xticks(rotation=90)
    plt.legend()
    plt.tight_layout()

    st.pyplot(fig)

    with st.expander("Details from the Social Security database"):
        st.write('"All names are from Social Security card applications for births that occurred in the United States after 1879. Note that many people born before 1937 never applied for a Social Security card, so their names are not included in our data. For others who did apply, our records may not show the place of birth, and again their names are not included in our data."')



with tab3:
    st.write('Year')

    years = [i for i in range(1880, 2023)]

    tyear = st.select_slider(
    "Select a year",
    options=years)

    year_of_interest = tyear
    top_names = df[df['year'] == year_of_interest]
    

    st.write(f'Details of the top male name in {tyear}:', top_names[top_names['sex'] == 'M'].nlargest(1, 'count'))
    st.write(f'Details of the top female name in {tyear}:', top_names[top_names['sex'] == 'F'].nlargest(1, 'count'))

    topnums = [i for i in range(1, 11)]

    topn = st.select_slider('Select a number', options=topnums)

    top_female = top_names[top_names['sex'] == 'F'].nlargest(topn, 'count')
    top_male = top_names[top_names['sex'] == 'M'].nlargest(topn, 'count')
    

    fig = plt.figure(figsize=(15, 8))
    sns.barplot(data=top_female, x='count', y='name')
    plt.title(f"Top {topn} Female Names in {year_of_interest}")
    plt.xlabel('Count')
    plt.ylabel('Name')
    plt.tight_layout()
    st.pyplot(fig)

    fig = plt.figure(figsize=(15, 8))

    

    sns.barplot(data=top_male, x='count', y='name')
    plt.title(f"Top 10 Male Names in {year_of_interest}")
    plt.xlabel('Count')
    plt.ylabel('Name')
    plt.tight_layout()
    st.pyplot(fig)

    

