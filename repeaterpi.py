import alsaaudio, wave, numpy, time, os
import subprocess
import sys

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
inp.setchannels(1)
inp.setrate(44100)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
inp.setperiodsize(1024)

soglia = 500

buffer_completo = False
conto_silenzio = 0
registrazione_iniziata = False

def salva_wav(data):
    w = wave.open('test.wav', 'w')
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(44100)
    w.writeframes(data)
    w.close()

all = []

while True:
    # sto in ascolto
    l, data = inp.read()
    a = numpy.fromstring(data, dtype='int16')
    volume = numpy.abs(a).mean()
    #print volume, soglia

    if volume > soglia:
        print "Soglia superata"
        registrazione_iniziata = True
        conto_silenzio = 0
    else:
        if registrazione_iniziata:
            conto_silenzio = conto_silenzio + 1
            if conto_silenzio > 100:
                buffer_completo = True
                registrazione_iniziata = False
                conto_silenzio = 0

    if registrazione_iniziata:
        if not buffer_completo:
            all.append(data)
            #sys.stdout.write('-')
            print "attach"
    else:
        if buffer_completo:
            salva_wav(''.join(all))
            all = []
            buffer_completo = False
            subprocess.call(["aplay","test.wav"])
            print "riproduzione terminata"



