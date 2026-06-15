from pynput import keyboard
import spotify_func

def on_press(key):
    try:
        if not hasattr(key, 'char'):
            pass
            
        elif key.char == 'a':
            print("a was pressed")
            track_id = spotify_func.get_curr_track(access_token)
            playlist_id = spotify_func.create_playlist("test", access_token)
            spotify_func.add_track(track_id, playlist_id, access_token)

    except:
        print("invalid input (what did you press?): {}".format(key))

def on_release(key):
    # print('{} released; it was {}'.format(
    #     key, 'faked' if injected else 'not faked'))
    if key == keyboard.Key.esc:
        # Stop listener if escape key is pressed
        return False

[auth_code, refresh_token, access_token] = spotify_func.authorize_user()
# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
