import sqlite3 


def adicionar_aluno( ):

    banco = sqlite3.connect('databaseturma')
    cur = banco.cursor()

    nome = str(input('Escreva o nome do aluno: ')).strip()
    idade = int(input('Escreva a idade do aluno: ')).strip()
    turma = str(input('Escreva a turma do aluno: ')).strip()
    
    cur.execute('INSERT INTO Alunos (nome, idade, turma) VALUES (?, ?, ?)',
                (nome,idade,turma))
    
    banco.commit()
    id_gerado = cur.lastrowid
    banco.close()

    return id_gerado


def busca_aluno():
    banco = sqlite3.connect('databaseturma')
    cur = banco.cursor()
    
    escolha1 = input('Você gostaria de listar todos os alunos? S para sim e N para não:  ').strip().upper()
    if escolha1 == 'S':
        cur.execute('SELECT * FROM Alunos ')
        tabela = cur.fetchall()
        banco.close()
        return tabela
    elif escolha1 == 'N':
        modo_busca = int(input('Você deseja procurar por nome ou id? 1 - id 2 - nome    '))

        if modo_busca == 1:
            idescolhido = int(input('Qual o id do aluno: '))
            cur.execute('SELECT * FROM Alunos WHERE id = ?', (idescolhido,))
        elif modo_busca == 2:
            nome_escolhido = input('Qual é o nome do aluno: ')
            cur.execute('SELECT * FROM Alunos WHERE nome LIKE ?', (f'%{nome_escolhido}%',))
        else:
            banco.close()
            return 'Opção invalida'
    else:
        banco.close()
        return 'Opção invalida'

    
    alunos = cur.fetchall()
    banco.close()
    return alunos

def atualizador():
    banco = sqlite3.connect('databaseturma')
    cur = banco.cursor()

    idaluno = int(input('Insira o id do aluno: '))
    cur.execute('SELECT nome FROM Alunos WHERE id = ?', (idaluno,))
    aluno = cur.fetchone()
    if not aluno:
        print('Aluno não encontrado')
        banco.close()
        return 'Aluno não encontrado'

    tacerto = input(f'Gostaria de atualizar os dados do aluno {aluno}? S para Sim E N para não: ').strip().upper()
    if tacerto == 'S':

        escolha = int(input('O que você deseja alterar no aluno: 1 - Nome\n2 - Idade\n3 - Turma\n4 - Tudo '))

        if escolha == 1:
            nome_novo = input('Qual o novo nome: ')
            cur.execute('UPDATE Alunos SET nome = ? WHERE id = ?', (nome_novo, idaluno))

        elif escolha == 2:
            idade_nova = int(input('Qual a idade nova: '))
            cur.execute('UPDATE Alunos SET idade = ? WHERE id = ?', (idade_nova, idaluno))

        elif escolha == 3:
            turma_nova = input('Qual a turma nova: ')
            cur.execute('UPDATE Alunos SET turma = ? WHERE id = ?', (turma_nova, idaluno))

        elif escolha == 4:
            nome_novo = input('Qual o novo nome: ')
            idade_nova = int(input('Idade nova: '))
            turma_nova = input('Turma nova: ')
            cur.execute('UPDATE Alunos SET nome = ?, idade = ?, turma = ? WHERE id = ?', (nome_novo, idade_nova, turma_nova, idaluno))
        
        banco.commit()
        banco.close()
        return 'Banco atualizado com sucesso!'
    elif tacerto == 'N':
        print('Nenhuma Alteração foi feita')
        banco.close()
        return 'Operação abortada pelo usuario'
        

def apagador():
    banco = sqlite3.connect('databaseturma')
    cur = banco.cursor()
    idaluno = int(input('Qual o id do aluno que você deseja deletar: '))
    cur.execute('SELECT nome FROM Alunos WHERE id = ?', (idaluno,))
    alunos = cur.fetchone()
    if not alunos:
        banco.close()
        return 'Aluno não encontrado'
    certeza = input(f'Aluno encontrado!\nNome: {alunos}\nTem certeza que deseja continuar? S Para sim e N para não: ').strip().upper()
    if certeza == 'S':
        cur.execute('DELETE FROM Alunos WHERE id = ?', (idaluno,))
        banco.commit()
        banco.close()
        return 'Aluno deletado com sucesso'
    elif certeza == 'N':
        banco.close()
        return 'Nenhuma alteração foi feita'
    else:
        banco.close()
        return 'Opção invalida, tente novamente'

    

           
        
if __name__ == "__main__":

    while True:
        print('1 - Para adicionar aluno')
        print('2 - Para listar alunos ')
        print('3 - Para atualizar dados')
        print('4 - Para deletar dados')
        print('0 - Para sair ')
        opção = int(input('Insira sua ação: '))

        if opção == 1:
            id_novo = adicionar_aluno()
            print('Id gerado para esse aluno: ', id_novo)
        elif opção == 2:
            for aluno in busca_aluno():
                print(f'Id = {aluno[0]}, Nome = {aluno[1]}, Idade = {aluno[2]}, Turma = {aluno[3]}')
        elif opção == 3:
            print(atualizador())
        
        elif opção == 4:
            print(apagador())

        elif opção == 0:
            print('Até a proxima!')
            break
        else:
            print('Opção invalida')


        
            
            

        
    
