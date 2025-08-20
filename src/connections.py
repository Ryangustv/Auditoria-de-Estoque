import psycopg2 as pg 

#Conexão com banco ERP, dados de origem
conexaoErp = pg.connect(
    host="localhost",
    port=5442,
    user="erp",
    password="erp123",
    database="erp"
)
#Conexão com banco HUB, dados de destino
conexaoHub = pg.connect(
    host="localhost",
    port=5332,
    user="hubcon",
    password="hub123",
    database="postgres"
)