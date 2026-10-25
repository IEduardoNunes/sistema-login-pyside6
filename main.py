# TODO: Criar uma interface questionando se o usuário já possui uma conta;
# TODO: Caso possua, entrar na tela de login (usuário, senha e esqueceu a senha);
# TODO: Caso não possua, entrar em uma tela de cadastro (cadastrar o usuário e a senha) (caso o usuário já exista, a pessoa deverá escolher outro nome de usuário). Após isso, voltará direto para a tela de login;
# TODO: Caso o usuário não lembre a senha, deverá entrar em uma tela de redefinição de senha (deverá ser informado o usuário e a nova senha). Após isso, voltará direto para a tela de login.
# TODO: 4 interfaces: questionário; cadastro; login; redefinição de senha.



#Importando recursos
from PySide6.QtWidgets import QApplication, QTableWidgetItem
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice
import mysql.connector #importante instalar o driver de comunicação via cmd antes com o comando "pip install mysql-connector-python".

conexao = mysql.connector.connect( #Desse jeito nós realizamos a conexão do python com o mysql
    host = '127.0.0.1', #informando o número IP da máquina local
    user = 'dev', #Informando o usuário criado no mysql
    password = '123456', #Informando a senha cadastrada para o usuário
    database = 'DBlogin' #Informando qual será o banco de dados utilizado para conexão
)

def register_button(): #Ao clicar no botão 'não', irá abrir a tela de cadastro e fechar a tela de questionário.
    register.show()
    questionnaire.close()

def login_button(): #Ao clicar no botão 'sim', irá abrir a tela de login e fechar a tela de questionário.
    login.show()
    questionnaire.close()
    
def redefine_button():
    redefine.show()
    login.close()

def save_user(): #Função para a tela de cadastro
    user = register.txtUserRegister.text()
    password = register.txtPasswordRegister.text() #Armazena os dados do usuário nas variáveis
    
    if user != '' and password != '': #Faz com que o usuário tenha que informar um usuário e senha para conseguir se registrar.
        cursor = conexao.cursor()
        sql = 'select * from registers where user_login = %s'
        dados = (str(user),)
        cursor.execute(sql, dados)
        resultado = cursor.fetchall() #Seleciona os registros no banco de dados que já tenham um usuário igual cadastrado
        
        if len(resultado) == 0: #Caso não tenha nenhum usuário cadastrado com o mesmo nome, ele executa o código
            sql = 'insert into registers(user_login, password_login) values(%s,%s)'
            dados = (str(user), str(password))
            cursor.execute(sql, dados) #
            
            conexao.commit()
            
            register.txtUserRegister.setText('')
            register.txtPasswordRegister.setText('')
            login.show()
            
            register.close() #Basicamente, armazena os dados inseridos pelo usuário dentro do banco de dados. Também fecha a janela de cadastro e abre a janela de login.
        else: #O sistema impede um cadastro se o nome de usuário já tiver sido criado dentro do banco de dados, e realiza os seguintes processos:
            register.lblRegister.setText('Usuário já existente.')
            register.txtUserRegister.setText('')
            register.txtPasswordRegister.setText('')
    else: #Limpa os campos e escreve uma mensagem do erro ocorrido
        register.txtUserRegister.setText('')
        register.txtPasswordRegister.setText('')
        register.lblRegister.setText('Informe um usuário e senha.')

def login_user(): #Tela de login
    user = login.txtUserLogin.text()
    password = login.txtPasswordLogin.text() #Recebe os dados armazenados nos campos
    
    if user != '' and password != '': #Faz com que o usuário tenha que informar um usuário e senha para conseguir se registrar.
        cursor = conexao.cursor()
        sql = 'select password_login from registers where user_login = %s' #Seleciona a senha do usuário específico
        dados = (str(user),)
        cursor.execute(sql, dados)
        resultado = cursor.fetchone()
        if resultado and resultado[0] == password: #Caso a senha seja igual a senha cadastrada, o sistema irá executar
            inside.show()
            login.close()
        else: #Limpa os campos e escreve uma mensagem do erro ocorrido
            login.txtUserLogin.setText('')
            login.txtPasswordLogin.setText('')
            login.lblLogin.setText('Usuário ou senha incorreto.')
        
        
    else: #Limpa os campos e escreve uma mensagem do erro ocorrido
        login.txtUserLogin.setText('')
        login.txtPasswordLogin.setText('')
        login.lblLogin.setText('Informe um usuário e senha.')
    
def redefine_user(): #Tela de redefinição
    user = redefine.txtUserRedefine.text()
    password = redefine.txtPasswordRedefine.text() #Recebe os dados armazenados pelo usuário.
    
    if user != '' and password != '': #Faz com que o usuário tenha que informar um usuário e senha para conseguir se registrar.
        cursor = conexao.cursor()
        sql = 'update registers set password_login = %s where user_login = %s'
        dados = (str(password), str(user))
        cursor.execute(sql,dados) #Realizando a atualização da senha do usuário específico.
        if cursor.rowcount > 0: ##Indica quantas linhas foram modificadas/encontradas pelo update (caso tenha sido uma ou mais, realiza o processo do if, caso não, realiza o processo do else).
            conexao.commit()
            cursor.close()
        
            login.show()
            redefine.close()
            login.lblLogin.setText('Senha alterada.') #Mostrando a tela de login, fechando a de redefinição e informando na tela que a senha foi alterada.
        else: ##Limpa os campos da tela de redefinição e informa uma mensagem de usuário não existente.
            cursor.close()
            redefine.txtUserRedefine.setText('')
            redefine.txtPasswordRedefine.setText('')
            redefine.lblRedefine.setText('Usuário não existente.')
    else: #Limpa os campos e informa um mensagem de erro.
        redefine.txtUserRedefine.setText('')
        redefine.txtPasswordRedefine.setText('')
        redefine.lblRedefine.setText('Informe um usuário ou senha válidos.')


app = QApplication([])

loader = QUiLoader()

arquivo = QFile("questionario.ui") #Aqui informamos qual arquivo será aberto pelo python.
arquivo.open(QIODevice.ReadOnly)
questionnaire = loader.load(arquivo)
questionnaire.btnNot.clicked.connect(register_button) #Abrindo a função 'register_user' ao clicar no botão 'Não' da tela de questionário.
questionnaire.btnYes.clicked.connect(login_button) #Abrindo a funcão 'login_user' ao clicar no botão 'sim' da tela de questionário.
 
arquivo2 = QFile("cadastro.ui")
arquivo2.open(QIODevice.ReadOnly)
register = loader.load(arquivo2) #Essas 3 linhas definem qual arquivo será aberto quando o botão 'btnRelatorio' for clicado.
register.btnSave.clicked.connect(save_user) #Abrindo a função 'save_user' ao clicar no botão 'Salvar' dentro da tela de cadastro.

arquivo3 = QFile("login.ui")
arquivo3.open(QIODevice.ReadOnly)
login = loader.load(arquivo3)
login.btnEnter.clicked.connect(login_user)
login.btnForgot.clicked.connect(redefine_button)

arquivo4 = QFile("inside.ui")
arquivo4.open(QIODevice.ReadOnly)
inside = loader.load(arquivo4)

arquivo5 = QFile("redefinicao.ui")
arquivo5.open(QIODevice.ReadOnly)
redefine = loader.load(arquivo5)
redefine.btnRedefine.clicked.connect(redefine_user)

arquivo.close()
arquivo2.close()
arquivo3.close()
arquivo4.close()
arquivo5.close()

questionnaire.show()

app.exec()
'''O código acima puxa os recursos de inicialização da 
Criada com o pyside6 e executa o arquivo, fazendo a
interface gráfica ser aberta na tela do usuário'''

