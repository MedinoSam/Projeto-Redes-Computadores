import sys
import socket
import threading
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit,
    QLineEdit, QPushButton, QVBoxLayout, QWidget,
    QDialog, QLabel, QHBoxLayout
)
from PySide6.QtCore import Signal, QObject


class MessageReceiver(QObject):
    message_received = Signal(str)

    def __init__(self, client_socket):
        super().__init__()
        self.client = client_socket
        self.running = True

    def start_listening(self):
        while self.running:
            try:
                msg = self.client.recv(2048).decode('utf-8')
                if msg:
                    self.message_received.emit(msg)
                else:
                    self.message_received.emit("Servidor desconectado.")
                    break
            except:
                self.message_received.emit("Erro na conexão com o servidor.")
                break


class UsernameDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Escolha seu nome de usuário")
        self.setFixedSize(300, 100)

        self.label = QLabel("Digite seu nome de usuário:")
        self.line_edit = QLineEdit()
        self.ok_button = QPushButton("OK")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

        self.ok_button.clicked.connect(self.accept)
        self.line_edit.returnPressed.connect(self.accept)

    def get_username(self):
        return self.line_edit.text().strip()


class ChatClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cliente Chat - PySide6")
        self.setGeometry(100, 100, 400, 300)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Digite uma mensagem...")
        self.send_button = QPushButton("Enviar")

        layout = QVBoxLayout()
        layout.addWidget(self.chat_display)
        layout.addWidget(self.input_field)
        layout.addWidget(self.send_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Janela para escolher username
        username_dialog = UsernameDialog()
        if username_dialog.exec() == QDialog.Accepted:
            username = username_dialog.get_username()
            if not username:
                username = "UsuarioQt"  # fallback
        else:
            sys.exit()  # Sai se não escolher usuário

        self.username = username

        # Conectar ao servidor
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect(('localhost', 8888))
            self.client.send(self.username.encode('utf-8'))
        except:
            self.chat_display.append("Não foi possível conectar ao servidor.")
            self.input_field.setEnabled(False)
            self.send_button.setEnabled(False)
            return

        # Conectar sinais e slots
        self.send_button.clicked.connect(self.send_message)
        self.input_field.returnPressed.connect(self.send_message)

        # Thread para receber mensagens
        self.receiver = MessageReceiver(self.client)
        self.receiver.message_received.connect(self.display_message)
        self.thread = threading.Thread(target=self.receiver.start_listening, daemon=True)
        self.thread.start()

    def send_message(self):
        msg = self.input_field.text()
        if msg:
            try:
                self.client.send(msg.encode('utf-8'))
                # Mostrar mensagem enviada na tela, com indicação de "Você"
                self.chat_display.append(f"<Você> {msg}")
                self.input_field.clear()
            except:
                self.chat_display.append("Falha ao enviar mensagem.")

    def display_message(self, msg):
        # Aqui, para evitar repetir mensagem própria (que já mostramos),
        # você pode querer filtrar mensagens que começam com "<username>"
        # e ignorar se for do próprio usuário, mas isso depende do formato do servidor.
        # Por ora, só exibe tudo normalmente:
        if not msg.startswith(f"<{self.username}>"):
            self.chat_display.append(msg)

    def closeEvent(self, event):
        try:
            self.receiver.running = False
            self.client.close()
        except:
            pass
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatClient()
    window.show()
    sys.exit(app.exec())
