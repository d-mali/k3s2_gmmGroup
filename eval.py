import soundfile as sf
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import argparse

def parse_transcription(wav_file):
    # load pretrained model
    processor = Wav2Vec2Processor.from_pretrained("addy88/wav2vec2-english-stt")
    model = Wav2Vec2ForCTC.from_pretrained("addy88/wav2vec2-english-stt")
    # load audio
    audio_input, sample_rate = sf.read(wav_file)
    # Ensure tensors are returned in PyTorch format
    input_values = processor(audio_input, sampling_rate=sample_rate, return_tensors="pt").input_values
    # INFERENCE
    # retrieve logits & take argmax
    with torch.no_grad():
        logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    # transcribe
    transcription = processor.decode(predicted_ids[0], skip_special_tokens=True)
    print(transcription)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio using Wav2Vec2 model.")
    parser.add_argument("wav_file", type=str, help="Path to the input WAV file.")
    args = parser.parse_args()

    parse_transcription(args.wav_file)
