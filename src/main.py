import time
from raspberry import Raspberry
from bms import BMS

_TENSAO_DATASHEET_MIN = 70.0
rasp = Raspberry()

bms = BMS("COM4")

def processar_falha():
    rasp.abrir_shutdown_system()
    rasp.acionar_sinal_ams()

try:
    while True:

        if rasp.validar_sistema_ativo() or rasp.validar_conectado_carga():
            print("Sistema monitorando!")

            if bms.validar_falha():
                processar_falha()
                time.sleep(10)
                continue
            
            if bms.retornar_tensao_total() < _TENSAO_DATASHEET_MIN:
                processar_falha()
                time.sleep(10)
                continue
            
            """"
            TODO ADICIONAR DEMAIS VALIDAÇÕES DO REGULAMENTO

             if bms.retornar_tensao_total() < _TENSAO_DATASHEET_MIN:
                processar_falha()
                continue
            """

        time.sleep(5)
except KeyboardInterrupt:
    print("\nPrograma encerrado pelo usuário (Ctrl+C).")
finally:
    rasp.finalizar()
    bms.desconectar()