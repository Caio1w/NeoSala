import sqlite3, tabulate, time
import sistema
banco = sqlite3.connect('database.db')
cur = banco.cursor()
banco_configurado = False
try:
    
    cur.execute(
        'INSERT INTO Alunos (nome, idade, escolaridade, serie, turma) VALUES (?, ?, ?, ?, ?)',
        ('teste', 1, 'teste', 'teste', 'teste')
    )
    print("Banco configurado!")
    cur.execute("DELETE FROM Alunos WHERE escolaridade = ?", ("teste",))
    banco.commit()
    banco_configurado = 1

except Exception as e:
    print("Banco de dados desconfigurado, crie a database nas opções abaixo.", e)
    banco_configurado = 0


while True:
    print('-------------------------------------------------')
    print('1 - Para adicionar aluno')
    print('2 - Para listar alunos ')
    print('3 - Para selecionar aluno')
    print('9 - Criar database.db')
    print('')
    print('0 - Para sair ')

    print('------------------------------------')
    option = None
    try:
        option = int(input('Insira sua ação: '))
    except ValueError:
        print('opção invalida')
    #As opções são daqui pra baixo, essa primeira é só pra configurar o banco
    if option == 9 and banco_configurado == 0:
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
        print('Database criada com sucesso, prossiga.')
        banco_configurado = 1
    #Aqui é pra sair independemente se o banco ta configurado ou não
    elif option == 0:
        print('Até a proxima!')
        break
    #Aqui é quando o usuario tenta fazer alguma ação com o banco desconfigurado
    elif banco_configurado == 0:
        print('Banco desconfigurado, configure o banco antes de tentar qualquer ação crie a database.db.')
        time.sleep(2)
        continue
    else:
        #e finalmente aqui são as opções 
        #Opção 1 - Adicionar aluno
        if option == 1:
            
            while True:
                nome = input('Insira o nome do aluno:  ').strip()
                idade = int(input('Insira a idade do aluno: '))
                escolaridade = int(input('1 - Fundamental\n2 - Médio\nInsira a escolaridade dadas as opções acima: '))
                if escolaridade == 1:
                    escolaridade = 'Fundamental'
                    try:
                        serie = input('Qual a turma(ex: 1 Para primeiro ano, 2 para segundo): ')
                        serie_validas = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

                    except ValueError as e:
                        print('Insira um número como série', e)
                        continue
                    if serie not in serie_validas:
                        print('Essa serie não existe, tente novamente.')
                        continue
                    try:
                        turma = input('Qual sala do aluno(ex: A, B, C): ')
                        turma_validas = ['A', 'B', 'C', 'D', 'E', 'F']
                    except ValueError as e:
                        print('Insira uma série valida', e)
                        if turma not in turma_validas:
                            print('Turma inexistente, tente novamente.')
                            continue
                            
                elif escolaridade == 2:
                    escolaridade = 'Médio'
                    try:
                        serie = input('Qual a turma(ex: 1 Para primeiro ano, 2 para segundo): ')
                        serie_validas = ['1', '2', '3']

                    except ValueError as e:
                        print('Insira um número como série', e)
                        continue
                    if serie not in serie_validas:
                        print('Essa serie não existe, tente novamente.')
                        continue
                    try:
                        turma = input('Qual sala do aluno(ex: A, B, C): ')
                        turma_validas = ['A', 'B', 'C', 'D', 'E', 'F']
                    except ValueError as e:
                        print('Insira uma série valida', e)
                        if turma not in turma_validas:
                            print('Turma inexistente, tente novamente.')
                            continue
                else:
                    print('Opção invalida, Tente novamente.')
                    continue
                
                
            
                id_novo = sistema.adicionar_aluno(nome, idade, escolaridade, serie, turma )
                print('Id gerado para esse aluno: ', id_novo)
                time.sleep(1)
                cont = input('Deseja continuar? S para sim E N para não: ').strip().upper()
                if cont == 'S':
                    time.sleep(1)
                    continue
                else:
                    break
        #Opção 2 - Listar alunos
        elif option == 2:
            banco = sqlite3.connect('database.db')
            cur = banco.cursor()
            serie = int(input('Qual serie você deseja listar:  '))
            turma = input('Qual a sala você deseja listar: ').strip().upper()
            colunas = ['Nome', 'Idade', 'escolaridade', 'Turma', 'Sala']
            
            alunos = sistema.busca_aluno(serie,turma)
            if not alunos:
                print('==========================')
                print('Turma vazia')
                print('==========================')
            else:
                print(tabulate.tabulate(sistema.busca_aluno(serie,turma), headers=colunas, tablefmt='grid'))  
            time.sleep(1)

            
        #Opção 3 - Selecionar aluno
        elif option == 3:
            banco = sqlite3.connect('database.db')
            cur = banco.cursor()
            alunoid = int(input('Qual o id do aluno: '))
            cur.execute('SELECT nome FROM Alunos WHERE id = ?', (alunoid,))
            aluno = cur.fetchone()
            if not aluno:
                print('Aluno não encontrado.')
            else:
                print(f'Aluno encontrado! {aluno[0]}')
                #Menu de alterar aluno
                while True:
                    print('1 - Alterar dados\n2 - Remover aluno\n0 - Voltar pro menu principal ')
                    opcao = int(input('Insira sua ação dadas as opções acima: '))
                    if opcao == 1: 
                        print('-------------------------------------')
                        print('O que você deseja alterar do aluno: ')
                        print('1 - Turma')
                        print('-----------------------------------')
                        oq = int(input('Qual sua ação: '))
                        if oq == 1:
                            cur.execute('SELECT turma FROM Alunos WHERE id = ?', (alunoid,))
                            sala_atual = cur.fetchone()
                            certeza = input(f'Certeza que deseja alterar a sala de {aluno[0]}?\nPara confirmar escreva o nome do aluno:  ')
                            if certeza == aluno[0]:
                                sala_validas = ['A', 'B', 'C', 'D', 'E', 'F']
                                print(f'Salas validas: {sala_validas}')
                                sala_nome = input('Qual a nova sala do aluno: ').strip().upper()
                                
                                
                                if sala_nome not in sala_validas:
                                    print('Sala invalida')
                                    continue
                                else:
                                    print(sistema.atualizador_turma(sala_nome, alunoid ))
                                print(f'Da sala {sala_atual[0]} para {sala_nome} ')

                    if opcao == 2:
                        certeza = input(f'Tem certeza que deseja deletar o aluno {aluno[0]}?\nSe sim escreva o nome do aluno abaixo:').strip().upper()
                        
                        if certeza == aluno[0].strip().upper():
                            sistema.apagador(alunoid)
                            print('Aluno removido com sucesso')
                            break
                        else:
                            print('Operação cancelada')

                    if opcao == 0:
                        break
                            
                            
        elif option == 9:
            print('Banco já foi configurado.')          

    
                    

                

        
            
            
