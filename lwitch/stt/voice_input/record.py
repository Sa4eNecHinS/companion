import sounddevice as sd
import wavio


def record(
    path: str,
    duration: int,
    freq: int | None = 48_000,  # fifine's hz
    device: str | None = "Fifine Microphone Mono",
    dtype: str | None = "int16",
) -> bool:
    if duration < 0:
        return False

    if not path:
        return False

    try:
        recording = sd.rec(
            # общее число кадров за продолжительность duration
            int(duration * freq),
            # samplerate позволяет записать звуки определенной freq без искажений
            samplerate=freq,
            channels=1,  # количество каналов для записи
            device=device,
            dtype=dtype,  # тип данных для записи
        )
        sd.wait()
        wavio.write(
            file=f"{path}/record.wav",
            data=recording,  # массив со звуком (кадры и столбцы)
            rate=freq,  # частота дискретизации
            sampwidth=2,  # глубина звука (2 отлично сочетается с int16)
        )

        print(recording.min())
        print(recording.max())
        print(recording.shape)

        return True

    except KeyboardInterrupt:
        pass


def check_device_features() -> dict:
    features = {}
    for num_d, feat_d in enumerate(sd.query_devices()):
        features[num_d] = feat_d

    return features


if __name__ == "__main__":
    print("Start recording ...")
    path = "/home/a_nyone/apps/ros2_ws/src/lwitch/lwitch/stt"

    if record(path, 3):
        print("Voice input succefully recorded")
    else:
        print("ERROR")

    print("\nChecking device features ...")
    for num, ftr in check_device_features().items():
        print(num, " | ", ftr)
        print("-" * 97)
