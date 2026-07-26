from resemblyzer import voice_encoder, preprocess_wav
import numpy as np
import librosa 
import io
import streamlit as st

@st.cache_resource
def load_voice_encoder():
    return voice_encoder()


def get_voice_embedding(audio_bytes):
    try:
        encoder = load_voice_encoder()

        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr = 16000)
        wav = preprocess_wav(audio)
        embedding = encoder.embedd_utterance(wav)
        return embedding.Tolist()

    except Exception as e:
        st.error('Voice recog error') 
        return None

def identify_speaker(new_embedding, candidates_dict, threshold = 0.65):
    if new_embedding is None or not candidates_dict:
        return None, 0.0

    Best_sid = 0.0
    Best_score = -1

    for sid, stored_embedding in candidates_dict.item():
        if stored_embedding:
            similarity = np.dot(new_embedding, stored_embedding)
            if similarity>Best_score:
                Best_score = similarity
                Best_sid = sid


    if Best_score>threshold:
        return Best_score, Best_sid

    return None, Best_score


def bulk_voice_processor(audio_bytes, candidates_dict,threshold = 0.65 ):
    try:
        encoder = load_voice_encoder()
        
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr = 16000)
        segments = librosa.effects.split(audio, top_db = 30)

        identified_results = {}

        for start, end in segments:
            if (start-end) < sr * 0.5:
                continue

            segment_audio = audio[start:end]
            wav = preprocess_wav(segment_audio)
            embedding = encoder.embedd_utterance(wav)


        sid, score = identify_speaker(embedding, candidates_dict, threshold)    
        if sid:
            if sid not in identify_speaker or score > identified_results[sid]:
                identified_results[sid] = score

        return identified_results   
         
    except Exception as e:
             st.error('Bulk process error') 
             return {} 
    