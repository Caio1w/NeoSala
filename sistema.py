import sqlite3 

#------------ Parte de adicionar alunos----------------
def adicionar_aluno(nome, idade, escolaridade,serie, turma ):


    with sqlite3.connect('database.db') as banco:
        cur = banco.cursor()
        cur.execute('INSERT INTO Alunos (nome, idade, escolaridade, serie, turma) VALUES (?, ?, ?, ?, ?)',
                    (nome, idade, escolaridade, serie, turma))
        

        id_gerado = cur.lastrowid
        
        return id_gerado


def busca_aluno(sr, trm):
    with sqlite3.connect('database.db') as banco:
        cur = banco.cursor()
        cur.execute('SELECT nome, idade, escolaridade, serie, turma FROM Alunos WHERE serie = ? AND turma = ? ', (sr, trm) )
        lista = cur.fetchall()
        if not lista:
            return None
        return lista
    
def atualizador_turma(turma_nova, alunoid ):
    
    with sqlite3.connect('database.db') as banco:
        cur = banco.cursor()
        cur.execute('UPDATE Alunos SET turma = ? WHERE id = ?', (turma_nova, alunoid))
        return 'A sala do aluno foi alteradar com sucesso'



def apagador(idaluno):


    with sqlite3.connect('database.db') as banco:
        cur = banco.cursor()
        
        cur.execute('DELETE FROM Notas WHERE id = ?', (idaluno,))
        cur.execute('DELETE FROM Alunos WHERE id = ?', (idaluno,))
        return 'Aluno deletado com sucesso'

#Funções de notas abaixo:


def ad_nota(id, b1, b2, b3, b4, sr, trm):
    with sqlite3.connect('database.db') as banco:
        cur = banco.cursor()

        cur.execute('SELECT id FROM Notas WHERE aluno_id = ?', (id,))
        resultado = cur.fetchone()
        if resultado:
            return 'Nota já existente'
        else:
            try:
                cur.execute('INSERT INTO Notas (aluno_id, b1, b2, b3, b4, serie, turma) VALUES (?, ?, ?, ?, ?, ?,?) ', (id, b1, b2, b3, b4, sr, trm))
            except Exception as e:
                return 'Erro ao atribuir nota', e
            banco.commit()
            banco.close()
            return 'Notas atribuidas com sucesso.'


def alt_nota(aluno_id, b1=None, b2=None, b3=None, b4=None):
    with sqlite3.connect('database.db') as banco:
        cur = banco.cursor()
        campos = []
        valores = []

        if b1 is not None:
            campos.append("b1 = ?")
            valores.append(b1)
        if b2 is not None:
            campos.append("b2 = ?")
            valores.append(b2)
        if b3 is not None:
            campos.append("b3 = ?")
            valores.append(b3)
        if b4 is not None:
            campos.append("b4 = ?")
            valores.append(b4)

        if not campos:
            return "Nenhuma nota para atualizar"

        valores.append(aluno_id)
        sql = f"UPDATE notas SET {', '.join(campos)} WHERE aluno_id = ?"
        cur.execute(sql, valores)
        return f"Notas do aluno {aluno_id} atualizadas com sucesso"
def listar_notas(aluno_id):
    
    
    with sqlite3.connect('database.db') as banco:
        cur = banco.cursor()
        cur.execute(
            'SELECT b1, b2, b3, b4 FROM Notas WHERE aluno_id = ?',
            (aluno_id,)
        )
        notasal = cur.fetchone()
        return notasal