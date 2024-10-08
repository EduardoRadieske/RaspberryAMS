import time
import os
from raspberry import Raspberry
from bms import BMS

serial_port = os.environ.get("SERIAL_PORT", "COM4")

rasp = Raspberry()

bms = BMS(serial_port, True)

def processar_falha():
    rasp.abrir_shutdown_system()
    rasp.acionar_sinal_ams()

try:
    print("Iniciando sistema...")

    while True:
        bms.restart()

        if rasp.validar_sistema_ativo() or rasp.validar_conectado_carga():
            print("Sistema monitorando!")

            if bms.validar_falha():
                processar_falha()
                time.sleep(5)
                continue
            
            if not bms.validar_niveis_tensao():
                processar_falha()
                time.sleep(5)
                continue
            
            """"
            TODO ADICIONAR DEMAIS VALIDAÇÕES DO REGULAMENTO

             if bms.retornar_tensao_total() < _TENSAO_DATASHEET_MIN:
                processar_falha()
                continue
            """

        time.sleep(1)
except KeyboardInterrupt:
    print("\nPrograma encerrado pelo usuário (Ctrl+C).")
finally:
    rasp.finalizar()
    bms.desconectar()