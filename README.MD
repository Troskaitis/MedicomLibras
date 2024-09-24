# Cartão Médico Virtual

Esta aplicação web em Python permite o cadastro de informações médicas básicas de pacientes com deficiência auditiva, ele gera um cartão médico virtual, que pode ser usado para facilitar o atendimento médico dessas pessoas. O cartão contém informações como tipo sanguíneo, medicamentos controlados, histórico cirúrgico, doenças crônicas, e alergias, em um formato visual similar a um cartão de saúde.

## Estrutura do Projeto
A aplicação é desenvolvida com Flask e contém as seguintes funcionalidades:

1. Formulário de Cadastro de Informações Médicas
Na primeira etapa, o usuário preenche um formulário com as seguintes informações:
Nome
Data de Nascimento
Tipo Sanguíneo
Medicamentos controlados
Histórico de cirurgias
Doenças na família
Alergias (a medicamentos ou outras)
Doenças crônicas
Essas informações são então enviadas para a segunda etapa, onde o cartão virtual é gerado.

2. Cartão Médico Virtual
Após o envio das informações, um cartão médico virtual é gerado e exibido na tela. Este cartão possui o seguinte layout:
Nome do paciente
Tipo sanguíneo
Data de nascimento
Medicamentos controlados
Histórico cirúrgico
Doenças crônicas e outras informações relevantes
O design do cartão simula um cartão físico com um layout responsivo.
Tecnologias Utilizadas
Python: Linguagem de programação usada para desenvolver a aplicação.
Flask: Micro-framework utilizado para construir a aplicação web.
HTML/CSS: Utilizados para estruturar e estilizar o formulário e o cartão virtual.
Bootstrap: Framework de CSS usado para responsividade e design.
Jinja2: Template engine do Flask para renderização dinâmica de dados no HTML.
Como Rodar o Projeto
Pré-requisitos
Python 3.x instalado.
Virtualenv (opcional, mas recomendado para isolar dependências).

## Instalação

Clone o repositório para sua máquina local:
```bash
git clone https://github.com/seu-usuario/cartao-medico-virtual.git
```

Entre no diretório do projeto:
```bash
cd cartao-medico-virtual
```

Crie um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
```

Ative o ambiente virtual:

No Windows:
```bash
venv\Scripts\activate
```
No Linux/macOS:
```bash
source venv/bin/activate
```
## Instale as dependências:

```bash
pip install -r requirements.txt
```

Executando a Aplicação
Após instalar as dependências, inicie o servidor Flask:

```bash
flask run
```

Acesse a aplicação no seu navegador pelo endereço:

arduino
http://127.0.0.1:5000
Estrutura de Diretórios
A estrutura do projeto é organizada da seguinte forma:

csharp
cartao-medico-virtual/
│
├── app.py                   # Arquivo principal da aplicação Flask
├── templates/                # Pasta contendo os templates HTML
│   ├── index.html            # Página inicial do formulário de cadastro
│   ├── card.html             # Página do cartão médico virtual
│
├── static/                   # Arquivos estáticos (CSS, imagens, etc.)
│   └── style.css             # Arquivo de estilização customizada (opcional)
│
├── README.md                 # Este arquivo README
├── requirements.txt          # Dependências da aplicação
└── venv/                     # Ambiente virtual (opcional)

## Funcionalidades Futuras
Inserção dos campos para dados pessoais, e melhoria das informções médicas.
Frente e verso do cartão virtual.
Autenticação e segurança para proteger as informações sensíveis do usuário.
armazenamento dos dados em arquivo .BD
