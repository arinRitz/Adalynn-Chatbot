import numpy as np
import matplotlib.backends.backend_tkagg as tkagg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk
import vosk
import pyaudio
import webbrowser
import json
import pyttsx3

def exit_application():
    root.destroy()


# initialization of speak
# initialization of speak function
engine = pyttsx3.init()
# Set properties (optional)
engine.setProperty('rate', 150)  # Speed of speech (words per minute)
engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
# Get a list of available voices
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')

def speak(text):
    engine.say(text)
    engine.runAndWait()
    # end of speak func

speak("Hello Boss Adalynn Here")
print("Hello Boss Adalynn Here")
speak("How may I help You Today")
print("How may I help You Today")

# Set the path to the Vosk model directory
model_path = 'C:/Users/ahsan/Desktop/New folder/vosk-model-en-in-0.5/vosk-model-en-in-0.5'

# Initialize Vosk with the specified model path
vosk.SetLogLevel(-1)
model = vosk.Model(model_path)
recognizer = vosk.KaldiRecognizer(model, 16000)

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Start a Tkinter window
root = tk.Tk()
root.title("Adlynn")

# Remove title bar and make window non-resizable
root.overrideredirect(True)
root.resizable(False, False)

# Calculate the screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the window dimensions
window_width = 400
window_height = 300

# Calculate the position to center the window
x_offset = (screen_width - window_width) // 2
y_offset = (screen_height - window_height) // 2

# Set window size and position
root.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")

# Create a canvas to display the animation
canvas = tk.Canvas(root, width=window_width, height=window_height)
canvas.pack()

# Create a text box to display voice and text input
text_box = tk.Text(root, height=10, width=50)
text_box.pack()

# Create a figure and axis with fixed aspect ratio
fig, ax = plt.subplots(figsize=(6, 4))

# Set the axis limits
ax.set_xlim(0, 2*np.pi)
ax.set_ylim(-2, 2)

# Initialize two lines with light green and light blue colors and thicker lines
line1, = ax.plot([], [], lw=5, color='lightgreen')
line2, = ax.plot([], [], lw=5, color='lightblue')

# Remove the axes points (ticks)
ax.set_xticks([])
ax.set_yticks([])

# Initialization function: plot the background of each frame
def init():
    line1.set_data([], [])
    line2.set_data([], [])
    return line1, line2

# Animation function: update the lines with each frame
def animate(i):
    x = np.linspace(0, 2*np.pi, 100)
    # Calculate the phase shift to create the forward and reverse motion
    phase_shift_forward = i * np.pi / 5  # Increase the frequency
    phase_shift_reverse = (100 - i) * np.pi / 5  # Increase the frequency
    # Calculate y values for forward and reverse motion
    y1_forward = np.sin(x + phase_shift_forward)
    y2_forward = np.sin(x - phase_shift_forward)
    y1_reverse = np.sin(x + phase_shift_reverse)
    y2_reverse = np.sin(x - phase_shift_reverse)
    # Set data based on the direction of motion
    if i < 50:
        line1.set_data(x, y1_forward)
        line2.set_data(x, y2_forward)
    else:
        line1.set_data(x, y1_reverse)
        line2.set_data(x, y2_reverse)
    return line1, line2

# Create the animation with fewer frames to speed up
ani = FuncAnimation(fig, animate, frames=400, init_func=init, blit=True)

# Convert the Matplotlib figure to a Tkinter-compatible canvas
canvas = tkagg.FigureCanvasTkAgg(fig, master=canvas)
canvas.draw()

# Pack the canvas into the Tkinter window
canvas.get_tk_widget().pack()

# Function to listen and recognize speech
def listen_and_recognize():
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)

    while True:
        try:
            data = stream.read(8000)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                if 'text' in result:
                    command = result['text'].lower()
                    print("You said:", command)
                    text_box.insert(tk.END, f"You said: {command}\n")
                    text_box.see(tk.END)  # Scroll to the bottom

                    if "open website" in command:
                        speak("Opening website")
                        webbrowser.open("https://www.example.com")  # Change the URL as needed

                    elif "open gym" in command:
                        print("Ahsan")

        except KeyboardInterrupt:
            print("Stopping...")
            break

    stream.stop_stream()
    stream.close()
    audio.terminate()

# Start listening and recognizing speech (in a separate thread)
root.after(100, listen_and_recognize)

# Run the Tkinter event loop
root.mainloop()
