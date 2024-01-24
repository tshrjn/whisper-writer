from whispercpp import Whisper as WhisperCPP

# List of model names:
# large corresponds to largev3
WHISPER_MODEL = "tiny.en"  # large

w = WhisperCPP.from_pretrained("tiny.en")


def transcribe_from_file(audio_model_cpp, audio_file, sample_rate):
    """
    For WhisperCPP
    """
    import ffmpeg
    import numpy as np

    y, _ = (
        ffmpeg.input(audio_file, threads=0)
        .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=sample_rate)
        .run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True)
    )

    arr = np.frombuffer(y, np.int16).flatten().astype(np.float32) / 32768.0
    ret = audio_model_cpp.transcribe(arr)
    return ret


def apply_whispercpp(filepath: str, mode: str) -> str:
    if mode not in ("transcribe"):
        raise ValueError(f"Invalid mode: {mode}")

    response = w.transcribe_from_file(filepath)
    transcript = response.strip()

    return transcript
