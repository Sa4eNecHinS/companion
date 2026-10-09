from faster_whisper import WhisperModel

model_size = "base"
# run on CPU with INT8
model = WhisperModel(model_size, device="cpu", compute_type="int8")
# model = WhisperModel(model_size, device="cuda", compute_type="float16")


def speak_to_text(path_to_file: str) -> dict:
    info = {}
    full_text = ""
    segments, information = model.transcribe(path_to_file)

    info["language"] = information.language
    info["language_probability"] = information.language_probability

    # turns to list, cause whisper breaks down long text into segments
    # -> [0] - speak starts
    # -> [-1] - speak ends
    list_segments = list(segments)

    if list_segments:
        info["start_record"] = list_segments[0].start
        info["end_record"] = list_segments[-1].end
        full_text = " ".join([segment.text for segment in list_segments])

    info["text"] = full_text.strip()

    return info


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Transcribe an audio file locally.")
    parser.add_argument("path", help="Path to an audio file")
    path = parser.parse_args().path

    txt = speak_to_text(path)
    print(
        f"""Language is {txt.get("language", None)}, with probability {
            txt.get("language_probability", None)
        }"""
    )
    print(
        f"""[{txt.get("start_record", None)} -> {txt.get("end_record", None)}] {
            txt.get("text", None)
        }"""
    )
