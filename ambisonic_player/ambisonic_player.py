import numpy as np
import sounddevice as sd
from scipy.io import wavfile


file = "countdown1.wav"
fs, data = wavfile.read(file)

file2 = "countdown2.wav"
fs2, data2 = wavfile.read(file2)

print(len(data), len(data2))

if not fs == fs2:
    raise ValueError("Les fréquences d'échantillonnages ne sont pas les mêmes")

class objet_sonore:
    def __init__(self, data, angle):
        self.data = data    #Audio data array
        self.angle = angle  #Angle of the object 

        self.coordinates()

    def coordinates(self):
        self.W = self.data
        self.X = self.data*np.cos(self.angle) 
        self.Y = self.data*np.sin(self.angle)

        

class speaker_object:
    def __init__(self, phi, teta, buffer_size):
        self.phi = phi #angle horizontal
        self.teta = teta #angle vertical

        self.X_factor = np.cos(self.phi)*np.cos(self.teta)
        self.Y_factor = np.sin(self.phi)*np.cos(self.teta)
        self.Z_factor = np.sin(self.teta)

        self.array = np.zeros(buffer_size)

    def calculate(self, sound_object):
        self.array += (sound_object.W/np.sqrt(2) +self.X_factor*sound_object.X + self.Y_factor*sound_object.Y + self.Z_factor*sound_object.Y)

lst_speaker = []
lst_sound_object = []

lst_speaker.append(speaker_object(np.pi/4, 0, len(data)))   #LF
lst_speaker.append(speaker_object(-np.pi/4, 0, len(data)))  #RF
lst_speaker.append(speaker_object(3*np.pi/4, 0, len(data))) #LB
lst_speaker.append(speaker_object(-3*np.pi/4, 0, len(data)))#RB

lst_sound_object.append(objet_sonore(data, np.pi/4))
#objet2 = objet_sonore(data2, -np.pi/4)

for speaker in lst_speaker:
    for object in lst_sound_object:
        speaker.calculate(object)

print(sd.query_devices())

output_matrix = lst_speaker[0].array
for object in lst_speaker[1::]:
    output_matrix = np.column_stack((output_matrix, object.array))

print(output_matrix.shape)

sd.play(data, fs, device=args.device)
sd.wait()