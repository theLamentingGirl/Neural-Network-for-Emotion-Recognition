#importing libraries 
import os
# import torchvision 
# import torch
import re

def extract_emotion_label(file_path, name, video_frames, video_fps):
    
    label_path = os.path.join(file_path, 'dialog/EmoEvaluation')
    file = open(os.path.join(label_path, name[:-4]+'.txt'), 'r')
    content = file.read()
    
    timestamps = re.findall('\[\d*\W\d{4}\s-\s\d*\W\d{4}\]', content)
    emotion_label = re.findall('\t\w{3}\t', content)
    emotion_label = [i[1:-1] for i in emotion_label]
    
    characters = re.findall('[_][MF]\d', content)
    unique_char, data, vlabel_data = [], {}, {}
    for char in characters:
        if char not in unique_char:
            unique_char.append(char[1])
            data[char[1]] = []
            vlabel_data[char[1]] = []
    
    video_duration = video_frames/video_fps ### in seconds
    
    if (len(timestamps) == len(emotion_label)) and (len(timestamps) == len(characters)):
        for char, stamp, emotion in zip(characters, timestamps, emotion_label):
            duration = re.findall('\d*\W\d{4}', stamp)
            start, end = float(duration[0]), float(duration[1])
            data[char[1]].append([start, end, emotion])
    
    
    for char in data:
        last_end = 0
        for info in data[char]:
            start, end, emotion = info
            
            frames_unknown = round((start - last_end) * video_fps)
            vlabel_data[char] += ['xxx' for i in range(frames_unknown)]
            
            frames_known = round((end - start) * video_fps)
            vlabel_data[char] += [emotion for i in range(frames_known)]
            
            last_end = end
            
        if last_end < video_duration:
            #frames_remaining = round((video_duration - last_end) * video_fps)
            frames_remaining = video_frames - len(vlabel_data[char])
            vlabel_data[char] += ['xxx' for i in range(frames_remaining)]
    
    return vlabel_data

def video_processing(video_data):
    pass


data_directory = './Dataset/' ### path to EMOCAP data
class_label = {'xxx' : 0, 'fru' : 1, 'ang' : 2, 'neu' : 3, 'sur' : 4, 'sad' : 5, 'exc' : 6, 'hap' : 7}

for session_number in range(1, 6):
    file_path = os.path.join(data_directory, f'IEMOCAP_full_release/Session{session_number}')
    video_path = os.path.join(file_path, 'dialog/avi/DivX/')
    
    for name in os.listdir(video_path):
        if name[-4:] == '.avi':
            train_data = torchvision.io.read_video(os.path.join(video_path, name))
            vlabel_data = extract_emotion_label(file_path=file_path, 
                                                name=name, 
                                                video_frames=train_data[0].shape[0], 
                                                video_fps=train_data[2]['video_fps'])
            print(train_data[0].shape[0])
            for i in vlabel_data:
                print(len(vlabel_data[i]))
            break
    break

