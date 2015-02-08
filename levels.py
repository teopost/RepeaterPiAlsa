# sudo apt-get install python-pygame python-alsaaudio

import alsaaudio, wave, numpy, time, os, audioop, math
import sys

if __name__ == "__main__":
  print "Attendere. Initializzazione in corso..."

  inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
  inp.setchannels(1)
  inp.setrate(44100)
  inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
  inp.setperiodsize(1024)

  soglia = 80

  print "Pronto..."
 
  while True:
    # sto in ascolto
    l, data = inp.read()
    a = numpy.fromstring(data, dtype='int16')
    volume = int(round(numpy.abs(a).mean()))
    #print "Soglia:%s, Volume:%s | %s" % (soglia, volume, '*'*volume )
    print "Soglia:%s, Volume:%s" % (soglia, volume)
    time.sleep(.005)



