create table if not EXISTS produtos(
    id serial primary key,
    codigo varchar(45) not null unique,
    codigo_referenia varchar(45) not null unique,
    descricao text,
    preco numeric(10,2) not null
);

CREATE TABLE IF NOT EXISTS estoques (
    id SERIAL PRIMARY KEY,
    produto VARCHAR(50),
    empresa VARCHAR(10),
    quantidade INTEGER
);


INSERT INTO estoques (produto, empresa, quantidade) VALUES
('P001', '01', 10),
('P002', '01', 5),
('P003', '01', 8),
('P004', '02', 12),
('P005', '02', 0);
