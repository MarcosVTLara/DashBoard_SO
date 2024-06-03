import tkinter as tk
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import subprocess

#View
class DashboardApp:
    #Essa classe manipula especificamente a parte visual do codigo, pegando os dados da classe de BuscaDados
    def __init__(self, dashboard):
        #Criação dos Frames, Notebooks e ListBox
        self.dashboard = dashboard
        self.dashboard.title("Dashboard Sistemas Operacionais")
        self.dashboard.geometry("1200x540")
        self.first = True
        self.caminho = '/'
        self.last_caminhos = ['/']

        nb = ttk.Notebook(self.dashboard)
        nb.place(x=0, y=0)

        self.frame1 = Frame(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame1, text="Info. SO")

        self.frame2 = tk.Listbox(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame2, text="Info. CPU")

        self.frame3 = tk.Listbox(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame3, text="Info. Hardware")

        self.frame4 = Frame(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame4, text="Info. Memoria")

        nb2 = ttk.Notebook(self.frame4)
        nb2.place(x=0, y=0)
        self.frame4_1 = Frame(self.frame4, width=960, height=530, bg='#eff5f6')
        nb2.add(self.frame4_1, text="Valores totais memória")
        self.frame4_2 = Frame(self.frame4, width=960, height=530, bg='#eff5f6')
        nb2.add(self.frame4_2, text="Gráfico memória")

        self.frame5 = tk.Listbox(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame5, text="Info. processos")
        scroll = tk.Scrollbar( self.frame5)
        scroll.pack(side="right", fill="both")

        self.frame5.config(yscrollcommand=scroll.set)
        scroll.config(command= self.frame5.yview)

        self.frame6 = tk.Listbox(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame6, text="Info. partições")

        self.frame7 = tk.Frame(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame7, text="Info. Arquivos")

        nb3 = ttk.Notebook(self.frame7)
        nb3.place(x=0, y=0)
        self.frame7_1 = tk.Listbox(self.frame7, width=960, height=530, bg='#eff5f6')
        nb3.add(self.frame7_1, text="Navegação Diretórios")

        self.frame8 = tk.Listbox(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame8, text="Info. Partições Sis. Arqui.")

        self.frame9 = tk.Frame(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame9, text="Entrada/Saída")

        nb4 = ttk.Notebook(self.frame9)
        nb4.place(x=0, y=0)
        self.frame9_1 = tk.Frame(self.frame9, width=960, height=530, bg='#eff5f6')
        nb4.add(self.frame9_1, text="Processos")


    #Função que atualiza todas as abas de informações
    def attInformacoes(self, dados):
        self.attGraficoMemoria(dados)
        self.attTabelaMemoria(dados)
        self.attInfoSO(dados)
        self.attInfoProcesso(dados)
        self.attInfoCPU(dados)
        self.attInfoHardware(dados)
        self.attInfoParticoes(dados)
        self.attInfoParticoesDir(dados)
        self.attProcessosAtivos(dados)
        if self.first == True:
            self.attTabelaDiretorios(dados.diretorios)
            self.first = False

    # Atualiza a tabela de dados da memoria usando Treeview
    def attTabelaMemoria(self, dados):
        for widget in self.frame4_1.winfo_children():
            widget.destroy()
        table = ttk.Treeview(self.frame4_1, columns=(1, 2), show="headings", height=10)
        table.pack()
        table.heading(1, text="Tipo")
        table.heading(2, text="Valor usado/disponivel (kb)")
        table.insert('', tk.END, values=['Memoria Total', dados.mtotal])
        table.insert('', tk.END, values=['Memoria Usado', dados.mUsada])
        table.insert('', tk.END, values=['Memoria Livre', dados.mLivre])
        table.insert('', tk.END, values=['Buff/Cache', dados.mBuff])
        table.insert('', tk.END, values=['Memoria Compartilhada', dados.mCompartilhada])
        table.insert('', tk.END, values=['Memoria Disponivel', dados.mDisponivel])

    #Adiciona linha por linha dos dados de processos
    def attInfoProcesso(self, dados):
        #Deleta as informações antigas
        for widget in self.frame5.winfo_children():
            widget.destroy()
        self.frame5.delete(0, END)
        i = 1
        #Insere uma linha vazia para identação
        self.frame5.insert(0, '')
        #Adiciona as linhas de informações
        for linha in dados.processos:
            self.frame5.insert(i, linha)
            i+=1
        labelEXP = ttk.Label(self.frame5, text="Informações sobre os Processos:")
        labelEXP.pack()

    # Adiciona linha por linha dos dados da CPU
    def attInfoCPU(self, dados):
        # Deleta as informações antigas
        for widget in self.frame2.winfo_children():
            widget.destroy()
        self.frame2.delete(0, END)
        labelEXP = ttk.Label(self.frame2, text="Informações sobre a CPU:")
        i = 1
        # Insere uma linha vazia para identação
        self.frame2.insert(0, '')
        # Adiciona as linhas de informações
        for linha in dados.informacoesCPU:
            self.frame2.insert(i, linha)
            i += 1
        labelEXP.pack()

    # Adiciona linha por linha dos dados do hardware
    def attInfoHardware(self, dados):
        # Deleta as informações antigas
        for widget in self.frame3.winfo_children():
            widget.destroy()
        self.frame3.delete(0, END)
        labelEXP = ttk.Label(self.frame3, text="Informações sobre o Hardware:")
        i = 1
        # Insere uma linha vazia para identação
        self.frame3.insert(0, '')
        # Adiciona as linhas de informações
        for linha in dados.infoHardware:
            self.frame3.insert(i, linha)
            i += 1
        labelEXP.pack()

    # Adiciona linha por linha dos dados das partições
    def attInfoParticoes(self, dados):
        # Deleta as informações antigas
        for widget in self.frame6.winfo_children():
            widget.destroy()
        self.frame6.delete(0, END)
        labelEXP = ttk.Label(self.frame6, text="Informações sobre as Partições:")
        i = 1
        # Insere uma linha vazia para identação
        self.frame6.insert(0, '')
        # Adiciona as linhas de informações
        for linha in dados.particoes:
            self.frame6.insert(i, linha)
            i += 1
        labelEXP.grid()

    # Adiciona os dados do Sistema Operacional
    def attInfoSO(self, dados):
        # Deleta as informações antigas
        for widget in self.frame1.winfo_children():
            widget.destroy()
        labelEXP = ttk.Label(self.frame1, text="Informações sobre o SO:")
        infoSOLabel = ttk.Label(self.frame1, text=dados.infoSO, background='#eff5f6')
        labelEXP.grid()
        infoSOLabel.grid()

    #Cria um grafico para o uso de memória e insere a imagem na tela
    def attGraficoMemoria(self, dados):
        # Deleta o grafico antigo
        for widget in self.frame4_2.winfo_children():
            widget.destroy()
        #Tamanho
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        #Labels e dados
        labels = ['Usado', 'Livre', 'Buffer/Cache']
        sizes = [dados.mUsada, dados.mLivre, dados.mBuff]

        #Angulos
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        canvas = FigureCanvasTkAgg(fig, master=self.frame4_2)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def attInfoParticoesDir(self, dados):
        # Deleta as informações antigas
        for widget in self.frame8.winfo_children():
            widget.destroy()
        self.frame8.delete(0, END)
        labelEXP = ttk.Label(self.frame8, text="Informações sobre as Partições do Sistema de arquivos:")
        i = 1
        # Insere uma linha vazia para identação
        self.frame8.insert(0, '')
        # Adiciona as linhas de informações
        lista_de_linhas = dados.infoParticoesDir.split("\n")
        for linha in lista_de_linhas:
            self.frame8.insert(i, linha)
            i += 1
        labelEXP.grid()

    def buscaDiretorioFilhos(self, caminho):
        linhas = subprocess.run(["ls", '-lh', caminho], capture_output=True, text=True)
        parseado = self.parse_file_entries(linhas.stdout)
        return parseado

    def buscaInfoPorPID(self, PID):
        linhas = subprocess.run(["lsof", '-p', PID], capture_output=True, text=True).stdout
        return linhas

    def botao_voltar(self):
        last_caminho = self.last_caminhos[-1]
        diretorios = self.buscaDiretorioFilhos(self.last_caminhos[-1])
        self.attTabelaDiretorios(diretorios)
        self.caminho = last_caminho
        if last_caminho != '/':
            self.last_caminhos.pop()

    def attTabelaDiretorios(self, diretorios):
        for widget in self.frame7_1.winfo_children():
            widget.destroy()

        table = ttk.Treeview(self.frame7_1, columns=(1, 2, 3, 4, 5, 6), show="headings", height=10)
        table.pack()
        table.heading(1, text="Nome Diretorio")
        table.heading(2, text="Permissões")
        table.heading(3, text="Número de link")
        table.heading(4, text="Proprietário")
        table.heading(5, text="Tamanho conteudo (bytes)")
        table.heading(6, text="Data/Hora de modificação")
        for entry in diretorios:
            table.insert('', tk.END, values=[entry['name'], entry['permissions'], entry['links'], entry['owner'],
                                             entry['size'], entry['modified_date']])
        button = tk.Button(self.frame7_1, text="Voltar", command=self.botao_voltar)
        button.pack(pady=10)
        def item_selected(event):
            item = table.selection()[0]
            # Obtém os valores da linha clicada
            values = table.item(item, 'values')
            if self.caminho == "/":
                self.caminho += values[0]
            else:
                self.last_caminhos.append(self.caminho)
                self.caminho = self.caminho + '/' + values[0]

            diretorios_filhos = self.buscaDiretorioFilhos(self.caminho)


            self.attTabelaDiretorios(diretorios_filhos)

        table.bind('<<TreeviewSelect>>', item_selected)

    def attProcessosAtivos(self, dados):
        for widget in self.frame9_1.winfo_children():
            widget.destroy()

        table = ttk.Treeview(self.frame9_1, columns=(1, 2, 3, 4, 5, 6), show="headings", height=10)
        table.pack()
        table.heading(1, text="USER")
        table.heading(2, text="PID")
        table.heading(3, text="CPU (%)")
        table.heading(4, text="MEM (%)")
        table.heading(5, text="START")
        table.heading(6, text="COMMAND")
        for entry in dados.processosAtivos:
            table.insert('', tk.END, values=[entry['USER'], entry['PID'], entry['%CPU'], entry['%MEM'],
                                            entry['START'], entry['COMMAND']])

        def item_selected(event):
            item = table.selection()[0]
            # Obtém os valores da linha clicada
            values = table.item(item, 'values')
            PID = values[1]
            dash = tk.Tk()
            dash.title("Processo - PID: " + PID)
            dash.geometry("960x540")
            frame_info = tk.Listbox(dash, width=960, height=530, bg='#eff5f6')
            frame_info.pack(padx=10, pady=10)
            linhas = self.buscaInfoPorPID(PID)
            lista_de_linhas = linhas.split("\n")
            #labelEXP = ttk.Label(frame_info, text="Informações sobre o processo de PID [" + PID + "]:")
            i = 1
            # Insere uma linha vazia para identação
            frame_info.insert(0, '')
            # Adiciona as linhas de informações
            for linha in lista_de_linhas:
                frame_info.insert(i, linha)
                i += 1
            #labelEXP.grid()

        table.bind('<<TreeviewSelect>>', item_selected)

    def parse_file_entries(self, data):
        entries = []
        lines = data.strip().split('\n')
        primeira_linha = True
        for line in lines:
            if primeira_linha == True:
                primeira_linha = False
                continue
            parts = line.split()
            entry = {
                'permissions': parts[0],
                'links': int(parts[1]),
                'owner': parts[2],
                'group': parts[3],
                'size': parts[4],
                'modified_date': ' '.join(parts[5:8]),
                'name': parts[8]
            }
            entries.append(entry)

        return entries
