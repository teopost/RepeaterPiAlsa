# sudo apt-get install python-pygame python-alsaaudio

import alsaaudio, wave, numpy, time, os, audioop, math
import subprocess
import sys

def salva_wav(data):
    w = wave.open('temp.wav', 'w')
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(44100)
    w.writeframes(data)
    w.close()

def play(audiofile):
    print "play ", audiofile
    subprocess.call(["aplay", audiofile ])

if __name__ == "__main__":
  print "Attendere. Initializzazione in corso..."

  inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
  inp.setchannels(1)
  inp.setrate(44100)
  inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
  inp.setperiodsize(1024)

  soglia = 80

  buffer_completo = False
  registrazione_iniziata = False
  cicli_sotto_soglia_durante_registrazione = 0
  cicli_sopra_soglia = 0

  all = []

  subprocess.call(["sudo","python","RX.py"])

  print "Pronto..."
 
  while True:
    # sto in ascolto
    l, data = inp.read()
    a = numpy.fromstring(data, dtype='int16')
    #volume = audioop.max(data, 2)
    volume = int(round(numpy.abs(a).mean(),-1))

    if volume > soglia:
        if not registrazione_iniziata:
            cicli_sopra_soglia = cicli_sopra_soglia + 1
            print cicli_sopra_soglia   
            if cicli_sopra_soglia > 5:
                print "soglia superata"
                registrazione_iniziata = True
                cicli_sotto_soglia_durante_registrazione = 0
                cicli_sopra_soglia = 0
    else:
        cicli_sopra_soglia = 0 
        if registrazione_iniziata:
            cicli_sotto_soglia_durante_registrazione = cicli_sotto_soglia_durante_registrazione + 1
            if cicli_sotto_soglia_durante_registrazione > 30:
                buffer_completo = True
                registrazione_iniziata = False
                cicli_sotto_soglia_durante_registrazione = 0

    if registrazione_iniziata:
        if not buffer_completo:
            all.append(data)
            if volume > soglia:
                print "RECORDING (%s)...: Volume: %s - %d - %d" % (soglia, volume, cicli_sopra_soglia, cicli_sotto_soglia_durante_registrazione)
            else:
                print "recording (%s)...: Volume: %s - %d - %d" % (soglia, volume, cicli_sopra_soglia, cicli_sotto_soglia_durante_registrazione)

    else:
        if buffer_completo:
            audiodata=''.join(all)

            salva_wav(audiodata)
           
            all = []

            subprocess.call(["sudo","python","TX.py"])
            #inp.write(audiodata)

            play("temp.wav")
            play("beep.wav")

            subprocess.call(["sudo","python","RX.py"])

            buffer_completo = False
            registrazione_iniziata = False
            cicli_sotto_soglia_durante_registrazione = 0
            cicli_sopra_soglia = 0

            print "riproduzione terminata"



