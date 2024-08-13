from dalybms import daly_bms
from serial.serialutil import SerialException
import logging
import time

class BMS:
    _TENSAO_DATASHEET_MAX = 3.6
    _TENSAO_DATASHEET_MIN = 3.0

    _ult_status_tensao = True

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

    def restart(self):
        try:
            self.daly.restart()
        except Exception as e:
            print(f"Ocorreu um erro BMS restart: {e}")
    
    def validar_niveis_tensao(self, tentativa = 1):
        socJson = False

        try:
            socJson = self.daly.get_cell_voltage_range()
        except Exception as e:
            print(f"Ocorreu um erro BMS get_cell_voltage_range: {e}")

        if not socJson:
            if tentativa < 3:
                self.desconectar()
                try:
                    self.daly.restart()
                except Exception as e:
                    print(f"Ocorreu um erro BMS restart: {e}")

                time.sleep(2)

                return self.validar_niveis_tensao(tentativa + 1)
            else:
                print(f"_ult_status_tensao 2: {self._ult_status_tensao}")
                return self._ult_status_tensao
        
        if (socJson['lowest_voltage'] < self._TENSAO_DATASHEET_MIN or 
            socJson['highest_voltage'] > self._TENSAO_DATASHEET_MAX):
            self._ult_status_tensao = False
        else:
            self._ult_status_tensao = True

        print(f"_ult_status_tensao 1: {self._ult_status_tensao}")
        return self._ult_status_tensao

