import pandas as pd  

# Criando um DataFrame com os dados  
dados = {  
    "order_id": [1, 2, 3, 4, 5],  
    "product": ["Notebook", "Mouse", "Teclado", "Monitor", "Impressora"],  
    "quantity": [2, 5, 3, 1, 4],  
    "price": [3500.00, 100.00, 250.00, 1200.00, 800.00],  
    "date": ["2024-02-27", "2024-02-26", "2024-02-25", "2024-02-24", "2024-02-23"]  
}  

df = pd.DataFrame(dados)  

# Salvando como CSV  
df.to_csv("vendas.csv", index=False)  

print("Arquivo CSV criado com sucesso!")
