import time
import sys
from serial.serialutil import SerialException
from raspberry import Raspberry
from bms import BMS

_TENSAO_DATASHEET_MIN = 70.0
rasp = Raspberry()

try:
    bms = BMS("COM4", True)
except SerialException:
    print("BMS NÃO ESTÁ CONECTADO!")

def processar_falha():
    rasp.abrir_shutdown_system()
    rasp.acionar_sinal_ams()

try:
    while True:

        if rasp.validar_sistema_ativo() or rasp.validar_conectado_carga():
            print("Sistema monitorando!")
            
            if bms.validar_falha():
                processar_falha()
                continue
            
            if bms.retornar_tensao_total() < _TENSAO_DATASHEET_MIN:
                processar_falha()
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

"""
def validarStatus():
    if daly.get_status() == False:
        daly.disconnect()
        sys.exit()

def reiniciar():
    execucao = 1
    daly.disconnect()
    daly.restart()


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

daly = daly_bms.DalyBMS(5, 4, logger)


daly = daly_bms.DalyBMS(5)

daly.connect("COM4")

validarStatus()

execucao = 1
totalExecucoes = 1

try:
    while True:
        print(f"Iteração {totalExecucoes}")
        print("==========================")

        if execucao == 3:
            reiniciar()

            validarStatus()
        
        try:
            socJson = daly.get_all()
            soc_str = json.dumps(socJson)
            print("Retorno: " + soc_str)
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            reiniciar()

            validarStatus()

        execucao += 1
        totalExecucoes +=1
        time.sleep(5)

except KeyboardInterrupt:
    daly.disconnect()
    print("\nPrograma encerrado pelo usuário (Ctrl+C).")
"""