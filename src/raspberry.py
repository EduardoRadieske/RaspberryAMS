import traceback
import time
from RPiSim.GPIO import GPIO 
#import RPi.GPIO as GPIO ---- PARA EXECUTAR NO RASPBIAN

class Raspberry:
    _GPIO_SISTEMA_TRACAO = 23
    _GPIO_CONECTADO_CARGA = 24
    _GPIO_SHUTDOWN_CIRCUIT = 17
    _GPIO_AVISO_AMS = 27

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self._GPIO_SISTEMA_TRACAO, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) 
        GPIO.setup(self._GPIO_CONECTADO_CARGA, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(self._GPIO_SHUTDOWN_CIRCUIT, GPIO.OUT, GPIO.LOW) 
        GPIO.setup(self._GPIO_AVISO_AMS, GPIO.OUT, GPIO.LOW)   
    
    def validar_sistema_ativo(self):
        try:
            return GPIO.input(self._GPIO_SISTEMA_TRACAO)
        except Exception:
            traceback.print_exc()
            return False

    def validar_conectado_carga(self):
        try:
            return GPIO.input(self._GPIO_CONECTADO_CARGA)
        except Exception:
            traceback.print_exc()
            return False
    
    def finalizar():
        try:
            GPIO.cleanup()
        except Exception:
            traceback.print_exc()

    def abrir_shutdown_system(self):
        try:
            GPIO.output(self._GPIO_SHUTDOWN_CIRCUIT, GPIO.HIGH)
        except Exception:
            traceback.print_exc()
    
    def acionar_sinal_ams(self):
        try:
            GPIO.output(self._GPIO_AVISO_AMS, GPIO.HIGH)
        except Exception:
            traceback.print_exc()