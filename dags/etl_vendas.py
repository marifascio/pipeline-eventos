import pandas as pd  

# 🟢 EXTRAÇÃO: Carregar os dados do CSV  
df = pd.read_csv("vendas.csv")  
print("\n📌 Dados originais:\n", df.head())  

# 🟡 TRANSFORMAÇÃO: Criar a coluna total_value  
df["total_value"] = df["quantity"] * df["price"]  

# Converter a coluna 'date' para o formato datetime  
df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")  

# Filtrar pedidos com valores acima de R$ 100  
df_filtrado = df[df["total_value"] > 100]  

print("\n📌 Dados transformados:\n", df_filtrado.head())  

# 🔵 CARGA: Salvar os dados transformados em um novo CSV  
df_filtrado.to_csv("vendas_transformado.csv", index=False)  

print("\n✅ Processo ETL concluído! Dados salvos em 'vendas_transformado.csv'")
