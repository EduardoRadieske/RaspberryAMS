from dalybms import daly_bms
from serial.serialutil import SerialException
import logging
import time

class BMS:
    _ult_soc_medido = 0.0

    def __init__(self, porta, debug = False):
        if debug:
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.DEBUG)

            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)

            logger.addHandler(handler)
            self.daly = daly_bms.DalyBMS(5, 4, logger)
        else:
            self.daly = daly_bms.DalyBMS(5)

        try:
            self.daly.connect(porta)
        except SerialException as ex:
            print(f"BMS NÃO ESTÁ CONECTADO! Detalhes: {ex}")

    def validar_falha(self):
        try:
            return not self.daly.get_status()
        except Exception:
            return True


    def desconectar(self):
        try:
            self.daly.disconnect()
        except Exception:
            pass
    
    def retornar_tensao_total(self, tentativa = 1):
        socJson = False

        try:
            socJson = self.daly.get_soc()
        except Exception as e:
            print(f"Ocorreu um erro BMS get_soc: {e}")

        if not socJson:
            if tentativa < 3:
                self.desconectar()
                try:
                    self.daly.restart()
                except Exception as e:
                    print(f"Ocorreu um erro BMS restart: {e}")

                time.sleep(2)

                return self.retornar_tensao_total(tentativa + 1)
            else:
                ##DEBGUG print(f"_ult_soc_medido: {self._ult_soc_medido}")
                return self._ult_soc_medido
            
        self._ult_soc_medido = socJson.total_voltage
        return socJson.total_voltage
    
    
    