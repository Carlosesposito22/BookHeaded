# Contribuindo para o Projeto BookHeaded 🤝

Bem-vindo ao projeto BookHeaded! Obrigado por considerar contribuir para o nosso projeto! Siga as instruções abaixo para configurar o ambiente de desenvolvimento.

## Pré-requisitos

Antes de começar, certifique-se de ter o seguinte instalado na sua máquina:

- [Python](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [VScode](https://code.visualstudio.com/download)

## Passos para Configuração

### 1. Clone o Repositório

Abra seu terminal e navegue até o diretório onde deseja clonar o repositório. Em seguida, execute o comando abaixo:
```
git clone https://github.com/Carlosesposito22/BookHeaded.git
```

### 2. Navegue até o Diretório do Projeto
Use o comando
```
cd BookHeaded
```

### 3. Crie e Ative um Ambiente Virtual
Para criar um ambiente virtual, execute o seguinte comando:
```
python -m venv venv
```

Para ativar o ambiente virtual:

### No Windows:
```
source venv/Scripts/activate
```

### No macOS/Linux:
```
source venv/bin/activate
```

### 4. Instale as Dependências
Com o ambiente virtual ativado dentro da mesma pasta, instale as dependências necessárias:
```
pip install -r requirements.txt
```
### 5. Execute as migrações:
Realize as migrações no banco usando: 
(Note que em algums dispositivos é usado py como prefixo ao inves de python)
```
python manage.py migrate
```
### 6. Execute o Servidor de Desenvolvimento
Finalmente, para iniciar o servidor de desenvolvimento, execute:

```
python manage.py runserver
```

Agora, você deve ser capaz de acessar o aplicativo em seu navegador, normalmente o servidor local é http://localhost:8000/.

### 7. Contribuindo com Código

Recomendamos o uso do Visual Studio Code (VSCode) para desenvolver o projeto. Para abrir o projeto no VSCode, siga os passos abaixo:

# Abra o VSCode.
Clique em File > Open Folder... e selecione o diretório do projeto BookHeaded.
Certifique-se de que o ambiente virtual esteja ativado no terminal do VSCode.

# Abra um Pull Request.

### Processo de Revisão
Nossa equipe irá analisar todos os pull requests. Apenas aqueles que forem coerentes e estiverem alinhados com os objetivos do projeto serão aprovados.

# Dúvidas?
Se tiver qualquer dúvida, sinta-se à vontade para abrir uma issue.


## Diretrizes de Desenvolvimento 🤔

  - Para fazer uma boa contribuição siga as boas práticas de codificação em Python, HTML e CSS.
  - Formatação correta do código.
  - Ordem de imports correta no código.
