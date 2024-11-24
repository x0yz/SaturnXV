import customtkinter as ctk
import threading
import requests
import time
from tkinter import filedialog

tokens = []
proxies = []

class Worker(threading.Thread):
    def __init__(self, token, channel_id, cooldown, proxy=None):
        super().__init__()
        self.token = token
        self.channel_id = channel_id
        self.cooldown = cooldown
        self.proxy = proxy
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            url = f'https://discord.com/api/v9/channels/{self.channel_id}/messages'
            headers = {'Authorization': self.token, 'Content-Type': 'application/json'}
            payload = {'content': app.message}
            proxy_dict = {'http': self.proxy, 'https': self.proxy} if self.proxy else None

            try:
                response = requests.post(url, headers=headers, json=payload, proxies=proxy_dict)
                if response.status_code == 200:
                    app.show_log(f"[+] Message sent with token {self.token[:5]}***.")
                else:
                    app.show_log(f"[-] Failed to send message with token {self.token[:5]}***: {response.status_code}")
            except Exception as e:
                app.show_log(f"Error: {e} with token {self.token[:5]}***")
            time.sleep(self.cooldown / 1000)

    def stop(self):
        self._stop_event.set()

class RaidTool(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Premium Saturn XV Spammer 2.0")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True)
        self.tabview.add("Settings")
        self.tabview.add("Server Spam")

        self.create_config_tab()
        self.create_server_spam_tab()

        self.workers = []
        self.message = ""

    def create_config_tab(self):
        layout = ctk.CTkFrame(self.tabview.tab("Settings"))
        self.import_tokens_button = ctk.CTkButton(layout, text="Import Tokens", command=self.import_tokens)
        self.import_tokens_button.pack(pady=10)
        self.import_proxies_button = ctk.CTkButton(layout, text="Import Proxies (optional)", command=self.import_proxies)
        self.import_proxies_button.pack(pady=10)
        layout.pack(padx=20, pady=20)

    def import_tokens(self):
        file_name = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_name:
            with open(file_name, 'r') as f:
                tokens.clear()
                tokens.extend(line.strip() for line in f)
            print(f"Imported {len(tokens)} tokens.")

    def import_proxies(self):
        file_name = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_name:
            with open(file_name, 'r') as f:
                proxies.clear()
                proxies.extend(line.strip() for line in f)
            print("Proxies imported.")

    def create_server_spam_tab(self):
        layout = ctk.CTkFrame(self.tabview.tab("Server Spam"))
        self.channel_label = ctk.CTkLabel(layout, text="Channel ID")
        self.channel_label.pack(pady=5)
        self.channel_input = ctk.CTkEntry(layout)
        self.channel_input.pack(pady=5)
        self.message_label = ctk.CTkLabel(layout, text="Message")
        self.message_label.pack(pady=5)
        self.message_input = ctk.CTkTextbox(layout, height=25, wrap="word")
        self.message_input.pack(pady=5)
        self.message_input.bind("<KeyRelease>", self.update_message)
        self.cooldown_label = ctk.CTkLabel(layout, text="Cooldown: 500ms")
        self.cooldown_label.pack(pady=5)
        self.cooldown_slider = ctk.CTkSlider(layout, from_=1, to=60000, command=self.update_cooldown_label)
        self.cooldown_slider.set(1250)
        self.cooldown_slider.pack(pady=10)
        self.start_button = ctk.CTkButton(layout, text="Start Raid", command=self.start_spam)
        self.start_button.pack(pady=10)
        self.stop_button = ctk.CTkButton(layout, text="Stop Raid", command=self.stop_spam, state="disabled")
        self.stop_button.pack(pady=10)
        self.log_label = ctk.CTkLabel(layout, text="Live Logs")
        self.log_label.pack(pady=10)
        self.log_output = ctk.CTkTextbox(layout, height=30, state="disabled", wrap="word")
        self.log_output.pack(pady=5)
        layout.pack(padx=20, pady=20)

    def update_message(self, event):
        self.message = self.message_input.get("1.0", "end-1c")

    def update_cooldown_label(self, value):
        self.cooldown_label.configure(text=f"Cooldown: {int(value)}ms")

    def start_spam(self):
        if tokens:
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            cooldown = int(self.cooldown_slider.get())
            for token in tokens:
                worker = Worker(token, self.channel_input.get(), cooldown)
                self.workers.append(worker)
                worker.start()

    def stop_spam(self):
        for worker in self.workers:
            worker.stop()
        self.workers.clear()
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")

    def show_log(self, message):
        self.log_output.configure(state="normal")
        self.log_output.insert("end", message + "\n")
        self.log_output.yview("end")
        self.log_output.configure(state="disabled")

if __name__ == "__main__":
    app = RaidTool()
    app.mainloop()

# STOP!
# You are allowed to modify this code and share it but please give us credits :)
# Made by nf