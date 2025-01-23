import tkinter as tk
from tkinter import messagebox
from vulns import check_os, smb_vuln

def check_snmp():
    host = host_entry.get()
    port = port_entry.get()
    if check_os(host, port):
        messagebox.showinfo("Resultado", "SNMP Vulnerável, procure o suporte técnico responsável!")
    else:
        messagebox.showinfo("Resultado", "SNMP Seguro!")

def check_smb():
    host = host_entry.get()
    port = port_entry.get()
    if smb_vuln(host, port):
        messagebox.showinfo("Resultado", "SMB Vulnerável, procure o suporte técnico responsável!")
    else:
        messagebox.showinfo("Resultado", "SMB Seguro!")

def exit_app():
    root.destroy()

root = tk.Tk()
root.title("RedeSeg")

tk.Label(root, text="----------------Valide Vulnerabilidades----------------").pack()

tk.Label(root, text="IP do host:").pack()
host_entry = tk.Entry(root)
host_entry.pack()

tk.Label(root, text="Porta do host:").pack()
port_entry = tk.Entry(root)
port_entry.pack()

tk.Button(root, text="Verificar vulnerabilidade SNMP", command=check_snmp).pack()
tk.Button(root, text="Verificar vulnerabilidade SMB", command=check_smb).pack()
tk.Button(root, text="Sair", command=exit_app).pack()

root.mainloop()