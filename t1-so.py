#constantes
listc = [2, 0, 7, 2, 10, 5, 17, 8, 20, 1, 9, 8, 11, 17, 18, 7, 1, 0]
tam = len(listc)

class Memory:

    lis = []

    def __init__(self):
        self

    def set_list(self,lis):
        self.lis = lis

    def mem_tam(self):
        return len(self.lis)

    def mem_le(self,pos):
        try:
            return self.lis[pos]
        except:
            print("Acesso a endereço de memória inválido!")
            return 1

    def mem_escreve(self,pos,novo):
        try:
            self.lis[pos] = novo
            return 0
        except:
            print("Acesso a endereço de memória inválido!")
            return 1

    def mem_destroy(self):
        self.lis.clear()

class ES:
    
    def __init__(self):
        self
    
    #teclado = 0 terminal = 1

    def es_le(self, dispositivo, mem, valor):
        if(dispositivo != 0):
            print("Operação ilegal!")
            return 
        return mem.mem_le(valor)

    def es_escreve(self, dispositivo, mem, valor, novo):
        if(dispositivo != 1):
            print("Operação ilegal!")
            return 
        
        mem.mem_escreve(valor, novo)
        print("Print do ES:" + str(mem.mem_le(valor)))
        return 
        

class State:

    pc = int
    acu = int
    aux = int
    modo = str # 0 = a CPU está apta a executar a próxima instrução; !0 instrução de parada ou erro
    comp = str

    def __init__(self):
        self.pc = 0
        self.acu = 0
        self.aux = None
        self.modo = "ERR_OK"
        self.comp = "Funcionamento normal"

    def imprime_estado(self):
        print("PC:" + str(self.pc))
        print("Acumulador:" + str(self.acu))
        print("Auxiliar:" + str(self.aux)) 
        print("Modo:" + str(self.modo))
        print("Complemento:" + self.comp)
        print("")

class CPU:

    mem = None
    es = None
    state = None


    def __init__(self, mem, es, state):
        self.mem = mem
        self.es = es
        self.state = state

    def cpu_estado(self):
        return self.state

    def cpu_altera_estado(self, novo):
        self.state = novo

    def cpu_mem(self):
        return self.mem

    def cpu_altera_memoria(self, mem):
        self.mem = mem

    def cpu_es(self):
        return self.es

    def cpu_altera_es(self, es):
        self.es = es

    def cpu_modo(self):
        return self.state.modo

    def cpu_executa(self):
        pc = self.state.pc
        if(pc >= tam):
            self.state.modo = 1
            self.state.comp = "Acesso a endereço de memória inválido!"
        codigo = self.mem.mem_le(pc)
        a = self.state.acu
        if(pc+1 < tam): 
            a1 = self.mem.mem_le(pc + 1)
        x = self.state.aux

        if codigo == 0:
            # NOP não faz nada
            self.state.pc += 1
            return 0
        elif codigo == 1:
            # PARA para a CPU
            self.state.modo = "ERR_CPU_PARADA"
            self.state.comp = "Código bem sucedido."
            return 2
        elif codigo == 2:
            # CARGI carrega imediato
            self.state.acu = a1
            self.state.pc += 2
            return 0
        elif codigo == 3:
            # CARGM carrega da memória
            self.state.acu = self.mem.mem_le(a1)
            self.state.pc += 2
            return 0
        elif codigo == 4:
            # CARGX carrega indexado
            self.state.acu = self.mem.mem_le(a1 + x)
            self.state.pc += 2
            return 0
        elif codigo == 5:
            # ARMM armazena na memória
            self.mem.mem_escreve(a1, a)
            self.state.pc += 2
            return 0
        elif codigo == 6:
            # ARMX armazena indexado
            self.mem.mem_escreve(a1 + x, a)
            self.state.pc += 2
            return 0
        elif codigo == 7:
            # MVAX inicializa X
            self.state.aux = a
            self.state.pc += 1
            return 0
        elif codigo == 8:
            # MVXA recupera X
            self.state.acu = x
            self.state.pc += 1
            return 0
        elif codigo == 9:
            # INCX 	incrementa X
            try:
                self.state.aux += 1
                self.state.pc += 1
                return 0
            except:
                self.state.modo = "3"
                self.state.comp = "X não inicializado antes do incremento."
                return 3
            
        elif codigo == 10:
            # SOMA 	soma
            self.state.acu += self.mem.mem_le(a1)
            self.state.pc += 2
            return 0
        elif codigo == 11:
            # SUB subtração
            self.state.acu -= self.mem.mem_le(a1)
            self.state.pc += 2
            return 0
        elif codigo == 12:
            # MULT multiplicação
            self.state.acu *= self.mem.mem_le(a1)
            self.state.pc += 2
            return 0
        elif codigo == 13:
            # DIV divisão
            self.state.acu /= self.mem.mem_le(a1)
            self.state.acu = int(self.state.acu)
            self.state.pc += 2
            return 0
        elif codigo == 14:
            # RESTO resto
            self.state.acu %= self.mem.mem_le(a1)
            self.state.pc += 2
            return 0
        elif codigo == 15:
            # NEG negação
            self.state.acu = -a
            self.state.pc += 1
            return 0
        elif codigo == 16:
            # DESV desvio
            self.state.pc = a1
            return 0
        elif codigo == 17:
            # DESVZ desvio condicional
            if a == 0:
                self.state.pc = a1
                return 0
            self.state.pc += 2
            return 0
        elif codigo == 18:
            # DESVNZ desvio condicional
            if a != 0:
                self.state.pc = a1
                return 0
            self.state.pc += 2
            return 0
        elif codigo == 19:
            # LE leitura de E/S
            self.state.acu = self.es.es_le(0,self.mem,a1)
            self.state.pc += 2
            return 0
        elif codigo == 20:
            # ESCR escrita de E/S
            self.es.es_escreve(1,self.mem,a1,a)
            self.state.pc += 2
            return 0
        elif codigo == None:
            self.state.modo = 1
            self.state.comp = "Código nulo!"
            return 1
        else:
            self.state.modo = 1
            self.state.comp = "Código inválido!"
        



progr = listc

mem = Memory()
es = ES()
state = State()
cpu = CPU(mem,es,state)

cpu.mem.set_list(progr)

while True:
    cpu.state.imprime_estado()
    err = cpu.cpu_executa() #Retorna 0 se o programa vai seguir executando, 1 se deu erro, 2 se foi bem sucedido
    
    if err != 0:
        print("Código de saída:" + str(err))
        print("Estado final:")
        cpu.state.imprime_estado()
        print(cpu.mem.lis)
        exit(0)
