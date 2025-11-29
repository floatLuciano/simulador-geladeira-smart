import math

class GeladeiraFisica:
    def __init__(self, temp_inicial=25.0, vol_inicial=5.0):
        # Estado atual do sistema
        self.temp_int = temp_inicial
        self.volume = vol_inicial
        self.temp_ext = 30.0  # Valor inicial padrão
        self.tempo_decorrido = 0
        
        # Constantes de Calibração (Dinâmica)
        # k_isolamento: Quão rápido o calor entra
        self.k_isolamento = 0.002

        # k_compressor: Quão forte o motor resfria
        self.k_compressor = 0.15
        
    def atualizar_ambiente_externo(self, tempo):
        #Simula um dia completo em 500 passos. Começa Frio (20°C), sobe até o Pico (40°C) e desce.
        
        self.temp_ext = 30 - 10 * math.cos(tempo * 0.012)


    def simular_eventos_usuario(self, tempo):
        #Simula o comportamento humano: encher e esvaziar a geladeira. Isso altera o VOLUME e gera PICO DE CALOR (porta aberta). São eventos
        #simples e predefinidos para testar cenários diferentes
    
        
        # EVENTO 1: Chegada das compras na geladeira (Manhã - passo 100)
        if tempo == 100:
            print(f"\n[EVENTO {tempo}s] Compras na geladeira (fica cheia).")
            self.volume = 9.0      # Vai para 90% de capacidade (Massa térmica alta)
            self.temp_int += 2.0   # Porta aberta por muito tempo + alimentos quentes entrando
            
        # EVENTO 2: Preparando o almoço (Meio-dia - passo 250)
        elif tempo == 250:
            print(f"\n[EVENTO {tempo}s] Abrindo para pegar ingredientes.")
            # Volume não muda muito, mas entra calor
            self.temp_int += 2.0   
            
        # EVENTO 3: Faxina na geladeira / Jantar (Tarde - passo 400)
        elif tempo == 400:
            print(f"\n[EVENTO {tempo}s] Esvaziando a geladeira.")
            self.volume = 2.0      # Cai para 20% (Vazia - esfria rápido, esquenta rápido)
            self.temp_int += 1.0   # Porta aberta

    def simular_passo(self, potencia_aplicada, dt=1):
        #Aplica a Lei de Resfriamento de Newton via Integração de Euler. dt: passo de tempo da simulação (padrão = 1 unidade)
        # 1. Ganho de Calor (Troca com o ambiente)
        # Quanto maior a diferença (ext - int), mais rápido esquenta.
        diff_temp = self.temp_ext - self.temp_int
        ganho_calor = diff_temp * self.k_isolamento * dt
        
        # 2. Perda de Calor (Ação do Compressor)
        # Se a geladeira estiver cheia (volume alto), a eficiência de resfriamento cai um pouco
        # devido à dificuldade de circulação do ar e inércia térmica.
        fator_volume = 1.0 - (self.volume * 0.02) 
        perda_calor = (potencia_aplicada / 100.0) * self.k_compressor * fator_volume * dt
        
        # 3. Atualiza a Temperatura
        self.temp_int = self.temp_int + ganho_calor - perda_calor
        
        # Limites pra não bugar a simulação
        if self.temp_int < -5: self.temp_int = -5
        
        self.tempo_decorrido += dt
        return self.temp_int