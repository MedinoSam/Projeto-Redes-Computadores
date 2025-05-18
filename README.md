# 💬 Projeto de Chat com Sockets e Interface Qt

Este projeto implementa um sistema de chat com servidor e múltiplos clientes utilizando `socket` e `threading` em Python. A interface gráfica foi construída com **PySide6 (Qt)**. Os usuários podem se conectar, enviar e receber mensagens em tempo real.

## 📁 Estrutura do Projeto

```
Projeto-Redes-Computadores/
├── servidor/
│   └── servidor.py
├── cliente_window/
│   └── cliente_window.py
└── README.md
```

---

## ⚙️ Requisitos

- Python 3.10 ou superior
- Pip
- PySide6

---

## 🖥️ Execução no Linux (WSL / Ubuntu)

### 1. Instale dependências:

```bash
sudo apt update
sudo apt install python3 python3-pip -y
pip install PySide6
```

### 2. (Opcional) Instale bibliotecas gráficas adicionais:

```bash
sudo apt install libxkbcommon0 libxkbcommon-x11-0 libxcb-xinerama0 libegl1 libxcb-cursor0 -y
```

> ⚠️ Se estiver usando WSL, é necessário ter um **servidor gráfico** rodando (como [VcXsrv](https://sourceforge.net/projects/vcxsrv/) no Windows) e definir a variável `DISPLAY`:
```bash
export DISPLAY=:0
```

### 3. Rode o servidor:

```bash
cd servidor
python3 servidor.py
```

### 4. Rode o cliente com interface:

```bash
cd ../cliente_window
python3 cliente_window.py
```

---

## 🪟 Execução no Windows (CMD / PowerShell / PyCharm)

### 1. Instale o Python e o pip

Baixe o Python pelo site oficial: https://www.python.org/downloads/  
Certifique-se de marcar a opção **"Add Python to PATH"**.

### 2. Instale o PySide6

```bash
pip install PySide6
```

### 3. Execute o servidor:

```bash
cd servidor
python servidor.py
```

### 4. Em outro terminal, execute o cliente:

```bash
cd cliente_window
python cliente_window.py
```

---

## 💡 Funcionalidades

- Conexão de múltiplos clientes simultaneamente
- Interface gráfica para envio e recebimento de mensagens
- Notificação de entrada e saída de usuários
- Comando `/lista` para listar usuários conectados
- Comando `/sair` para encerrar o cliente
- Comando `/parar` no servidor para encerramento geral

---

## 👥 Autores

- [Seu Nome]
- [Nome dos colegas da equipe]

---

## 📝 Licença

Projeto desenvolvido como parte da disciplina **Redes de Computadores - UFAL**.
