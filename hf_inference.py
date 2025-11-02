# hf_inference.py
import os, time, requests

HF_MODEL = os.environ.get("HF_MODEL", "sshleifer/distilbart-cnn-12-6")
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
HF_TOKEN = os.environ.get("HF_API_TOKEN")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

def _call_hf(inputs, max_length=200, min_length=60):
    payload = {
        "inputs": inputs,
        "parameters": {
            "max_length": max_length,
            "min_length": max(0, min(min_length, max_length - 10)),
            "do_sample": False
        },
        "options": {"wait_for_model": True}
    }
    for _ in range(10):
        r = requests.post(HF_API_URL, headers=HEADERS, json=payload, timeout=60)
        if r.status_code == 503:
            # model loading on HF – backoff
            try:
                wait = int(r.json().get("estimated_time", 5)) + 1
            except Exception:
                wait = 5
            time.sleep(min(wait, 15))
            continue
        r.raise_for_status()
        data = r.json()
        if isinstance(data, list) and data and "summary_text" in data[0]:
            return data[0]["summary_text"]
        if isinstance(data, dict) and data.get("error"):
            raise RuntimeError(data["error"])
        return str(data)
    raise TimeoutError("HF model never became ready")

def _chunks(words, size):
    for i in range(0, len(words), size):
        yield " ".join(words[i:i+size])

def summarize_text(text, max_length=200, min_length=60):
    text = (text or "").strip()
    if not text:
        return ""
    words = text.split()
    if len(words) <= 650:
        return _call_hf(text, max_length, min_length)
    partials = []
    for chunk in _chunks(words, 650):
        partials.append(_call_hf(chunk, max_length, min_length))
        time.sleep(0.2)  # gentle pacing
    combined = " ".join(partials)
    return _call_hf(combined, max_length, min_length)