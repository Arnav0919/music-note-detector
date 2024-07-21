#Basic Musical Note Detector using pyAudio , numpy and tkinter.
#Note that the image paths used can be different for different users so kindly see to it .

from tkinter import *
import pyaudio
import wave
import threading
import numpy
import scipy.io.wavfile as wavfile
import scipy.fftpack
import time
from queue import Queue

notes = [
    ['C0', 16.35, []],
    ['C#0/Db0', 17.32, []],
    ['D0', 18.35, []],
    ['D#0/Eb0', 19.45, []],
    ['E0', 20.60, []],
    ['F0', 21.83, []],
    ['F#0/Gb0', 23.12, []],
    ['G0', 24.50, []],
    ['G#0/Ab0', 25.96, []],
    ['A0', 27.50, []],
    ['A#0/Bb0', 29.14, []],
    ['B0', 30.87, []],
    ['C1', 32.70, []],
    ['C#1/Db1', 34.65, []],
    ['D1', 36.71, []],
    ['D#1/Eb1', 38.89, []],
    ['E1', 41.20, []],
    ['F1', 43.65, []],
    ['F#1/Gb1', 46.25, []],
    ['G1', 49.00, []],
    ['G#1/Ab1', 51.91, []],
    ['A1', 55.00, []],
    ['A#1/Bb1', 58.27, []],
    ['B1', 61.74, []],
    ['C2', 65.41, []],
    ['C#2/Db2', 69.30, []],
    ['D2', 73.42, []],
    ['D#2/Eb2', 77.78, []],
    ['E2', 82.41, []],
    ['F2', 87.31, []],
    ['F#2/Gb2', 92.50, []],
    ['G2', 99.00, []],
    ['G#2/Ab2', 103.83, []],
    ['A2', 110.00, []],                 
    ['A#2/Bb2', 116.54, []],
    ['B2', 123.47, []],
    ['C3', 130.81, []],
    ['C#3/Db3', 138.59, []],
    ['D3', 146.83, []],
    ['D#3/Eb3', 155.56, []],
    ['E3', 164.81, []],
    ['F3', 174.61, []],
    ['F#3/Gb3', 185.00, []],
    ['G3', 196.00, []],
    ['G#3/Ab3', 208, []],
    ['A3', 221.00, []],
    ['A#3/Bb3', 234, []],
    ['B3', 247, []],
    ['C4', 264, []],
    ['C#4/Db4', 279, []],
    ['D4', 296, []],  
    ['D#4/Eb4', 314, []],
    ['E4', 329, []],
    ['F4', 350.23, []],
    ['F#4/Gb4', 371.00, []],
    ['G4', 396.00, []],
    ['G#4/Ab4', 419.30, []],
    ['A4', 445.00, []],
    ['A#4/Bb4', 472.16, []],
    ['B4', 501, []],
    ['C5', 529.25, []],
    ['C#5/Db5', 557.37, []],
    ['D5', 587.33, []],
    ['D#5/Eb5', 622.25, []],
    ['E5', 659.25, []],
    ['F5', 698.46, []],
    ['F#5/Gb5', 739.99, []],
    ['G5', 783.99, []],
    ['G#5/Ab5', 830.61, []],
    ['A5', 880.00, []],
    ['A#5/Bb5', 932.33, []],
    ['B5', 987.77, []],
    ['C6', 1046.50, []],
    ['C#6/Db6', 1108.73, []],
    ['D6', 1174.66, []],
    ['D#6/Eb6', 1244.51	, []],
    ['E6', 1318.51, []],
    ['F6', 1396.91, []],
    ['F#6/Gb6', 1479.98, []],
    ['G6', 1567.98, []],
    ['G#6/Ab6', 1661.22, []],
    ['A6', 1760.00	, []],
    ['A#6/Bb6', 1864.66, []],
    ['B6', 1975.53	, []],
    ['C7', 2093.00, []],
    ['C#7/Db7', 2217.46, []],
    ['D7', 2349.32, []],
    ['D#7/Eb7', 2489.02, []],
    ['E7', 2637.02, []],
    ['F7', 2793.83, []],
    ['F#7/Gb7 ', 2959.96, []],
    ['G7', 3135.96, []],
    ['G#7/Ab7', 3322.44, []],
    ['A7', 3520.00, []],
    ['A#7/Bb7', 3729.31, []],
    ['B7', 3951.07, []],
    ['C8', 4186.01, []],
    ['C#8/Db8', 4434.92, []],
    ['D8', 4698.63, []],
    ['D#8/Eb8', 4978.03, []],
    ['E8', 5274.04, []],
    ['F8', 5587.65, []],
    ['F#8/Gb8', 5919.91, []],
    ['G8', 6271.93, []],
    ['G#8/Ab8', 6644.88	, []],
    ['A8', 7040.00, []],
    ['A#8/Bb8', 7458.62, []],
    ['B8', 7902.13, []],]

#this function generalises the notes
def normalizeNote(note):
    if len(note) == 2:
        return note[0]
    else:
        return note[0]+note[1] 

#function to get the note by passing the frequency
def getNote(frequency):
    global notes
    for noteIndex in range(0, len(notes)):
        noteData = notes[noteIndex]
        uppperBoundFrequency = noteData[1] * 1.015
        lowerBoundFrequency = noteData[1] * 0.986
        if frequency >= lowerBoundFrequency and frequency <= uppperBoundFrequency:
            return noteData[0]
    return ''

#function to record audio and convert to wav file
def record_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    audio.terminate()

    wave_file = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(audio.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()

#note detecton function using fast fourier transform
def detect(detected_notes_label):

    fileSampleRate, signal = wavfile.read("file.wav")
    if len(signal.shape) == 2:
        signal = signal.sum(axis=1) / 2
    N = signal.shape[0] 
    seconds = N / float(fileSampleRate) 
    timeSamplesPerSecond = 1.0 / fileSampleRate
    timeVector = scipy.arange(0, seconds, timeSamplesPerSecond)
    fft = abs(scipy.fft.fft(signal))
    fftOneSide = fft[range(N // 2)]
    fftFrequencies = scipy.fftpack.fftfreq(signal.size, timeVector[1] - timeVector[0])
    fftFrequenciesOneSide = fftFrequencies[range(N // 2)]

    realAbsoluteValues = abs(fftOneSide)
    normalizedAbsoluteValues = abs(fftOneSide) / numpy.linalg.norm(abs(fftOneSide))
    x = []
    y = []
    yRealValues = []
    recordedNotes = []
    for frequencyIndex in range(0, len(fftFrequenciesOneSide)):
        if fftFrequenciesOneSide[frequencyIndex] >= 110 and fftFrequenciesOneSide[frequencyIndex] <= 8200:
            x.append(fftFrequenciesOneSide[frequencyIndex])
            y.append(normalizedAbsoluteValues[frequencyIndex])
            yRealValues.append(realAbsoluteValues[frequencyIndex])
            if normalizedAbsoluteValues[frequencyIndex] > 0.200:
                note = getNote(fftFrequenciesOneSide[frequencyIndex])
                if note != '':
                    generalizedNote = normalizeNote(note)
                    if generalizedNote not in recordedNotes:
                        recordedNotes.append(generalizedNote)
    
    # Instead of updating the label directly, put the detected notes in a queue
    detected_notes_label.config(text="Detected Note: " + ','.join(map(str, recordedNotes)))
 

#function to conitnuously perform the process using threads
def continuous_record_and_detect(detected_notes_label):
    while True:  # Infinite loop for continuous recording and detection
        record_audio()
        detected_notes = detect(detected_notes_label)
        
        # Use the main thread to update the label
        root.after(0, lambda: detected_notes_label.config(text="Detected Note: " + ', '.join(map(str, detected_notes))))
        time.sleep(1)
    

root = Tk()
root.title("Note Detector")
root.iconbitmap(r"music (1).ico")
root.geometry("620x405")

bg=PhotoImage(file=r"music-mind-music-abstract-art-created-with-generative-ai-technology_545448-15311.png")
canvas1 = Canvas( root, width = 400, 
                 height = 400) 
  
canvas1.pack(fill = "both", expand = True) 
  
# Display image 
canvas1.create_image( 0, 0, image = bg,  anchor = "nw") 
  
def open_recording_window():
    recording_window = Toplevel(root)
    recording_window.title("Recording & Display section")
    recording_window.geometry("510x310")

    canvas = Canvas(recording_window, width=500, height=300)
    canvas.pack()

    # Load the background image for the recording window
    recording_window.background_image_recording = PhotoImage(file=r"abstract-watercolor-guitar-exploding-with-colorful-motion-generated-by-ai_188544-19725.png")

    # Display the background image on the Canvas
    canvas.create_image(0, 0, anchor="nw", image=recording_window.background_image_recording)

    custom_font=("Times New Roman",12,"bold")

    instruction_label = Label(recording_window, text="Recording in progress...", bd=2, relief="raised", highlightbackground="grey",font=custom_font,bg="PaleTurquoise")
    instruction_label.pack(pady=10)
    instruction_label.place(x=300,y=15)

    detected_notes_var = StringVar()
    detected_notes_label = Label(recording_window, text="Detected Note : ", bd=2, relief="raised", highlightbackground="grey", width=20,font=custom_font,bg="Khaki")
    detected_notes_label.pack( pady=10)
    detected_notes_label.place(x=290,y=70)

    stop_button = Button(recording_window, text="Stop Recording", command=recording_window.destroy, bg="pink",font=custom_font)
    stop_button.pack(pady=20, ipadx=20, ipady=10)
    stop_button.place(x=320,y=250)
     # Start continuous recording and detection in a separate thread
    threading.Thread(target=continuous_record_and_detect, args=(detected_notes_label,)).start()



FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 88200
CHUNK = 5012
RECORD_SECONDS = 3.5
WAVE_OUTPUT_FILENAME = "file.wav"

custom_font=("Times New Roman",11,"bold")
instruction_label = Label(root, text="Press the button to record", bd=2, relief="raised", highlightbackground="grey",fg="white",bg="black",font=custom_font)
instruction_label.pack(pady=10)
instruction_label.place(x=5,y=245)

photo = PhotoImage(file=r"music.png")
resized_photo = photo.subsample(8,12)

button_rec = Button(root, text="Record", image=resized_photo, compound=TOP, command=open_recording_window, bg="gold",relief="raised",font=custom_font)
button_rec.pack(padx=20, pady=20, ipadx=20, ipady=20)
button_rec.place(x=54,y=280)

root.mainloop()
