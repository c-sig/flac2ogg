import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

DEFAULT_QUALITY = 6.0
MAX_BITRATE = 192000


class FlacConverter:
    def __init__(self, master):
        self.master = master
        master.title("FLAC to Vorbis Converter")
        tk.Label(master, text="Select a FLAC file to convert:").pack()
        tk.Button(master, text="Select File", command=self.select_file).pack()

    def select_file(self):
        filetypes = (("FLAC files", "*.flac"), ("All files", "*.*"))
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a file", filetypes=filetypes)
        if filename:
            self.convert_file(filename)

    def convert_file(self, filename):
        output_filename = os.path.splitext(filename)[0] + ".ogg"
        temp_filename = os.path.splitext(filename)[0] + "_temp.flac"
        command = [
            'ffmpeg', '-y', '-i', filename, '-af', 'adelay=200|200', '-c:a', 'flac', '-ar', '48000', temp_filename
        ]
        subprocess.run(command, check=True)
        quality = DEFAULT_QUALITY
        step_size = 0.2  # Starting step size
        min_step_size = 0.000001  # Minimum step size
        while True:
            command = [
                'ffmpeg', '-y', '-i', temp_filename, '-map', '0:a', '-c:a',
                'libvorbis', '-q:a', f'{quality:.4f}', '-ar', '48000', output_filename
            ]
            subprocess.run(command, check=True)
            actual_bitrate = int(
                subprocess.check_output([
                    'ffprobe', '-v', '0', '-show_entries', 'format=bit_rate',
                    '-of', 'compact=p=0:nk=1', output_filename
                ])
            )
            if actual_bitrate < 191500:
                quality += step_size
            elif actual_bitrate > 192000:
                quality -= step_size
            else:
                break
            step_size = max(step_size * 0.9, min_step_size)  # Decrease step size
        os.remove(temp_filename)
        messagebox.showinfo(
            "Conversion complete",
            f"{filename} has been converted to {output_filename} with a bitrate of {actual_bitrate / 1000:.1f} kbps "
            f"and a quality of {quality:.4f}"
        )


root = tk.Tk()
app = FlacConverter(root)
root.mainloop()
