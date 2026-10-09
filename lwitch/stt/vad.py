from silero_vad import load_silero_vad, read_audio, get_speech_timestamps


def vad(path: str):
    model = load_silero_vad()
    wav = read_audio(path)
    speech_timestamps = get_speech_timestamps(
        wav,
        model,
        # Return speech timestamps in seconds (default is samples)
        return_seconds=True,
    )
    return speech_timestamps


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Detect speech in an audio file.")
    parser.add_argument("path", help="Path to an audio file")
    res = vad(parser.parse_args().path)
    print(res)
