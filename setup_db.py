import sqlite3

banco = sqlite3.connect('database.db')

cur = banco.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS Alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL,
            escolaridade TEXT NOT NULL,
            serie INT NOT NULL,
            turma TEXT NOT NULL);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER NOT NULL,
            bimestre1 REAL,
            bimestre2 REAL,
            bimestre3 REAL,
            bimestre4 REAL,
            FOREIGN KEY (aluno_id) REFERENCES Alunos (id)
            
            
            );""")


