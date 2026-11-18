# %%
import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "notebook_connected"

# read the data
df = pd.read_csv('../data/coffee_sales.csv')
df.head(10)

# 3. Criar a coluna de mês
df['mes'] = df['data'].dt.to_period('M').astype(str)

# 4. Definir total_mensal: soma das unidades por mês
total_mensal = df.groupby('mes')['unidades'].sum()

# convert data column to datetime
df['data'] = pd.to_datetime(df['data'])
df.head()

# ensuring that date is in order
df = df.sort_values('data')
df.head()

# counting na's
df.isna().sum()


# plot time series
fig = px.line(df, 
    x='data', 
    y='vendas', 
    title='Vendas diárias da cafeteria'
)

fig.update_layout(
    xaxis_title='Data', 
    yaxis_title='Unidades vendidas'
)

# moving average 
df['media_7_dias'] = df['vendas'].rolling(7).mean()
df.head(10)

# plot time series with MA
fig = px.line(df, 
    x='data', 
    y=['vendas', 'media_7_dias'], 
    title='Vendas e média móvel'
)

fig.update_layout(
    xaxis_title='Data', 
    yaxis_title='Unidades vendidas', 
    legend_title='Série'
)

# dias da semana 
df['dia_semana'] = df['data'].dt.dayofweek
df.head()

# media por dia 
media_por_dia = df.groupby('dia_semana')['vendas'].mean()

media_por_dia.index = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
fig = px.bar(
    x=media_por_dia.index, 
    y=media_por_dia.values, 
    title='Média de vendas por dia da semana'
)
fig.update_layout(
    xaxis_title='Dia da semana', 
    yaxis_title='Média de unidades vendidas'
)

# boxplots
fig = px.box(
    df, 
    x='dia_semana', 
    y='vendas', 
    points='outliers',
    title='Distribuição das vendas por dia da semana'
)
fig.update_xaxes(
    tickvals=[0, 1, 2, 3, 4, 5, 6],
    ticktext=['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
)
fig.update_layout(
    xaxis_title='Dia da semana', 
    yaxis_title='Unidades vendidas'
)

fig.update_layout(
    xaxis_title='Data',
    yaxis_title='Unidades vendidas'
)

fig = px.bar (
    x=total_mensal.index,
    y=total_mensal.values,
    title='Total de vendas por mês'
)
fig.update_layout(xaxis_title='Mês', yaxis_title='Total de unidades vendidas')
fig.show()

maiores_vendas = df.sort_values('vendas', ascending=False)
maiores_vendas[['data', 'vendas']].head()

data_pico = maiores_vendas['data'].iloc[0]
print('Data do pico: ', data_pico)

inicio = data_pico - pd.Timedelta(days=14)
fim = data_pico + pd.Timedelta(days=14)

recorte = df[df['data'] >= inicio]
recorte = recorte[recorte['data'] <= fim]

fig = px.line(
    recorte,
    x='data', 
    y='vendas', 
    markers=True, 
    title='Vendas em torno do maior pico'
    )
fig.update_layout(xaxis_title='Data', yaxis_title='Unidades vendidas')
# %%