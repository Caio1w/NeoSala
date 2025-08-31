import sqlite3

#------------ Parte de adicionar alunos----------------
def adicionar_aluno(nome, idade, escolaridade, serie, turma):
    with sqlite3.connect('database.db') as banco:
        cur = banco.cursor()
        cur.execute(
            'INSERT INTO Alunos (nome, idade, escolaridade, serie, turma) VALUES (?, ?, ?, ?, ?)',
            (nome, idade, escolaridade, serie, turma)
        )
        id_gerado = cur.lastrowid
        return id_gerado

def busca_aluno(sr, trm):
    with sqlite3.connect('database.db') as banco:
        cur = banco.cursor()
        cur.execute(
            'SELECT nome, idade, escolaridade, serie, turma FROM Alunos WHERE serie = ? AND turma = ?',
            (sr, trm)
        )
        lista = cur.fetchall()
        if not lista:
            return None
        return lista

def atualizador_turma(turma_nova, alunoid):
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

# Funções de notas abaixo:

def ad_nota_fundamental(id, por, mat, cie, his, ge, bi, sre, trm):
    with sqlite3.connect('database.db') as banco:
        cur = banco.cursor()
        cur.execute(
            'SELECT bimestre FROM notas_fundamental WHERE aluno_id = ? AND bimestre = ?',
            (id, bi)
        )
        resultado = cur.fetchone()
        if resultado:
            return 'Nota já existente para este bimestre.'
        else:
            try:
                cur.execute(
                    'INSERT INTO notas_fundamental (aluno_id, portugues, matematica, ciencias, historia, geografia, bimestre, serie, turma) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (id, por, mat, cie, his, ge, bi, sre, trm)
                )
            except Exception as e:
                return 'Erro ao atribuir nota', e
            return 'Notas atribuidas com sucesso.'
def ad_nota_medio(id, por, mat, bio, qim, fis, his, ge, ing, bi, sre, trm):
    with sqlite3.connect('database.db') as banco:
        cur = banco.cursor()
        cur.execute(
            'SELECT bimestre FROM notas_medio WHERE aluno_id = ? AND bimestre = ?',
            (id, bi)
        )
        resultado = cur.fetchone()
        if resultado:
            return 'Nota já existente para este bimestre.'
        else:
            try:
                cur.execute(
                    'INSERT INTO notas_medio (aluno_id, portugues, matematica, biologia, quimica, fisica, historia, geografia, ingles, bimestre, serie, turma) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, por, mat, bio, qim, fis, his, ge, ing, bi, sre, trm))
            except Exception as e:
                return 'Erro ao atribuir nota', e
            return 'Notas atribuidas com sucesso.'
        
def alt_nota_fundamental(aluno_id, por=None, mat=None, cie=None, his=None, ge=None):
    with sqlite3.connect('database.db') as banco:
        cur = banco.cursor()
        campos = []
        valores = []

        if por is not None:
            campos.append("portugues = ?")
            valores.append(por)
        if mat is not None:
            campos.append("matematica = ?")
            valores.append(mat)
        if cie is not None:
            campos.append("ciencias = ?")
            valores.append(cie)
        if his is not None:
            campos.append("historia = ?")
            valores.append(his)
        if ge is not None:
            campos.append("geografia = ?")
            valores.append(ge)

        if not campos:
            return "Nenhuma nota para atualizar"

        valores.append(aluno_id)
        sql = f"UPDATE notas_fundamental SET {', '.join(campos)} WHERE aluno_id = ?"
        cur.execute(sql, valores)
        return f"Notas do aluno {aluno_id} atualizadas com sucesso"

def alt_nota_medio(aluno_id, por=None, mat=None, bio=None, qim=None, fis=None, his=None, ge=None, ing=None):
    with sqlite3.connect('database.db') as banco:
        cur = banco.cursor()
        campos = []
        valores = []

        if por is not None:
            campos.append("portugues = ?")
            valores.append(por)
        if mat is not None:
            campos.append("matematica = ?")
            valores.append(mat)
        if bio is not None:
            campos.append("biologia = ?")
            valores.append(bio)
        if qim is not None:
            campos.append("quimica = ?")
            valores.append(qim)
        if fis is not None:
            campos.append("fisica = ?")
            valores.append(fis)
        if his is not None:
            campos.append("historia = ?")
            valores.append(his)
        if ge is not None:
            campos.append("geografia = ?")
            valores.append(ge)
        if ing is not None:
            campos.append("ingles = ?")
            valores.append(ing)

        if not campos:
            return "Nenhuma nota para atualizar"

        valores.append(aluno_id)
        sql = f"UPDATE notas_medio SET {', '.join(campos)} WHERE aluno_id = ?"
        cur.execute(sql, valores)
        return f"Notas do aluno {aluno_id} atualizadas com sucesso"
    

def listar_notas(aluno_id, bimestre):
    with sqlite3.connect('database.db') as banco:
        cur = banco.cursor()
        cur.execute('SELECT escolaridade FROM Alunos WHERE id = ?', (aluno_id,))
        escolaridade = cur.fetchone()
        if escolaridade == 'Fundamental':
            cur.execute(
                'SELECT portugues, matematica, ciencias, historia, geografia, bimestre FROM notas_fundamental WHERE aluno_id = ? AND bimestre = ?',
                (aluno_id, bimestre)
            )
            notasal = cur.fetchone()
            return notasal
        if escolaridade == 'Médio':
            cur.execute(
                'SELECT portugues, matematica, biologia, quimica, fisica,,historia,geografia,ingles, bimestre FROM notas_medio WHERE aluno_id = ? AND bimestre = ?',
                (aluno_id, bimestre) 

        
        )
            notasal = cur.fetchone()
        return notasal