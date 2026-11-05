CREATE TABLE IF NOT EXISTS cliente (id_cliente INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT 
NULL, telefone TEXT NOT NULL, email TEXT);
CREATE TABLE IF NOT EXISTS servico (id_servico INTEGER PRIMARY KEY AUTOINCREMENT, nome_servico TEXT 
NOT NULL, preco REAL NOT NULL);
CREATE TABLE IF NOT EXISTS profissional (id_profissional INTEGER PRIMARY KEY AUTOINCREMENT, 
nome_profissional TEXT NOT NULL, especialidade TEXT);
CREATE TABLE IF NOT EXISTS agendamento (id_agendamento INTEGER PRIMARY KEY AUTOINCREMENT, id_cliente 
INTEGER NOT NULL, id_servico INTEGER NOT NULL, id_profissional INTEGER NOT NULL, 
data_hora TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'Confirmado', FOREIGN 
KEY(id_cliente) REFERENCES cliente(id_cliente), FOREIGN KEY(id_servico) REFERENCES 
servico(id_servico), FOREIGN KEY(id_profissional) REFERENCES 
profissional(id_profissional));