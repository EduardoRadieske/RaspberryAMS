from dalybms import daly_bms
import logging

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

        self.daly.connect(porta)

    def validar_falha(self):
        return not self.daly.get_status()

    def desconectar(self):
        self.daly.disconnect()
    
    def retornar_tensao_total(self, tentativa = 1):
        try:
            socJson = self.daly.get_soc()
        except Exception as e:
            print(f"Ocorreu um erro BMS get_soc: {e}")

        if not socJson:
            if tentativa < 3:
                self.desconectar()
                self.daly.restart()

                self.retornar_tensao_total(tentativa + 1)
            else:
                return _ult_soc_medido
            
        _ult_soc_medido = socJson.total_voltage
        return socJson.total_voltage
    
    
    