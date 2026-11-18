# %%
import pandas as pd
import data_profiling as dp

df = pd.read_csv('../data/coffee_sales.csv')

df['data'] = pd.to_datetime(df['data'])
df = df.sort_values('data')

relatorio = dp.ProfileReport(
    df,
    title='Relatório de EDA',
    explorative=True
    )

relatorio.to_file('../data/eda_profilling.html')
# %%
