import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

rodando = False
driver = None
arquivo_msg = None


# -------------------------
# selecionar txt
# -------------------------
def selecionar_arquivo():
    global arquivo_msg

    caminho = filedialog.askopenfilename(
        title="Selecionar arquivo TXT",
        filetypes=[("Arquivos TXT", "*.txt")]
    )

    if caminho:
        arquivo_msg = caminho
        label_arquivo.config(
            text=f"Arquivo: {os.path.basename(caminho)}"
        )


# -------------------------
# abrir whatsapp
# -------------------------
def abrir_whatsapp(numero):
    global driver

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install()
        ),
        options=options
    )

    link = f"https://web.whatsapp.com/send?phone={numero}"
    driver.get(link)

    label_status.config(
        text="Escaneie QR Code..."
    )

    time.sleep(20)


# -------------------------
# enviar mensagem
# -------------------------
def enviar_mensagem(msg):
    global driver

    try:
        caixa = driver.find_element(
            By.XPATH,
            '//div[@contenteditable="true"]'
        )

        caixa.click()
        caixa.send_keys(msg)
        caixa.send_keys(Keys.ENTER)

        return True

    except Exception as e:
        label_status.config(
            text=f"Erro: {e}"
        )
        return False


# -------------------------
# bot principal
# -------------------------
def bot():
    global rodando
    global arquivo_msg

    numero = entrada_numero.get().strip()
    delay = entrada_delay.get().strip()
    loop = loop_var.get()

    if not numero:
        messagebox.showerror(
            "Erro",
            "Digite o número"
        )
        return

    if not arquivo_msg:
        messagebox.showerror(
            "Erro",
            "Selecione um arquivo TXT"
        )
        return

    try:
        delay = float(delay)
    except:
        delay = 2

    try:
        with open(
            arquivo_msg,
            "r",
            encoding="utf-8"
        ) as f:
            mensagens = [
                linha.strip()
                for linha in f
                if linha.strip()
            ]
    except:
        messagebox.showerror(
            "Erro",
            "Falha ao abrir TXT"
        )
        return

    abrir_whatsapp(numero)

    label_status.config(
        text="Bot rodando..."
    )

    if loop:
        while rodando:
            for msg in mensagens:
                if not rodando:
                    break

                enviar_mensagem(msg)
                label_status.config(
                    text=f"Enviado: {msg}"
                )
                time.sleep(delay)

    else:
        for msg in mensagens:
            if not rodando:
                break

            enviar_mensagem(msg)
            label_status.config(
                text=f"Enviado: {msg}"
            )
            time.sleep(delay)

        label_status.config(
            text="Lista enviada com sucesso"
        )
        rodando = False


# -------------------------
# iniciar
# -------------------------
def iniciar():
    global rodando

    if not rodando:
        rodando = True
        threading.Thread(
            target=bot,
            daemon=True
        ).start()


# -------------------------
# parar
# -------------------------
def parar():
    global rodando
    global driver

    rodando = False

    if driver:
        try:
            driver.quit()
        except:
            pass

    label_status.config(
        text="Bot parado"
    )


# -------------------------
# interface
# -------------------------
janela = tk.Tk()
janela.title("Bot WhatsApp")
janela.geometry("450x400")


tk.Label(
    janela,
    text="Número com DDI + DDD"
).pack(pady=5)

entrada_numero = tk.Entry(janela)
entrada_numero.pack()


tk.Label(
    janela,
    text="Delay entre mensagens"
).pack(pady=5)

entrada_delay = tk.Entry(janela)
entrada_delay.insert(0, "2")
entrada_delay.pack()


loop_var = tk.BooleanVar()

tk.Checkbutton(
    janela,
    text="Loop infinito",
    variable=loop_var
).pack(pady=10)


tk.Button(
    janela,
    text="Selecionar TXT",
    command=selecionar_arquivo
).pack(pady=10)


label_arquivo = tk.Label(
    janela,
    text="Nenhum arquivo selecionado"
)
label_arquivo.pack()


tk.Button(
    janela,
    text="Iniciar Bot",
    command=iniciar,
    bg="green",
    fg="white"
).pack(pady=10)


tk.Button(
    janela,
    text="Parar Bot",
    command=parar,
    bg="red",
    fg="white"
).pack(pady=10)


label_status = tk.Label(
    janela,
    text="Aguardando..."
)
label_status.pack(pady=20)


janela.mainloop()