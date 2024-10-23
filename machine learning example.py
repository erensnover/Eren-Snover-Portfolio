from google.colab import drive
drive.mount('/content/gdrive')

import IPython.display as ipd
import sys
from resemblyzer import preprocess_wav, VoiceEncoder, normalize_volume, wav_to_mel_spectrogram
from demo_utils import *
import cv2
from PIL import Image
import moviepy.editor as mp
from IPython.display import display
from itertools import groupby
from pathlib import Path
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
import librosa
import pandas as pd
import seaborn as sns

sys.path.append("Resemblyzer")

video_path = '/content/gdrive/MyDrive/coding final/testVideo/Exploiting A Legal Loophole.mp4'
cap = cv2.VideoCapture(video_path)

output_path = 'output.mp4'
fps = cap.get(cv2.CAP_PROP_FPS)
frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
output_video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, frame_size)

video = mp.VideoFileClip(video_path)

wav_fpaths = list(Path("gdrive", "MyDrive", "coding final","trainData").glob("**/*.wav"))

wav_fpaths.sort()

wav_testpaths = list(Path("gdrive", "MyDrive", "coding final","testData").glob("**/*.wav"))

wav_testpaths.sort()

wav_fpaths

wav_testpaths

print(len(wav_fpaths))

encoder = VoiceEncoder()
encoder

speaker_wavs = {speaker: list(map(preprocess_wav, wav_fpaths)) for speaker, wav_fpaths in
                groupby(tqdm(wav_fpaths, "Preprocessing wavs", len(wav_fpaths), unit="wavs"),
                        lambda wav_fpath: wav_fpath.parent.stem)}

test_wavs = {speaker: list(map(preprocess_wav, wav_testpaths)) for speaker, wav_testpaths in
                groupby(tqdm(wav_testpaths, "Preprocessing wavs", len(wav_testpaths), unit="wavs"),
                        lambda wav_testpath: wav_testpath.parent.stem)}

wav_fpaths[0]

wav_fpaths[0].parent.stem

wav_testpaths[0].parent.stem

speaker_wavs

test_wavs

# This is what comes out on the other end:
# speaker_wavs is a dictionary with one key per speaker
# Each item is a list of 10 librosa audio arrays
speaker_wavs

print(sys.version)

spk_embeds = np.array([encoder.embed_speaker(wavs[:len(wavs)-1]) \
                         for wavs in speaker_wavs.values()])

speaker_wavs.values()

print(spk_embeds.shape)

print(spk_embeds)

# Embed the utterance for which we want to determine the speaker
# This is basically the 'test set'
utterance_embed = np.array(encoder.embed_utterance(test_wavs['testData'][0]))

print(utterance_embed.shape)

print(utterance_embed)

#Compare the embedding of the utterance to the speaker embeddings
utt_sim_array = np.inner(spk_embeds, utterance_embed)

spk_embeds.shape

utterance_embed.shape

# These values work like correlations
# The lowest value is 0 (lowest similarity), the highest is 1 (highest similarity)
print(utt_sim_array)

sum(np.square(utterance_embed))

# We could also do this with Pearson's R
from scipy.stats import pearsonr
[pearsonr(utterance_embed,y) for y in spk_embeds]

# Index of the largest similarity
print(np.argmax(utt_sim_array))

# Which speaker does the file belong to?
# Get all the speaker names from the dictionary
speaker_names = speaker_wavs.keys()
# Dictionary keys don't have indices (since dicts used to have no order)
# So we need to turn it into a list first
speaker_names = list(speaker_names)
# Now we can check which speaker name the file belongs to
speaker_names[np.argmax(utt_sim_array)]

text = speaker_names[np.argmax(utt_sim_array)]
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_color = (255, 255, 255)  # White color
thickness = 2
position = (50, 50)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Overlay the text on the frame
    cv2.putText(frame, text, position, font, font_scale, font_color, thickness, cv2.LINE_AA)

    # Write the modified frame to the output video
    output_video.write(frame)

# Release the video capture and output video
cap.release()
output_video.release()

modified_video = mp.VideoFileClip(output_path)
original_audio = mp.VideoFileClip(video_path).audio

# Set the modified video's audio as the original audio
final_video = modified_video.set_audio(original_audio)

final_video.write_videofile('output_with_audio.mp4', codec='libx264', audio_codec='aac')
