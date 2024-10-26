# Medicom Libras (Cartão Médico Virtual)


## Descrição

O **Medicom Libras** é uma aplicação web construída em Flask que permite gerar um cartão médico virtual com informações importantes, como tipo sanguíneo, histórico médico e alergias. O objetivo é auxiliar pessoas com deficiência auditiva, a transmitirem suas informações de saúde com maior facilidade, a fim de otimizar o atendimento médico, e melhorar a qualidade de comunicação em ambientes hospitalares.

## Funcionalidades
- Formulário para coleta de informações pessoais e médicas.
- Geração de um cartão médico virtual, com frente e verso.
- Download do cartão como imagem.
- Layout responsivo e moderno.
- Tradução automatica em libras.
- Qrcode vinculado ao usuário cadastrado.

## Executando o projeto


### Clone o repositório:

```bash
git clone https://github.com/seu_usuario/MedicomLibras.git
```

### Acesse o diretório do projeto:

```bash
cd MedicomLibras
```

### Execute o servidor Flask:

```bash
flask run
```

### Acesse a aplicação no navegador:

http://127.0.0.1:5000/


## Pré-requisitos

- Python 3.8 ou superior
- `pip` para gerenciar pacotes

## Dependências

Instale as dependências usando o comando abaixo:

```bash
pip install -r requirements.txt
```


## Estrutura do Projeto

```bash
MedicomLibras/
├── app.py                 # Arquivo principal da aplicação Flask
├── config.py              # Configurações da aplicação
├── instance/              # Diretório com a base de dados SQLite
│   └── users.db
├── static/                # Arquivos estáticos (imagens, CSS)
│   ├── background.png
│   ├── cartao-medico.png
│   ├── Logo.png
│   └── style.css
├── templates/             # Templates HTML
│   ├── card.html
│   ├── form.html
│   ├── login.html
│   ├── register.html
│   └── informative.html
├── requirements.txt       # Lista de dependências
└── README.md              # Arquivo README com instruções do projeto
```

# Screenshots

## Desktop

### Tela de Login
![Tela de Login](assets/screenshot_login.png)

### Tela de Cadastro
![Tela de Cadastro](assets/screenshot_register.png)

### Tela do Formulário Médico
![Tela do Formulário Médico](assets/screenshot_form.png)

### Tela Sobre o Projeto
![Tela Sobre o Projeto](assets/screenshot_sobre.png)

### Cartão Médico Virtual
![Cartão Médico Virtual](assets/screenshot_card.png)

## Smartphone

### Tela de Login
<img src="assets/login(iPhone12Pro).png" alt="Tela de Login" width="300"/>

### Tela de Cadastro
<img src="assets/register(iPhone12Pro).png" alt="Tela de Cadastro" width="300"/>

### Tela do Formulário Médico
<img src="assets/form(iPhone12Pro).png" alt="Tela do Formulário Médico" width="300"/>

### Tela Sobre o Projeto
<img src="assets/sobre(iPhone12Pro).png" alt="Tela Sobre o Projeto" width="300"/>

### Cartão Médico Virtual
<img src="assets/card(iPhone12Pro).png" alt="Cartão Médico Virtual" width="300"/>