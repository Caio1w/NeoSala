import sqlite3, tabulate, time
import sistema

banco_configurado = False
try:
    with sqlite3.connect('database.db') as banco:
        cur = banco.cursor()
        cur.execute(
            'INSERT INTO Alunos (nome, idade, escolaridade, serie, turma) VALUES (?, ?, ?, ?, ?)',
            ('teste', 1, 'teste', 'teste', 'teste')
        )
        print("Banco configurado!")
        cur.execute("DELETE FROM Alunos WHERE escolaridade = ?", ("teste",))
        banco_configurado = True

except Exception as e:
    print("Banco de dados desconfigurado, crie a database nas opções abaixo.", e)
    banco_configurado = False


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
    if option == 9 and banco_configurado == False:
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
        CREATE TABLE IF NOT EXISTS notas_fundamental (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    aluno_id INTEGER NOT NULL,
                    portugues REAL,
                    matematica REAL,
                    ciencias REAL,
                    historia REAL,
                    geografia REAL,
                    bimestre INTEGER NOT NULL,
                    serie INTEGER NOT NULL,
                    turma TEXT NOT NULL,
                    FOREIGN KEY (aluno_id) REFERENCES Alunos (id)
                        ON DELETE CASCADE ON UPDATE NO ACTION);""")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS notas_medio (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    aluno_id INTEGER NOT NULL,
                    portugues REAL,
                    matematica REAL,
                    biologia REAL,
                    quimica REAL,
                    fisica REAL,
                    historia REAL,
                    geografia REAL,
                    ingles REAL,
                    bimestre INTEGER NOT NULL,
                    serie INTEGER NOT NULL,
                    turma TEXT NOT NULL,
                    FOREIGN KEY (aluno_id) REFERENCES Alunos (id)
                        ON DELETE CASCADE ON UPDATE NO ACTION);""")
        
        print('Database criada com sucesso, prossiga.')
        banco_configurado = True
    #Aqui é pra sair independemente se o banco ta configurado ou não
    elif option == 0:
        print('Até a proxima!')
        break
    #Aqui é quando o usuario tenta fazer alguma ação com o banco desconfigurado
    elif banco_configurado == False:
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
                        turma = input('Qual a turma do aluno(ex: A, B, C): ').strip().upper()
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
                                bimestre_validas = ['1', '2', '3', '4']
                                qualbimestre = input('Para qual bimestre você deseja atribuir a nota (1, 2, 3 ou 4): ')
                                if qualbimestre not in bimestre_validas:
                                    print('Bimestre invalido, tente novamente.')
                                    continue
                                bi = int(qualbimestre)
                                cur.execute('SELECT id FROM notas_fundamental WHERE aluno_id = ? AND bimestre = ?', (alunoid, bi))
                                resultado = cur.fetchone()
                                if resultado:
                                    print('Nota já existente')
                                    continue
                                else:
                                    cur.execute('SELECT serie, turma FROM Alunos  WHERE id = ?', (alunoid,))
                                    serie_e_turma_cru = cur.fetchone()
                                    seriedoaluno = serie_e_turma_cru[0]
                                    trmaluno = serie_e_turma_cru[1]
                                    escolaridade_valida = ['Fundamental', 'Médio']
                                    cur.execute('SELECT escolaridade FROM Alunos WHERE id = ?', (alunoid,))
                                    escolaridade = cur.fetchone()[0]
                                    if escolaridade not in escolaridade_valida:
                                        print('Escolaridade invalida, tente novamente.')
                                        continue
                                    if escolaridade == 'Fundamental':
                                        
                                    

                                        print("Deixe vazio caso ainda não haja nota para o bimestre")
                                        entradapor_fund = input("Insira a nota para a materia de portugues: ")

                                        if entradapor_fund.strip() == "":
                                            notportugues_fund = None  
                                        else:
                                            try:
                                                notportugues_fund = round(float(entradapor_fund), 1)
                                                if notportugues_fund > 10:
                                                    print('Notas maiores que 10 não são permitidas.')
                                                    continue
                                            except ValueError:
                                                print("Apenas são aceitos números")
                                                continue
                                        entradamat_fund = input("Insira a nota para a materia de matematica: ")
                                        if entradamat_fund.strip() == "":

                                            notmat_fund = None 
                    
                                        else:
                                            try:
                                                notmat_fund = round(float(entradamat_fund), 1)
                                                if notmat_fund > 10:
                                                    print('Notas maiores que 10 não são permitadas')
                                                    continue
                                            except ValueError:
                                                print("Apenas são aceitos números")
                                                continue
                                        entranotcie_fund = input("Insira a nota para a materia de ciencias: ")
                                        if entranotcie_fund.strip() == "":

                                            notcie_fund = None 
                    
                                        else:
                                            try:
                                                notcie_fund = round(float(entranotcie_fund), 1)
                                                if notcie_fund > 10:
                                                    print('Notas maiores que 10 não são permitadas')
                                                    continue
                                            except ValueError:
                                                print("Apenas são aceitos números")
                                                continue
                                        entradahis_fun = input("Insira a nota para a materia de historia: ")
                                        if entradahis_fun.strip() == "":

                                            nothis_fun = None
                                        else:
                                            try:
                                                nothis_fun = round(float(entradahis_fun), 1)
                                                if nothis_fun > 10:
                                                    print('Notas maiores que 10 não são permitadas')
                                                    continue
                                            except ValueError:
                                                print("Apenas são aceitos números")
                                                continue
                                        entradageo_fun = input("Insira a nota para a materia de geografia: ")
                                        if entradageo_fun.strip() == "":
                                            
                                            notgeo_fun = None
                                        else:
                                            try:
                                                notgeo_fun = round(float(entradageo_fun), 1)
                                                if notgeo_fun > 10:
                                                    print('Notas maiores que 10 não são permitadas')
                                                    continue
                                            except ValueError:
                                                print("Apenas são aceitos números")
                                                continue

                                    
                                        print(sistema.ad_nota_fundamental(alunoid, notportugues_fund, notmat_fund, notcie_fund, nothis_fun, notgeo_fun, bi, seriedoaluno, trmaluno))
                                    if escolaridade == 'Médio':
                                        print("Deixe vazio caso ainda não haja nota para o bimestre")
                                        entradapor_medio = input("Insira a nota para a materia de portugues: ")

                                        if entradapor_medio.strip() == "":
                                            notportugues_medio = None  
                                        else:
                                            try:
                                                notportugues_medio = round(float(entradapor_medio), 1)
                                                if notportugues_medio > 10:
                                                    print('Notas maiores que 10 não são permitidas.')
                                                    continue
                                            except ValueError:
                                                print("Apenas são aceitos números")
                                                continue
                                        entradamat_medio = input("Insira a nota para a materia de matematica: ")
                                        if entradamat_medio.strip() == "":

                                            notmat_medio = None 
                    
                                        else:
                                            try:
                                                notmat_medio = round(float(entradamat_medio), 1)
                                                if notmat_medio > 10:
                                                    print('Notas maiores que 10 não são permitadas')
                                                    continue
                                            except ValueError:
                                                print("Apenas são aceitos números")
                                                continue
                                        entranotbio_medio = input("Insira a nota para a materia de biologia: ")
                                        if entranotbio_medio.strip() == "":

                                            notbio_medio = None 
                    
                                        else:
                                            try:
                                                notbio_medio = round(float(entranotbio_medio), 1)
                                                if notbio_medio > 10:
                                                    print('Notas maiores que 10 não são permitadas')
                                                    continue
                                            except ValueError:
                                                print("Apenas são aceitos números")
                                                continue
                                        entranoqim_medio = input("Insira a nota para a materia de quimica: ")
                                        if entranoqim_medio.strip() == "":

                                            notqim_medio = None
                                        else:
                                            try:
                                                notqim_medio = round(float(entranoqim_medio), 1)
                                                if notqim_medio > 10:
                                                    print('Notas maiores que 10 não são permitadas')
                                                    continue
                                            except ValueError:
                                                print("Apenas são aceitos números")
                                                continue
                                        entradafis_medio = input("Insira a nota para a materia de fisica: ")
                                        if entradafis_medio.strip() == "":
                                            
                                            notfis_medio = None
                                        else:
                                            try:
                                                notfis_medio = round(float(entradafis_medio), 1)
                                                if notfis_medio > 10:
                                                    print('Notas maiores que 10 não são permitadas')
                                                    continue
                                            except ValueError:
                                                print("Apenas são aceitos números")
                                                continue
                                        entradahis_medio = input("Insira a nota para a materia de historia: ")
                                        if entradahis_medio.strip() == "":
                                            
                                            nothis_medio = None
                                        else:
                                            try:
                                                nothis_medio = round(float(entradahis_medio), 1)
                                                if nothis_medio > 10:
                                                    print('Notas maiores que 10 não são permitadas')
                                                    continue
                                            except ValueError:
                                                print("Apenas são aceitos números")
                                                continue
                                        entradageo_medio = input("Insira a nota para a materia de geografia: ")
                                        if entradageo_medio.strip() == "":
                                            
                                            notgeo_medio = None
                                        else:
                                            try:
                                                notgeo_medio = round(float(entradageo_medio), 1)
                                                if notgeo_medio > 10:
                                                    print('Notas maiores que 10 não são permitadas')
                                                    continue
                                            except ValueError:
                                                print("Apenas são aceitos números")
                                                continue
                                        entradaing_medio = input("Insira a nota para a materia de ingles: ")
                                        if entradaing_medio.strip() == "":
                                            
                                            noting_medio = None
                                        else:
                                            try:
                                                noting_medio = round(float(entradaing_medio), 1)
                                                if noting_medio > 10:
                                                    print('Notas maiores que 10 não são permitadas')
                                                    continue
                                            except ValueError:
                                                print("Apenas são aceitos números")
                                                continue
                                        print(sistema.ad_nota_medio(alunoid, notportugues_medio, notmat_medio, notbio_medio, notqim_medio, notfis_medio, nothis_medio, notgeo_medio, noting_medio, bi, seriedoaluno, trmaluno))
                            #Visualizar as notas
                            if opcao_notas == 2:
                                qualbimestre = input('Para qual bimestre você deseja ver a nota (1, 2, 3 ou 4): ')
                                if qualbimestre not in ['1', '2', '3', '4']:
                                    print('Bimestre invalido, tente novamente.')
                                    continue
                                bi = int(qualbimestre)

                                notas = sistema.listar_notas(alunoid, bi)
                                pos = 0
                                bi = 1
                                if notas:
                                    for nota in notas:
                                        print(f'Nota do bimestre {bi}: {notas[pos]}')

                                        pos += 1
                                        bi += 1
                                else:
                                    print('Notas não registradas.')
                            #Alterar notas
                            if opcao_notas == 3:
                                cur.execute('SELECT escolaridade FROM Alunos WHERE id = ?', (alunoid,))
                                escolaridade = cur.fetchone()[0]
                                if escolaridade == 'Fundamental':
                                    print('Deixe vazio caso não queira alterar a nota')
                                    entradapor_fund = input("Insira a nova nota para a materia de portugues: ")

                                    if entradapor_fund.strip() == "":
                                        notportugues_fund = None  
                                    else:
                                        try:
                                            notportugues_fund = round(float(entradapor_fund), 1)
                                            if notportugues_fund > 10:
                                                print('Notas maiores que 10 não são permitidas.')
                                                continue
                                        except ValueError:
                                            print("Apenas são aceitos números")
                                            continue
                                    entradamat_fund = input("Insira a nova nota para a materia de matematica: ")
                                    if entradamat_fund.strip() == "":

                                        notmat_fund = None 
                
                                    else:
                                        try:
                                            notmat_fund = round(float(entradamat_fund), 1)
                                            if notmat_fund > 10:
                                                print('Notas maiores que 10 não são permitadas')
                                                continue
                                        except ValueError:
                                            print("Apenas são aceitos números")
                                            continue
                                    entranotcie_fund = input("Insira a nova nota para a materia de ciencias: ")
                                    if entranotcie_fund.strip() == "":

                                        notcie_fund = None 
                
                                    else:
                                        try:
                                            notcie_fund = round(float(entranotcie_fund), 1)
                                            if notcie_fund > 10:
                                                print('Notas maiores que 10 não são permitadas')
                                                continue
                                        except ValueError:
                                            print("Apenas são aceitos números")
                                            continue
                                    entradahis_fun = input("Insira a nova nota para a materia de historia: ")
                                    if entradahis_fun.strip() == "":

                                        nothis_fun = None
                                    else:
                                        try:
                                            nothis_fun = round(float(entradahis_fun), 1)
                                            if nothis_fun > 10:
                                                print('Notas maiores que 10 não são permitadas')
                                                continue
                                        except ValueError:
                                            print("Apenas são aceitos números")
                                            continue
                                    entradageo_fun = input("Insira a nova nota para a materia de geografia: ")
                                    if entradageo_fun.strip() == "":
                                        
                                        notgeo_fun = None
                                    else:
                                        try:
                                            notgeo_fun = round(float(entradageo_fun), 1)
                                            if notgeo_fun > 10:
                                                print('Notas maiores que 10 não são permitadas')
                                                continue
                                        except ValueError:
                                            print("Apenas são aceitos números")
                                            continue
                                    print(sistema.alt_nota_fundamental(alunoid, notportugues_fund, notmat_fund, notcie_fund, nothis_fun, notgeo_fun))
                                if escolaridade == 'Médio':
                                    print('Deixe vazio caso não queira alterar a nota')
                                    entradapor_medio = input("Insira a nova nota para a materia de portugues: ")

                                    if entradapor_medio.strip() == "":
                                        notportugues_medio = None  
                                    else:
                                        try:
                                            notportugues_medio = round(float(entradapor_medio), 1)
                                            if notportugues_medio > 10:
                                                print('Notas maiores que 10 não são permitidas.')
                                                continue
                                        except ValueError:
                                            print("Apenas são aceitos números")
                                            continue
                                    entradamat_medio = input("Insira a nova nota para a materia de matematica: ")
                                    if entradamat_medio.strip() == "":

                                        notmat_medio = None 
                
                                    else:
                                        try:
                                            notmat_medio = round(float(entradamat_medio), 1)
                                            if notmat_medio > 10:
                                                print('Notas maiores que 10 não são permitadas')
                                                continue
                                        except ValueError:
                                            print("Apenas são aceitos números")
                                            continue
                                    entranotbio_medio = input("Insira a nova nota para a materia de biologia: ")
                                    if entranotbio_medio.strip() == "":

                                        notbio_medio = None 
                
                                    else:
                                        try:
                                            notbio_medio = round(float(entranotbio_medio), 1)
                                            if notbio_medio > 10:
                                                print('Notas maiores que 10 não são permitadas')
                                                continue
                                        except ValueError:
                                            print("Apenas são aceitos números")
                                            continue
                                    entranoqim_medio = input("Insira a nova nota para a materia de quimica: ")
                                    if entranoqim_medio.strip() == "":

                                        notqim_medio = None
                                    else:
                                        try:
                                            notqim_medio = round(float(entranoqim_medio), 1)
                                            if notqim_medio > 10:
                                                print('Notas maiores que 10 não são permitadas')
                                                continue
                                        except ValueError:
                                            print("Apenas são aceitos números")
                                            continue
                                    entradafis_medio = input("Insira a nova nota para a materia de fisica: ")
                                    if entradafis_medio.strip() == "":
                                        
                                        notfis_medio = None
                                    else:
                                        try:
                                            notfis_medio = round(float(entradafis_medio), 1)
                                            if notfis_medio > 10:
                                                print('Notas maiores que 10 não são permitadas')
                                                continue
                                        except ValueError:
                                            print("Apenas são aceitos números")
                                            continue
                                    entradahis_medio = input("Insira a nova nota para a materia de historia: ")
                                    if entradahis_medio.strip() == "":
                                        
                                        nothis_medio = None
                                    else:
                                        try:
                                            nothis_medio = round(float(entradahis_medio), 1)
                                            if nothis_medio > 10:
                                                print('Notas maiores que 10 não são permitadas')
                                                continue
                                        except ValueError:
                                            print("Apenas são aceitos números")
                                            continue
                                    entradageo_medio = input("Insira a nova nota para a materia de geografia: ")
                                    if entradageo_medio.strip() == "":
                                        
                                        notgeo_medio = None
                                    else:
                                        try:
                                            notgeo_medio = round(float(entradageo_medio), 1)
                                            if notgeo_medio > 10:
                                                print('Notas maiores que 10 não são permitadas')
                                                continue
                                        except ValueError:
                                            print("Apenas são aceitos números")
                                            continue
                                    entradaing_medio = input("Insira a nova nota para a materia de ingles: ")
                                    if entradaing_medio.strip() == "":
                                        
                                        noting_medio = None
                                    else:
                                        try:
                                            noting_medio = round(float(entradaing_medio), 1)
                                            if noting_medio > 10:
                                                print('Notas maiores que 10 não são permitadas')
                                                continue
                                        except ValueError:
                                            print("Apenas são aceitos números")
                                            continue
                                    print(sistema.alt_nota_medio(alunoid, notportugues_medio, notmat_medio, notbio_medio, notqim_medio, notfis_medio, nothis_medio, notgeo_medio, noting_medio))
                            if opcao_notas == 0:
                                break
                    if opcao == 0:
                        break
                            
                            
        elif option == 9:
            print('Banco já foi configurado.')          

    
                    