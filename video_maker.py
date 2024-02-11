import cv2
from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_audioclips
from gtts import gTTS

SILENCE = 'sound_effect/silence.mp3'

def audio_maker(text,lang,path):

    tts = gTTS(text=text, lang=lang)
    tts.save(f"{path}/{lang}.mp3")

def video_maker(image_path, audio_path, output_video_path):
    
    # Chargement de l'image
    image = cv2.imread(image_path)
    height, width, layers = image.shape

    # Lecture des fichiers audio
    audio_clip_1 = AudioFileClip(SILENCE)
    audio_clip_2 = AudioFileClip(audio_path)

    # Concaténation des clips audio
    combined_audio_clip = concatenate_audioclips([audio_clip_1, audio_clip_2])

    # Paramètres de la vidéo
    # La durée de la vidéo doit être au moins égale à celle de l'audio
    video_duration = max(8, combined_audio_clip.duration)
    fps = 1  # 1 image par seconde

    # Création de la vidéo avec OpenCV
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # Écriture de l'image dans le flux vidéo pour la durée spécifiée
    for _ in range(int(video_duration * fps)):  # Convertir en entier pour éviter les erreurs
        video_writer.write(image)

    # Libération du VideoWriter
    video_writer.release()

    # Chargement de la vidéo dans MoviePy
    video_clip = VideoFileClip(output_video_path)

    # Association du clip audio combiné à la vidéo
    final_clip = video_clip.set_audio(combined_audio_clip)

    # Exportation de la vidéo finale avec l'audio combiné
    final_clip.write_videofile(
        output_video_path, codec='libx264', audio_codec='aac', fps=fps)


