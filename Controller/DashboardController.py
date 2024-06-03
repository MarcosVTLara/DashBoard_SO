import threading
import tkinter as tk
from tkinter import *

from BackEnd.BuscarDados import BuscarDados
from FrontEnd.DashBoardApp import DashboardApp




class DashboardController:
    # Classe para controlar as chamadas do dashboard via thread
    def __init__(self):
        self.dashboard = tk.Tk()
        self.dashApp = DashboardApp(self.dashboard)
        self.dados = BuscarDados()
        self.buscarDados()
        self.dashboard.mainloop()

    def buscarDados(self):
        #Codigo que irá buscar a cada 5 segundos os dados do linux via threads, utilizamos uma thread para cada função de busca
        thread1 = threading.Thread(target=self.dados.buscaProcessos)
        thread2 = threading.Thread(target=self.dados.buscaInfoSO)
        thread3 = threading.Thread(target=self.dados.buscaParticoes)
        thread4 = threading.Thread(target=self.dados.buscaInfoHardware)
        thread5 = threading.Thread(target=self.dados.buscaInfoMemoria)
        thread6 = threading.Thread(target=self.dados.buscaInformacoesCPU)
        thread7 = threading.Thread(target=self.dados.buscaQuantidadeCPU)
        thread8 = threading.Thread(target=self.dados.buscaInfoParticoesDir)
        thread9 = threading.Thread(target=self.dados.buscaProcessosAtivos)
        self.dados.buscaDiretoriosRoot()

        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread5.start()
        thread6.start()
        thread7.start()
        thread8.start()
        thread9.start()
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        thread5.join()
        thread6.join()
        thread7.join()
        thread8.join()
        thread9.join()
        #Depois de buscar as informações o dashboard é atualizado com os dados
        self.dashApp.attInformacoes(self.dados)
        self.dashboard.after(5000, self.buscarDados)
