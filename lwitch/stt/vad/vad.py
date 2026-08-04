from silero_vad import load_silero_vad, read_audio, get_speech_timestamps


def vad():
    model = load_silero_vad()
    wav = read_audio("/home/a_nyone/apps/ros2_ws/src/lwitch/lwitch/stt/record.wav")
    speech_timestamps = get_speech_timestamps(
        wav,
        model,
        # Return speech timestamps in seconds (default is samples)
        return_seconds=True,
    )
    return speech_timestamps


if __name__ == "__main__":
    res = vad()
    print(res)
