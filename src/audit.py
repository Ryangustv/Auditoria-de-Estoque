import psycopg2 as pg
import csv
from datetime import datetime 
import connections as c

connErp = c.conexaoErp.cursor()
connHub = c.conexaoHub.cursor()

connErp.execute("""SELECT 
                   produto,
                   empresa,
                   quantidade 
                   FROM estoques;""")

estoque_Erp = connErp.fetchall()

divergentes = []
erros = []

for produto, empresa, qnt_erp in estoque_Erp:

    connHub.execute(
        """SELECT quantidade 
           FROM mpp_estoques
           WHERE produto = %s
           AND empresa = %s ;""",
        (produto, empresa)
    )
    resultado = connHub.fetchone()

    if resultado:
        qnt_hub = resultado[0]

        if qnt_erp != qnt_hub:
            connHub.execute(
                """UPDATE mpp_estoques
                   SET quantidade = %s 
                   WHERE produto = %s 
                   AND empresa = %s;""",
                (qnt_erp, produto, empresa)
            )

            connHub.execute(
                """INSERT INTO mpp_logs (produto, empresa, quantidade_erp, quantidade_hub)
                   VALUES(%s, %s, %s, %s);""",
                   (produto, empresa, qnt_erp, qnt_hub)
            )

            print(f"PRODUTO {produto} DIVERGENTE | ESTOQUE ERP {qnt_erp} ESTOQUE HUB {qnt_hub}")

            divergentes.append({
            'produto': produto,
            'empresa': empresa,
            'quantidade_erp': qnt_erp,
            'quantidade_hub': qnt_hub,
            'status': 'corrigido',
            })    
    else:
        erros.append({
            'produto': produto,
            'empresa': empresa,
            'quantidade_erp': qnt_erp,
            'status': 'produto ausente no HUB'
        })

c.conexaoHub.commit()

print(f"\n AUDITORIA FINALIZADA, {len(divergentes)} PRODUTOS CORRIGIDOS E {len(erros)} COM ERRO")

#Criando arquivo csv para as correções
with open('Auditorias/divergencias.csv', mode='w', newline='') as csvfile:
    campos_head=['produto', 'empresa', 'quantidade_erp', 'quantidade_hub', 'status']
    writer = csv.DictWriter(csvfile, fieldnames=campos_head)

    writer.writeheader()
    writer.writerows(divergentes)

#Criando arquivo csv para logs com erro
with open('Auditorias/erros.csv', mode='w', newline='') as errorfile:
    error_head=['produto', 'empresa', 'quantidade_erp', 'status']
    writer = csv.DictWriter(errorfile, fieldnames=error_head)

    writer.writeheader()
    writer.writerows(erros)



#fechando conexões
connErp.close()
connHub.close()