import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as ex
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime

st.set_page_config(layout="wide") 

col_names = ['Pid', 'Sex', 'Race', 'Ref_Date', 'Paper_Date', 'Referral_Date', 'Stat', 'Category', 'Offense',
            'General_Category', 'OffenseDescription', 'Referral_Type']

refs = pd.read_csv(r'Referrals 2010-2021 09-21-2021 17.06.csv', 
                  names=col_names, skiprows=1)

refs['Referral_Date'] = pd.to_datetime(refs['Referral_Date'])

general_2010 = refs.groupby(pd.Grouper(key='Referral_Date', freq='M'))['General_Category'].value_counts().unstack().fillna(0)
general_2016 = general_2010.loc[datetime.date(year=2016,month=1,day=1): ].copy()
general_2016.drop(['Contempt'], axis=1, inplace=True) # remove other category

st.title('Referral Offense Correlation')

st.dataframe(general_2016)


option = st.selectbox(
    'Offense 1', general_2016.columns)

option2 = st.selectbox(
    'Offense 2', general_2016.columns)


# ----------- scatter plots ---------------
fig = make_subplots(rows=1, cols=6, shared_yaxes=False, subplot_titles=("2016", "2017", "2018", '2019', '2020', '2021'))

fig.add_trace(
    go.Scatter(
        x=general_2016[option][:12],
        y=general_2016[option2][:12],
        mode="markers",
    ),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(
        x=general_2016[option][12:24],
        y=general_2016[option2][12:24],
        mode="markers",
    ),
    row=1, col=2
)
fig.add_trace(
    go.Scatter(
        x=general_2016[option][24:36],
        y=general_2016[option2][24:36],
        mode="markers",
    ),
    row=1, col=3
)
fig.add_trace(
    go.Scatter(
        x=general_2016[option][36:48],
        y=general_2016[option2][36:48],
        mode="markers",
    ),
    row=1, col=4
)
fig.add_trace(
    go.Scatter(
        x=general_2016[option][48:60],
        y=general_2016[option2][48:60],
        mode="markers",
    ),
    row=1, col=5
)
fig.add_trace(
    go.Scatter(
        x=general_2016[option][60:],
        y=general_2016[option2][60:],
        mode="markers",
    ),
    row=1, col=6
)

fig.update_xaxes(title_text=option, row=1, col=1)
fig.update_yaxes(title_text=option2, row=1, col=1)

fig.update_xaxes(tick0=0, dtick=10, row=1, col=1)
fig.update_xaxes(tick0=0, dtick=10, row=1, col=3)


fig.update_layout(width=1200, height=350, title_text="{} vs. {}".format(option, option2))
# -------------------------


# ------ Sub plots (line chart + r correlation)
fig1 = make_subplots(rows=2, cols=1, shared_yaxes=False)
y_list = ['2016', '2017', '2018', '2019', '2020', '2021']

fig1.add_trace(
go.Scatter(x=general_2016.index, y=general_2016[option], name=option),
row=1, col=1
)
fig1.add_trace(
    go.Scatter(x=general_2016.index, y=general_2016[option2], name=option2),
    row=1, col=1
)

c16 = round(general_2016[option][:12].corr(general_2016[option2][:12], method='pearson'), 2)
c17 = round(general_2016[option][12:24].corr(general_2016[option2][12:24], method='pearson'), 2)
c18 = round(general_2016[option][24:36].corr(general_2016[option2][24:36], method='pearson'), 2)
c19 = round(general_2016[option][36:48].corr(general_2016[option2][36:48], method='pearson'), 2)
c20 = round(general_2016[option][48:60].corr(general_2016[option2][48:60], method='pearson'), 2)
c21 = round(general_2016[option][60:].corr(general_2016[option2][60:], method='pearson'), 2)
c_list = [c16, c17, c18, c19, c20, c21]


fig1.add_trace(
    go.Scatter(x=y_list, y=c_list, name='Pearson Correlation'),
    row=2, col=1
)

fig1.update_yaxes(tick0=0, dtick=.3, row=2, col=1)
fig1.update_layout(width=1200, title_text="{} vs. {}".format(option, option2))
# ----------------------------

st.plotly_chart(fig1)
st.plotly_chart(fig)