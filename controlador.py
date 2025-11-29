import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def criar_controlador_fuzzy():
    # 1. Entradas e Saída
    
    # Respeitando os intervalos que definidos
    temp_int = ctrl.Antecedent(np.arange(0, 12.1, 0.1), 'temp_int')
    temp_ext = ctrl.Antecedent(np.arange(0, 50.1, 0.1), 'temp_ext')
    vol      = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'volume')
    potencia = ctrl.Consequent(np.arange(0, 101, 1), 'potencia')

    # 2. Funções de Pertinência

    # Temperatura Interna
    temp_int['frio']   = fuzz.trapmf(temp_int.universe, [0, 0, 1.5, 3.0])
    temp_int['ideal']  = fuzz.trimf(temp_int.universe, [1.5, 3.0, 4.5])
    temp_int['quente'] = fuzz.trapmf(temp_int.universe, [3.0, 5.0, 12, 12])

    # Temperatura Externa
    temp_ext['fria']   = fuzz.trapmf(temp_ext.universe, [0, 0, 10, 18])
    temp_ext['ideal']  = fuzz.trimf(temp_ext.universe, [14, 24, 34])
    temp_ext['quente'] = fuzz.trapmf(temp_ext.universe, [28, 35, 50, 50])

    # Volume
    vol['vazio'] = fuzz.trapmf(vol.universe, [0, 0, 2, 4])
    vol['medio'] = fuzz.trimf(vol.universe, [3, 5, 7])
    vol['cheio'] = fuzz.trapmf(vol.universe, [6, 8, 10, 10])

    # Saída: Potência
    potencia['baixa']      = fuzz.trimf(potencia.universe, [0, 0, 50])
    potencia['media']      = fuzz.trimf(potencia.universe, [30, 50, 70])
    potencia['alta']       = fuzz.trimf(potencia.universe, [50, 75, 100])
    potencia['muito_alta'] = fuzz.trimf(potencia.universe, [80, 100, 100])

    # 3. Base de Regras

    regras = [
        # Se está FRIO dentro, descansa
        ctrl.Rule(temp_int['frio'], potencia['baixa']),
        
        # Se está IDEAL dentro
        ctrl.Rule(temp_int['ideal'] & temp_ext['fria'], potencia['baixa']),
        ctrl.Rule(temp_int['ideal'] & temp_ext['ideal'], potencia['media']),
        ctrl.Rule(temp_int['ideal'] & temp_ext['quente'], potencia['alta']),
        ctrl.Rule(temp_int['ideal'] & vol['cheio'], potencia['media']), # Ajuste físico (evitar congelar)
        
        # Se está QUENTE dentro (Crítico)
        ctrl.Rule(temp_int['quente'] & temp_ext['fria'], potencia['media']),
        ctrl.Rule(temp_int['quente'] & temp_ext['ideal'], potencia['alta']),
        ctrl.Rule(temp_int['quente'] & (temp_ext['quente'] | vol['cheio']), potencia['muito_alta'])
    ]

    # Criação do Sistema de Controle
    sistema_ctrl = ctrl.ControlSystem(regras)
    simulador = ctrl.ControlSystemSimulation(sistema_ctrl)
    
    return simulador