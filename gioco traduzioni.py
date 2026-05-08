import sounddevice as sd # Libreria che serve a registrare il vocale
import scipy.io.wavfile as wav # Libreria per salvare il file in formato wav
import speech_recognition as sr # Libreria che riconosce il parlato e crea la trascrizione
from deep_translator import GoogleTranslator # Libreria per tradurre il testo
import os
import random

vite =3
risposta = input("Benvenuto! In questo gioco ti apparirà una frase in italiano, tu dovrai tradurla in inglese! Vuoi giocare? (sì/no) ")
if risposta == "si":
    livello = input("seleziona il livello di difficoltà: facile, medio, difficile")
    words_by_level = {
        "facile": ["gatto", "cane", "mela", "latte", "sole"],
        "medio": ["banana", "scuola", "ragazzo", "finestra", "giallo"],
        "difficile": ["tecnologia", "università", "informazione", "pronuncia", "immaginazione"]
    }
    while True:
        if livello == "facile":
            parola = random.choice(words_by_level["facile"])
        elif livello == "medio":
            parola = random.choice(words_by_level["medio"])
        elif livello == "difficile":
            parola = random.choice(words_by_level["difficile"])
        print("Ecco la parola da tradurre:", parola)
        durata_registrazione = 4  # Durata della registrazione in secondi
        sample_rate = 44100  # Frequenza di campionamento
        
        print("\nPreparati... inizia la registrazione")
        
        # Elimina il file precedente se esiste
        if os.path.exists("output.wav"):
            os.remove("output.wav")
        
        registrazione = sd.rec(frames=(durata_registrazione * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
        sd.wait()  # Aspetta che la registrazione sia finita
        print("Registrazione terminata, ora tutto verrà analizzato...")
        
        wav.write("output.wav", sample_rate, registrazione)  # Salva la registrazione in un file wav
        
        trascrittore = sr.Recognizer()  # Prepara il file al riconoscimento vocale e alla trascrizione
        with sr.AudioFile("output.wav") as source:
            audio = trascrittore.record(source)
        text = trascrittore.recognize_google(audio, language="it-IT")
        print("Hai detto: ", text) 
        if text.lower() == GoogleTranslator(source='it', target='en').translate(parola).lower():     
            print("Complimenti! Hai tradotto correttamente! :)")
            continua = input("Vuoi continuare? (sì/no) ")
            if continua == "si":
                if words_by_level[livello]:
                    words_by_level[livello].remove(parola)  # Rimuove la parola già usata
                    if not words_by_level[livello]:  # Se non ci sono più parole, il giocatore ha vinto
                        print("Hai completato il livello", livello, "! Passa al livello successivo!")
                        if livello == "facile":
                            livello = "medio"
                        elif livello == "medio":
                            livello = "difficile"
                        else:
                            print("Hai vinto il gioco! Complimenti!")
                        break
            else:
                print("Va bene, magari la prossima volta! :)") 
                breaksi        
        else:
            vite -= 1
            print("Mi dispiace, la traduzione corretta era:", GoogleTranslator(source='it', target='en').translate(parola), f"sei a {vite} vite da perdere! Studia di più! :(")
            if vite == 0:
                print("Game Over!")
                break
else:
      print("Va bene, magari la prossima volta! :)") 
       