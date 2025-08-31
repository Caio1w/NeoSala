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
    banco.close
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
                    b1 REAL,
                    b2 REAL,
                    b3 REAL,
                    b4 REAL,
                    serie INTEGER NOT NULL,
                    turma TEXT NOT NULL,
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
                try:
                    idade = int(input('Insira a idade do aluno: '))
                except:
                    print('Apenas são aceitos numeros.')
                    continue
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
                        turma = input('Qual sala do aluno(ex: A, B, C): ').split().upper()
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
                    print('1 - Alterar dados\n2 - Remover aluno\n3 - Seção de notas\n0 - Voltar pro menu principal ')
                    opcao = int(input('Insira sua ação dadas as opções acima: '))
                    if opcao == 1: 
                        print('-------------------------------------')
                        print('O que você deseja alterar do aluno: ')
                        print('1 - Turma')
                        print('-----------------------------------')
                        oq = int(input('Qual sua ação: '))
                        if oq == 1:
                            cur.execute('SELECT turma FROM Alunos WHERE id = ?', (alunoid,))
                            turma_atual = cur.fetchone()
                            certeza = input(f'Certeza que deseja alterar a sala de {aluno[0]}?\nPara confirmar escreva o nome do aluno:  ')
                            if certeza == aluno[0]:
                                turma_validas = ['A', 'B', 'C', 'D', 'E', 'F']
                                print(f'Salas validas: {turma_validas}')
                                turma_nova = input('Qual a nova sala do aluno: ').strip().upper()
                                
                                
                                if turma_nova not in turma_validas:
                                    print('Sala invalida')
                                    continue
                                else:
                                    print(sistema.atualizador_turma(turma_nova, alunoid ))
                                print(f'Da sala {turma_atual[0]} para {turma_nova} ')

                    if opcao == 2:
                        certeza = input(f'Tem certeza que deseja deletar o aluno {aluno[0]}?\nSe sim escreva o nome do aluno abaixo:').strip().upper()
                        
                        if certeza == aluno[0].strip().upper():
                            sistema.apagador(alunoid)
                            print('Aluno removido com sucesso')
                            
                        else:
                            print('Operação cancelada')
                    if opcao == 3:
                        while True:
                            print('---Seção de notas---')
                            print('1 - Para atribuir nota')
                            print('2 - Visualizar notas')
                            print('3 - Alterar notas')
                            print('0 - Voltar')
                            print(f'Aluno selecionado : {aluno[0]}')
                            opcao_notas = int(input('Seleciona uma ação acima: '))
                            # atribuidor de notas
                            if opcao_notas == 1:
                                cur.execute('SELECT id FROM Notas WHERE aluno_id = ?', (alunoid,))
                                resultado = cur.fetchone()
                                if resultado:
                                    print('Nota já existente')
                                    continue
                                else:
                                    cur.execute('SELECT serie, turma FROM Alunos  WHERE id = ?', (alunoid,))
                                    serie_e_turma_cru = cur.fetchone()
                                    seriedoaluno = serie_e_turma_cru[0]
                                    trmaluno = serie_e_turma_cru[1]
                                    print("Deixe vazio caso ainda não haja nota para o bimestre")
                                    entradab1 = input("Insira a nota para o primeiro bimestre: ")

                                    if entradab1.strip() == "":
                                        b1 = None  
                                    else:
                                        try:
                                            b1 = round(float(entradab1), 1)
                                            if b1 > 10:
                                                print('Notas maiores que 10 não são permitidas.')
                                                continue
                                        except ValueError:
                                            print("Apenas são aceitos números")
                                            continue
                                    entradab2 = input("Insira a nota para o segundo bimestre: ")
                                    if entradab2.strip() == "":

                                        b2 = None 
                
                                    else:
                                        try:
                                            b2 = round(float(entradab2), 1)
                                            if b2 > 10:
                                                print('Notas maiores que 10 não são permitadas')
                                                continue
                                        except ValueError:
                                            print("Apenas são aceitos números")
                                            continue
                                    entradab3 = input("Insira a nota para o terceiro bimestre: ")
                                    if entradab3.strip() == "":

                                        b3 = None 
                
                                    else:
                                        try:
                                            b3 = round(float(entradab3), 1)
                                            if b3 > 10:
                                                print('Notas maiores que 10 não são permitadas')
                                                continue
                                        except ValueError:
                                            print("Apenas são aceitos números")
                                            continue
                                    entradab4 = input("Insira a nota para o quarto bimestre: ")
                                    if entradab4.strip() == "":

                                        b4 = None 
                
                                    else:
                                        try:
                                            b4 = round(float(entradab4), 1)
                                            if b4 > 10:
                                                print('Notas maiores que 10 não são permitadas')
                                                continue
                                        except ValueError:
                                            print("Apenas são aceitos números")
                                            continue
                                    print(sistema.ad_nota(alunoid, b1, b2, b3, b4, seriedoaluno, trmaluno))
                            #Visualizar as notas
                            if opcao_notas == 2:
                                notas = sistema.listar_notas(alunoid)
                                pos = 0
                                bi = 1
                                if notas:
                                    for nota in notas:
                                        print(f'Nota do bimestre {bi}: {notas[pos]}')

                                        pos += 1
                                        bi += 1
                                else:
                                    print('Notas não registradas.')
                            if opcao_notas == 3:
                                entradab1 = input("Insira a nota para o primeiro bimestre: ")

                                if entradab1.strip() == "":
                                    b1 = None  
                                else:
                                    try:
                                        b1 = round(float(entradab1), 1)
                                        if b1 > 10:
                                            print('Notas maiores que 10 não são permitidas.')
                                            continue
                                    except ValueError:
                                        print("Apenas são aceitos números")
                                        continue
                                entradab2 = input("Insira a nota para o segundo bimestre: ")
                                if entradab2.strip() == "":

                                    b2 = None 
            
                                else:
                                    try:
                                        b2 = round(float(entradab2), 1)
                                        if b2 > 10:
                                            print('Notas maiores que 10 não são permitadas')
                                            continue
                                    except ValueError:
                                        print("Apenas são aceitos números")
                                        continue
                                entradab3 = input("Insira a nota para o terceiro bimestre: ")
                                if entradab3.strip() == "":

                                    b3 = None 
            
                                else:
                                    try:
                                        b3 = round(float(entradab3), 1)
                                        if b3 > 10:
                                            print('Notas maiores que 10 não são permitadas')
                                            continue
                                    except ValueError:
                                        print("Apenas são aceitos números")
                                        continue
                                entradab4 = input("Insira a nota para o quarto bimestre: ")
                                if entradab4.strip() == "":

                                    b4 = None 
            
                                else:
                                    try:
                                        b4 = round(float(entradab4), 1)
                                        if b4 > 10:
                                            print('Notas maiores que 10 não são permitadas')
                                            continue
                                    except ValueError:
                                        print("Apenas são aceitos números")
                                        continue
                                print(sistema.alt_nota(alunoid,b1,b2,b3,b4))
                            if opcao_notas == 0:
                                break
                    if opcao == 0:
                        break
                            
                            
        elif option == 9:
            print('Banco já foi configurado.')          

    
                    

                

        
            
            
