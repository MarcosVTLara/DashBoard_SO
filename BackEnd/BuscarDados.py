import re
import subprocess

#Model
class BuscarDados:
    #Classe que possue os valores mostrados em tela e que faz a busca desses valores
    def __init__(self):
        self.informacoesCPU = None
        self.quantidadeCPU = None
        self.infoHardware = None
        self.infoMemoria = None
        self.memoriaResumo = None
        self.processos = None
        self.particoes = None
        self.infoSO = None
        self.mtotal = None
        self.mUsada = None
        self.mLivre = None
        self.mCompartilhada = None
        self.mBuff = None
        self.mDisponivel = None
        self.infoParticoesDir = None
        self.diretorios = None
        self.processosAtivos = None

    #Busca das informações do CPU
    def buscaInformacoesCPU(self):
        cpuInfos = subprocess.run(['cat', '/proc/cpuinfo'], stdout=subprocess.PIPE)
        cpuInfosText = text=cpuInfos.stdout
        self.informacoesCPU = cpuInfosText.splitlines()

    #Busca informações da memoria
    def buscaInfoMemoria(self):
        self.memoriaResumo = subprocess.run(['free'], stdout=subprocess.PIPE)
        memoriaInfos = str(self.memoriaResumo.stdout)
        memoriaInfos.split()

        #Aqui estamos separando cada valor de uso de cada tipo da memoria, entre total, usada, livre, compartilhada, buff/cache e disponivel
        segunda_linha = memoriaInfos.split("\\n")[1]
        numbers = re.findall(r"\d+", segunda_linha)

        self.mtotal = numbers[0]
        self.mUsada = numbers[1]
        self.mLivre = numbers[2]
        self.mCompartilhada = numbers[3]
        self.mBuff = numbers[4]
        self.mDisponivel = numbers[5]

        self.infoMemoria = subprocess.run(['cat', '/proc/meminfo'], stdout=subprocess.PIPE)

    #Busca de quantidade de CPUs, esse valor não está sendo usado, mas foi mantido para mostrar o desenvolvimento do raciocinio
    def buscaQuantidadeCPU(self):
        cpu = subprocess.run(['nproc'], stdout = subprocess.PIPE)
        self.quantidadeCPU = cpu.stdout

    #Busca das informações de hardware
    def buscaInfoHardware(self):
        hardwareInfo = subprocess.run(['lscpu'], stdout = subprocess.PIPE)
        hardwareInfoText = text=hardwareInfo.stdout
        self.infoHardware = hardwareInfoText.splitlines()

    #Busca dos processos, utilizando n1 para atualizar apenas uma vez
    def buscaProcessos(self):
        processosInfos = subprocess.run(['top', '-b', '-n1'], stdout = subprocess.PIPE)
        processosInfosText = text=processosInfos.stdout
        self.processos = processosInfosText.splitlines()

    #Busca das partições
    def buscaParticoes(self):
        particoesInfo = subprocess.run(['cat', '/proc/partitions'], stdout = subprocess.PIPE)
        particoesInfosText = text=particoesInfo.stdout
        self.particoes = particoesInfosText.splitlines()

    #Busca das informações do Sistema Operacional
    def buscaInfoSO(self):
        self.infoSO = subprocess.run(["uname", '-a'], stdout=subprocess.PIPE).stdout

    def buscaInfoParticoesDir(self):
        self.infoParticoesDir = subprocess.run(["df", '-h'], capture_output=True, text=True).stdout

    def buscaDiretoriosRoot(self):
        linhas = subprocess.run(["ls", '-lh', '/'], capture_output=True, text=True)
        parseado = self.parse_file_entries(linhas.stdout)
        self.diretorios = parseado

    def buscaProcessosAtivos(self):
        linhas = subprocess.run(["ps", 'aux'], capture_output=True, text=True)
        parseado = self.parse_file_entries_processo(linhas.stdout)
        self.processosAtivos = parseado

    def parse_file_entries_processo(self, dados):
        entries = []
        lines = dados.strip().split('\n')
        primeira_linha = True
        for line in lines:
            if primeira_linha == True:
                primeira_linha = False
                continue
            parts = line.split()
            if len(parts) >= 11:
                entry = {
                    'USER': parts[0],
                    'PID': int(parts[1]),
                    '%CPU': float(parts[2]),
                    '%MEM': float(parts[3]),
                    'VSZ': int(parts[4]),
                    'RSS': int(parts[5]),
                    'TTY': parts[6],
                    'STAT': parts[7],
                    'START': parts[8],
                    'TIME': parts[9],
                    'COMMAND': ' '.join(parts[10:])
                }
                entries.append(entry)

        return entries

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
