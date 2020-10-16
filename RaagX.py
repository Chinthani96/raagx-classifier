# 12/05/2020

from keras.engine.saving import model_from_json
from keras.models import Sequential
from keras.layers import Dense
from scipy.io.wavfile import read
import matplotlib as mpl
from matlab import mlarray
mpl.use('Agg')
import matlab.engine
import numpy as np
import eel
import tensorflow as tf

eel.init('web')

# function to get the user input and return the processed audio file to be sent through the NN
@eel.expose
def process_audio(wav_file):

    samples = list(wav_file.values())

    # Converting the audio to a 1D numpy array. The audio comes in the type .dict
    a = np.empty([2686843, 1])
    for i in range(2686843):
        a[i] = samples[i]
    audio = a
    audio = audio[79:]  
    audio = audio.T
    predictions = test_with_sample_model(audio)
    raga = generate_raga(predictions)
    return raga


def generate_fft(audio):
    eng = matlab.engine.start_matlab()
    # getting the fast fourier transformation of the inserted clip
    x = eng.fft(mlarray.double(audio))
    ab = eng.abs(x)
    ab = np.array(ab)
    print(ab)
    print(type(ab))
    print(np.shape(ab))
    # generate_raga(ab)
    test_with_fft_model(ab)


def test_with_fft_model(fft):
    print(type(fft), np.shape(fft))
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model.h5")
    print("Loaded fft model from disk")
    # evaluate loaded model on test data
    loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    if fft.ndim == 1:
        fft = np.array([fft])
    predictions1 = loaded_model.predict(fft)
    print(predictions1)


def test_with_sample_model(audio_samples):
    json_file = open('model2.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model2.h5")
    print("Loaded sample model from disk")
    # evaluate loaded model on test data
    loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    if audio_samples.ndim == 1:
        audio_samples = np.array([audio_samples])
    predictions2 = loaded_model.predict(audio_samples)
    print(predictions2)
    return predictions2
    # generate_raga(predictions2)


def generate_raga(predictions):
    if predictions[0][0] > 0.5:
        raga = "Raaga Yemen"
    elif predictions[0][1] > 0.5:
        raga = "Raaga Basant"
    elif predictions[0][2] > 0.5:
        raga = "Raaga Jog"
    elif predictions[0][3] > 0.5:
        raga = "Raaga Thilakkamod"
    else:
        raga = "None of the Raagas"
    print(raga)
    return raga


eel.start('index.html', size=(1000, 600))
