import alsaaudio, wave, numpy, time, os, audioop
import subprocess
import sys

def salva_wav(data):
    w = wave.open('temp.wav', 'w')
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(44100)
    w.writeframes(data)
    w.close()


if __name__ == "__main__":

  inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
  inp.setchannels(1)
  inp.setrate(44100)
  inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
  inp.setperiodsize(1024)

  soglia = 3500

  buffer_completo = False
  registrazione_iniziata = False
  conto_silenzio = 0
  conto_inizio = 0

  all = []

  subprocess.call(["sudo","python","RX.py"])

  while True:
    # sto in ascolto
    l, data = inp.read()
    a = numpy.fromstring(data, dtype='int16')
    volume = audioop.max(data, 2)
    #volume = numpy.abs(a).mean()

    if volume > soglia:
        conto_inizio = conto_inizio +1
        if conto_inizio > 5:
            print ">>> Soglia superata"
            registrazione_iniziata = True
            conto_silenzio = 0
            conto_inizio = 0
    else:
        if registrazione_iniziata:
            conto_silenzio = conto_silenzio + 1
            if conto_silenzio > 30:
                buffer_completo = True
                registrazione_iniziata = False
                conto_silenzio = 0
                conto_inizio = 0

    if registrazione_iniziata:
        if not buffer_completo:
            all.append(data)
            print volume, soglia, conto_inizio

    else:
        if buffer_completo:
            salva_wav(''.join(all))
            all = []

            subprocess.call(["sudo","python","TX.py"])
            subprocess.call(["aplay","temp.wav","beep.wav"])
            subprocess.call(["sudo","python","RX.py"])

            buffer_completo = False
            registrazione_iniziata = False
            conto_silenzio = 0
            conto_inizio = 0

            print "riproduzione terminata"



