# Sistema de Login e Cadastro

Aplicação desktop em Python, com interface gráfica em PySide6 e banco de dados MySQL, que controla o acesso de usuários: cadastro, login e redefinição de senha.

## Funcionalidades
- Tela inicial que pergunta se o usuário já possui conta
- Cadastro de usuário e senha, com bloqueio de nomes de usuário repetidos
- Login com validação das credenciais no banco de dados
- Redefinição de senha informando o usuário e a nova senha
- Mensagens de erro na própria tela: campos vazios, usuário já existente, usuário inexistente e credenciais incorretas
- Área interna liberada somente após o login

## Fluxo das telas
```
Questionário
 ├─ "Sim" ─► Login ─► Área interna
 │             └─ "Esqueci a senha" ─► Redefinição ─► Login
 └─ "Não" ─► Cadastro ─► Login
```

## Tecnologias
Python · PySide6 (Qt) · MySQL · mysql-connector-python

## Banco de dados
Banco `DBlogin`, com a tabela `registers`:

```sql
CREATE DATABASE IF NOT EXISTS DBlogin;
USE DBlogin;

CREATE TABLE IF NOT EXISTS registers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_login VARCHAR(50) NOT NULL UNIQUE,
    password_login VARCHAR(255) NOT NULL
);
```
O script está em `database/DBlogin.sql`.

## Como executar
1. Clone o repositório
   ```bash
   git clone https://github.com/SEU-USUARIO/sistema-login-pyside6.git
   cd sistema-login-pyside6
   ```
2. Instale as dependências
   ```bash
   pip install -r requirements.txt
   ```
3. No MySQL, execute o script `database/DBlogin.sql`
4. Copie `.env.example` para `.env` e preencha com os dados do seu MySQL
5. Execute
   ```bash
   python main.py
   ```

## Autor
Eduardo Nunes dos S. Silva · [LinkedIn](https://www.linkedin.com/in/eduardo-nunes-dos-s-silva-18a321230) · [Portfólio](https://portfolio-eduardonunes.netlify.app)
