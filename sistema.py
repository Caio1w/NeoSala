import sqlite3 

#------------ Parte de adicionar alunos----------------
def adicionar_aluno(nome, idade, escolaridade,serie, turma ):

    banco = sqlite3.connect('database.db')
    cur = banco.cursor()

    cur.execute('INSERT INTO Alunos (nome, idade, escolaridade, serie, turma) VALUES (?, ?, ?, ?, ?)',
                (nome, idade, escolaridade, serie, turma))
    
    banco.commit()
    id_gerado = cur.lastrowid
    banco.close()
    return id_gerado


def busca_aluno(sr, trm):
    banco = sqlite3.connect('database.db')
    cur = banco.cursor()
    cur.execute('SELECT nome, idade, escolaridade, serie, turma FROM Alunos WHERE serie = ? AND turma = ? ', (sr, trm) )
    lista = cur.fetchall()
    if not lista:
        return None
    return lista
    
def atualizador_turma(turma_nova, alunoid ):
    
        banco = sqlite3.connect('database.db')
        cur = banco.cursor()
        cur.execute('UPDATE Alunos SET turma = ? WHERE id = ?', (turma_nova, alunoid))
        banco.commit()
        banco.close()
        return 'A sala do aluno foi alteradar com sucesso'



def apagador(idaluno):
    banco = sqlite3.connect('database.db')
    cur = banco.cursor()
    cur.execute('DELETE FROM Alunos WHERE id = ?', (idaluno,))
    banco.commit()
    banco.close()
    return 'Aluno deletado com sucesso'

