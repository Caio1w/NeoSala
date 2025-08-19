import sqlite3, tabulate, time
import sistema
banco = sqlite3.connect('database.db')
while True:
    print('-------------------------------------------------')
    print('1 - Para adicionar aluno')
    print('2 - Para listar alunos ')
    print('3 - Para selecionar aluno')
    print('')
    print('0 - Para sair ')
    print('------------------------------------')
    option = int(input('Insira sua ação: '))
    

    if option == 1:
        while True:
            nome = input('Insira o nome do aluno:  ').strip()
            idade = int(input('Insira a idade do aluno: '))
            escolaridade = int(input('1 - Fundamental\n2 - Médio\nInsira a escolaridade dadas as opções acima: '))
            if escolaridade == 1:
                escolaridade = 'Fundamental'
            elif escolaridade == 2:
                escolaridade = 'Médio'
            else:
                print('Opção invalida, Tente novamente.')
                continue
            try:
                turma = input('Qual a turma(ex: 1 Para primeiro ano, 2 para segundo): ')
            except:
                print('Opção invalida, são somente aceitos numeros.')
            sala = input('Qual sala do aluno(ex: A, B, C): ')
            salas_valdas = ['A', 'B', 'C', 'D', 'E', 'F']
            if sala not in salas_valdas:
                print('Turma invalida, tente novamente')
                continue
            id_novo = sistema.adicionar_aluno(nome, idade, escolaridade, turma, sala )
            print('Id gerado para esse aluno: ', id_novo)
            time.sleep(1)
            cont = input('Deseja continuar? S para sim E N para não: ').strip().upper()
            if cont == 'S':
                time.sleep(1)
                continue
            else:
                break

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

        

    if option == 3:
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
                            
                            
                            

                    

                

        
            
            
