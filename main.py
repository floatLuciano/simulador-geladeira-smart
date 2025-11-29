import time
import sys


from controlador import criar_controlador_fuzzy
from fisica import GeladeiraFisica


def rodar_simulacao():
    print("--- INICIANDO SIMULAÇÃO DA GELADEIRA NEBULOSA ---")
    
    # 1. Instanciando os Módulos
    fuzzy_system = criar_controlador_fuzzy()
    geladeira = GeladeiraFisica(temp_inicial=15.0, vol_inicial=8.0) # Começa quente (25°C) e Cheia (8.0)

    # Cabeçalho da tabela
    print(f"{'TEMPO':<6} | {'T. EXT':<8} | {'T. INT':<8} | {'POTÊNCIA':<10} | {'STATUS'}")
    print("-" * 65)

    # 2. Loop de Simulação (Ex: 500 rodadas)
    # Cada rodada representa um passo de tempo (ex: 30 segundos na vida real)
    for t in range(500):
        
        # A. Atualiza o mundo (Física)
        geladeira.atualizar_ambiente_externo(t)
        
        # B. Leitura dos Sensores -> Fuzzy
        fuzzy_system.input['temp_int'] = geladeira.temp_int
        fuzzy_system.input['temp_ext'] = geladeira.temp_ext
        fuzzy_system.input['volume']   = geladeira.volume
        
        # C. Tomada de Decisão (Compute)
        fuzzy_system.compute()
        potencia_calculada = fuzzy_system.output['potencia']
        
        # D. Atuação no Mundo (Física reage à potência)
        geladeira.simular_passo(potencia_calculada)
        
        # E. Visualização (Log)
        # Mostra apenas a cada 2 passos para não poluir demais
        if t % 2 == 0:
            status = "OK"
            if geladeira.temp_int > 5: status = "QUENTE"
            if geladeira.temp_int < 1: status = "FRIO DEMAIS"
            
            print(f"{t:<6} | {geladeira.temp_ext:.1f}°C    | {geladeira.temp_int:.1f}°C    | {potencia_calculada:.1f}%      | {status}")
            
            # Pequena pausa para dar efeito visual de "tempo real"
            time.sleep(0.05)

    print("-------------------------------------")
    print("Simulação concluída.")

if __name__ == "__main__":
    rodar_simulacao()