
# Gerenciador de Agenda para Barbearia

Este projeto é uma aplicação para gerenciar a agenda de uma barbearia, permitindo a criação, visualização e organização de compromissos.

## Pré-requisitos

- **Python**: Certifique-se de que você possui o Python instalado. Este projeto foi testado com Python 3.8 ou superior.

## Instalação

### Passo 1: Instalar o Python

1. Baixe o Python em [python.org](https://www.python.org/downloads/) e siga as instruções de instalação para o seu sistema operacional.
2. Para verificar a instalação, abra o terminal e digite:
   ```bash
   python --version
   ```
   ou, em alguns sistemas:
   ```bash
   python3 --version
   ```

### Passo 2: Clonar o Repositório

Clone este repositório para o seu ambiente local:
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### Passo 3: Configurar o Ambiente Virtual

Recomenda-se criar um ambiente virtual para gerenciar as dependências do projeto.

```bash
python -m venv venv
```

Ative o ambiente virtual:

- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **Linux/Mac**:
  ```bash
  source venv/bin/activate
  ```

### Passo 4: Instalar Dependências

As dependências do projeto estão listadas no arquivo `requirements.txt`. Para instalar todas as dependências, execute:

```bash
pip install -r requirements.txt
```

> Nota: O `requirements.txt` deve incluir as dependências principais, como `flask` e `sqlite3`.

## Banco de Dados SQLite

Este projeto usa o banco de dados SQLite para armazenar informações de compromissos e clientes. O SQLite é uma ótima opção para prototipagem e desenvolvimento local, pois é leve e não exige configuração de servidor.

### Inicializar o Banco de Dados

1. No diretório do projeto, crie o banco de dados SQLite:

   - Tem o arquivo barbershop.db que é a nossa base de dados.


2. Agora o banco de dados está pronto para uso e você pode iniciar a aplicação.

## Executar a Aplicação

Para rodar a aplicação, execute o arquivo principal (por exemplo, `app.py` ou `run.py`):

```bash
python app.py
```

A aplicação deve iniciar em `http://127.0.0.1:5000/`. A partir dessa URL, você pode acessar a interface da aplicação e gerenciar a agenda da barbearia.

## Estrutura do Projeto

```
.
├── app.py                   # Arquivo principal para iniciar a aplicação
├── requirements.txt         # Arquivo com as dependências do projeto
├── barbearia.db             # Banco de dados SQLite
└── README.md                # Este arquivo de documentação
```

## Licença

Este projeto é licenciado sob a licença MIT. Para mais detalhes, consulte o arquivo LICENSE.
