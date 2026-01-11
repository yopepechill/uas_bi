# %%
# a. Extracting data from sources
import pandas as pd
df = pd.read_csv("C:\\Users\\ASUS\\Documents\\SEM 5\\BUSSINES INTELLIGENCE\\Data_UAS.csv")


# %%
# b. Transforming data to fit analytic needs
# Mengubah TotalCharges ke numerik & menghapus kolom yang tidak perlu
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')


# %%
# c. Loading data into business systems for analysis
# Dalam konteks Colab, data dimuat ke dataframe yang siap pakai
df_clean = df.copy()
print("Data berhasil di-load dan ditransformasi.")
df_clean.head()

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# =========================
# DASH APP
# =========================
app = Dash(__name__)
server = app.server     # <<< TARO DI SINI (WAJIB DEPLOY)

app.layout = html.Div([
    html.H1("Customer Churn Dashboard"),
    dcc.Graph(...)
])

# =========================
# RUN LOCAL
# =========================
if __name__ == "__main__":
    app.run()

# %%
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import numpy as np

# =========================
# DATA
# =========================
data = df_clean

# =========================
# KPI
# =========================
churn_rate = (data['Churn'] == 'Yes').mean()

# =========================
# FIGURES (SESUIAI NOTEBOOK)
# =========================

# 1. Distribusi Tenure
fig_tenure = px.histogram(
    data, x='tenure',
    title='Distribusi Lama Berlangganan (Tenure)'
)

# 2. Monthly Charges vs Churn
fig_box = px.box(
    data, x='Churn', y='MonthlyCharges',
    title='Monthly Charges vs Churn'
)

# 3. Scatter Tenure vs TotalCharges (Interaktif Plotly)
fig_scatter_tc = px.scatter(
    data,
    x='tenure',
    y='TotalCharges',
    color='Churn',
    title='Tenure vs Total Charges (Interaktif)'
)

# 4. Clustering K-Means
fig_cluster = px.scatter(
    data,
    x='tenure',
    y='MonthlyCharges',
    color='Cluster',
    title='Segmentasi Pelanggan (K-Means)'
)

# 5. Violin Plot Contract vs Tenure
fig_violin = px.violin(
    data,
    x='Contract',
    y='tenure',
    color='Churn',
    box=True,
    points='all',
    title='Distribusi Tenure berdasarkan Kontrak dan Churn'
)

# 6. Time Series Trend (Tenure ~ MonthlyCharges)
ts_data = data.groupby('tenure')['MonthlyCharges'].mean().reset_index()

fig_trend = px.line(
    ts_data,
    x='tenure',
    y='MonthlyCharges',
    title='Tren Rata-rata Monthly Charges berdasarkan Tenure'
)

# =========================
# DASH APP
# =========================
app = Dash(__name__)
server = app.server   # <-- PENTING untuk deploy

app.layout = html.Div([

    html.H1("Customer Churn Dashboard", style={'textAlign': 'center'}),

    # KPI
    html.Div([
        html.H3(f"Churn Rate: {churn_rate:.2%}")
    ], style={
        'textAlign': 'center',
        'border': '2px solid black',
        'width': '30%',
        'margin': 'auto',
        'padding': '10px'
    }),

    html.Br(),

    dcc.Tabs([

        # TAB 1 — EDA
        dcc.Tab(label='Exploratory Data Analysis', children=[
            html.Div([
                dcc.Graph(figure=fig_tenure, style={'width': '50%'}),
                dcc.Graph(figure=fig_box, style={'width': '50%'})
            ], style={'display': 'flex'})
        ]),

        # TAB 2 — Relationship
        dcc.Tab(label='Variable Relationship', children=[
            dcc.Graph(figure=fig_scatter_tc),
            dcc.Graph(figure=fig_violin)
        ]),

        # TAB 3 — Segmentation
        dcc.Tab(label='Customer Segmentation', children=[
            dcc.Graph(figure=fig_cluster)
        ]),

        # TAB 4 — Trend & Time Series
        dcc.Tab(label='Trend Analysis', children=[
            dcc.Graph(figure=fig_trend)
        ])

    ])

])

# =========================
# RUN
# =========================
app.run(debug=True, port=8054)
# %%
