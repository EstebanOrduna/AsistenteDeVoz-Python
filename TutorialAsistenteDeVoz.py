import speech_recognition as sr  #Requiere PyAudio, la cual se pudo instalar solamente por medio de pipwin (installar pipwin primero y luego usar pipwin en lugar de pip para installar PyAudio. Si no se reconoce la palabra "pipwin", reiniciar VS Code y volver a intentar)
import pyttsx3
import winsound
import random
import getpass  #Para obtener el usuario de la computadora 

usuario = getpass.getuser() #Obtener nombre completo de usuario
usuario = usuario.split(" ")[0] #Utilizar únicamente el primer nombre

class Asistente():
    def __init__(self, nombre, velocidad=175, idioma="es-MX"):
        #Inicializar
        self.nombre = nombre
        self.velocidad = velocidad
        self.idioma = idioma
        self.conversaciónActiva=True

        ########### VOZ ###########
        #Arrancar motor TextToSpeech
        self.engine = pyttsx3.init()
        #Obtener voces disponibles [Puede variar según tu computadora]
        self.voices = self.engine.getProperty('voices')
        #Configurar voz en español
        self.engine.setProperty('language', idioma)
        print("Voces disponibles en esta computadora:")
        for voice in self.voices:
            print(f'Voz disponible: {voice.name}')
            #Utilizar voz mexicana
            if "-MX" in idioma: 
                if "MEXICO" in voice.name.upper() or "MÉXICO" in voice.name.upper():
                    self.engine.setProperty('voice', voice.id)
        print("")
        #Velocidad de voz
        self.engine.setProperty('rate',velocidad)

        #Presentación
        print(f"¡Asistente {self.nombre} disponible!")
        print(f'Voz: {voice.name}')

        #Reconocimiento de voz
        self.reconocimientoDeVoz = sr.Recognizer()

        self.saludar()

        self.esperarLlamada()

    def decir(self, frases):
        #Define la frase a decir
        if isinstance(frases,list):
            #Selecciona aleatoriamente una frase de la lista de frases
            frase = frases[random.randint(0,len(frases)-1)]
        else:
            frase = frases
        #Hablar
        print(f'{self.nombre}> {frase}')            
        self.engine.say(frase)
        self.engine.runAndWait()

    def escuchar(self):
        #REPETIR HASTA ESCUCHAR ALGO
        with sr.Microphone() as source:
            while True:
                try:
                    winsound.Beep(1000,75)
                    self.reconocimientoDeVoz.adjust_for_ambient_noise(source)
                    #print(f"{self.nombre}> Esperando audio...")
                    audio = self.reconocimientoDeVoz.listen(source, timeout=5, phrase_time_limit=10)
                    break
                except sr.WaitTimeoutError:
                    self.conversaciónActiva=False
                    continue
                else:
                    pass
        
        #Reconocimiento de audio
        #winsound.Beep(beep_freq, beep_dur)
        voice_data=""
        try:
            voice_data = self.reconocimientoDeVoz.recognize_google(audio, language=self.idioma).capitalize()
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            self.decir("Lo siento, mi reconocimiento de voz no está funcionando en estos momentos... Por favor asegúrate de tener conexión a internet")
            self.conversaciónActiva = False
        return voice_data.upper()

    def saludar(self):
        saludosIniciales = [
            f"¡Hola {usuario}! Aquí {self.nombre} reportándome!",
            f"¡Buen día {usuario}! Aquí {self.nombre}",
            f"¡Comencemos {usuario}!",
            f"¡Lista para ayudar {usuario}!",
            f"¡Hola {usuario}!",
            f"Que onda loco {usuario}!",
            "Este es un saludo"
        ]
        self.decir(saludosIniciales)
        #Iniciar conversación
        self.conversaciónActiva = True

    def esperarLlamada(self):
        while True:
            #INICIA CON UN MENSAJE EN BLANCO
            mensaje_de_voz=""
            #PRESTA ATENCIÓN POR SI TE HABLAN
            mensaje_de_voz = self.escuchar()
            #SI HAY UNA CONVERSACIÓN ACTIVA O TE HABLAN...
            if self.conversaciónActiva == True or self.nombre.upper() in mensaje_de_voz or self.nombre in mensaje_de_voz or "COMPUTADORA" in mensaje_de_voz or "ASISTENTE" in mensaje_de_voz:
                self.conversaciónActiva=True
                self.responder(mensaje_de_voz)

    def responder(self,mensaje):
        #DESIFRAR MENSAJE
        mensaje = mensaje.upper()
        print(f'{usuario}> {mensaje}')

        if not mensaje:
            self.decir("Quedo al pendiente.")
            self.conversaciónActiva=False
            return
        else:
            if "HOLA" in mensaje:
                self.decir(f"Hola, qué tal {usuario}!")
            
            elif "DIME ALGO" in mensaje:
                frases = [
                    "¿Qué quieres que te diga? Soy solo un ejemplo de tutorial...",
                    "Realmente no hay mucho que sepa decir en este punto de mi desarrollo",
                    "Al menos espero que disfruten este tutorial",
                    "¿Ya mero terminan de estudiarme?",
                    "¿Sabías que esta versión fue programada de urgencia un domingo por la noche?",
                ]
                self.decir(frases)

            elif "GRACIAS" in mensaje:
                self.decir("Fui programada para apoyarte.")
                self.conversaciónActiva= False

            else:
                self.decir(f"No entendí qué quisiste decir con {mensaje}")


Asistente("Sabina", 220, "es-MX")