import winsound 

def play_music():
    winsound.PlaySound(
        r"Resources\images\TUNIC  - Lifeformed.wav",
        winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC
    )
def stop_music():
    winsound.PlaySound(None, winsound.SND_PURGE)