import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

sns.set(style='dark')

# data day_df
day_df = pd.read_csv('day_data.csv')
day_df.head()



# regis
def registered(df):
    regis = df.groupby(by='date').agg({
        'registered': 'sum'
    }).reset_index()
    return regis

# casual
def casual(df):
    casual = df.groupby(by='date').agg({
        'casual': 'sum'
    }).reset_index()
    return casual



# daily
def daily(df):
    daily = df.groupby(by='date').agg({
        'count': 'sum'
    }).reset_index()
    return daily

    

# month
def bulan(df):
    month = df.groupby(by='month').agg({
        'count': 'sum'
    })
    nama_bulan = [
        'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
        'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
    ]
    month = month.reindex(nama_bulan, fill_value=0)
    return month


# work
def works(df):
    work = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return work


# cuaca
def create_weather_rent_df(df):
    cuaca = df.groupby(by='weather_condition').agg({
        'count': 'sum'
    })
    return cuaca


#  filter

max = pd.to_datetime(day_df['date']).dt.date.max()
min = pd.to_datetime(day_df['date']).dt.date.min()
 
with st.sidebar:
    st.image("logo.jpg")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min,
        max_value= max,
        value=[min, max]
    )

main = day_df[(day_df['date'] >= str(start_date)) & 
                (day_df['date'] <= str(end_date))]


work = works(main)
daily = daily(main)
cuaca = create_weather_rent_df(main)
regis = registered(main)
casual = casual(main)
month = bulan(main)

st.header('Bike Sharing')

st.subheader('Daily Bicycle')
column1, column2, column3 = st.columns(3)


with column1:
    rent = daily['count'].sum()
    st.metric('Total User', value= rent)


with column2:
    casuals = casual['casual'].sum()
    st.metric('Casual User', value= casuals)


with column3:
    register = regis['registered'].sum()
    st.metric('Registered User', value= register)
 



# berdasarkan Bulanan dan Tahun
st.subheader('Monthly / Bulan')
fig, ax = plt.subplots(figsize=(18, 6))
ax.plot(
    month.index,
    month['count'],
    marker='*', 
    linewidth=5,
    color='tab:red'
)

for i, j in enumerate(month['count']):
    ax.text(i, j + 1, str(j), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=20, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)


# Berdasarkan Cuaca
st.subheader('Weatherly/Cuaca')
fig, ax = plt.subplots(figsize=(12, 6))
warna=["tab:red", "tab:green", "tab:blue"]
sns.barplot(
    x=cuaca.index,
    y=cuaca['count'],
    palette=warna
)
for i, j in enumerate(cuaca['count']):
    ax.text(i, j + 1, str(j), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)




# Berdasarkan Workday
st.subheader('Workday')
fig, ax = plt.subplots(figsize=(12, 6))
warna=["tab:orange", "tab:green"]
sns.barplot(
    x=work.index,
    y=work['count'],
    palette=warna
)
for i, j in enumerate(work['count']):
    ax.text(i, j + 1, str(j), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)
