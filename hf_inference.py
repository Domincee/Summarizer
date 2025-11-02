# hf_inference.py
import os
import time
import requests

# Read token from common env var names and trim whitespace
_raw = (
    os.getenv("HF_API_TOKEN")
    or os.getenv("HUGGING_FACE_HUB_TOKEN")
    or os.getenv("HUGGINGFACEHUB_API_TOKEN")
    or os.getenv("HF_TOKEN")
)
HF_TOKEN = _raw.strip() if _raw else None
if not HF_TOKEN:
    raise EnvironmentError(
        "HF_API_TOKEN not set. Set HF_API_TOKEN=hf_... in your environment "
        "(PowerShell: $env:HF_API_TOKEN='hf_...')."
    )

HF_MODEL = os.getenv("HF_MODEL", "sshleifer/distilbart-cnn-12-6")
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}


def _call_hf(inputs: str, max_length=200, min_length=60) -> str:
    payload = {
        "inputs": inputs,
        "parameters": {
            "max_length": max_length,
            "min_length": max(0, min(min_length, max_length - 10)),
            "do_sample": False,
        },
        "options": {"wait_for_model": True},
    }

    backoff = 5
    for _ in range(10):
        r = requests.post(HF_API_URL, headers=HEADERS, json=payload, timeout=60)
        # Handle model warming
        if r.status_code == 503:
            try:
                wait = int(r.json().get("estimated_time", backoff))
            except Exception:
                wait = backoff
            time.sleep(min(wait + 1, 15))
            continue
        # Handle simple rate limiting
        if r.status_code == 429:
            time.sleep(min(backoff, 15))
            backoff = min(backoff * 2, 30)
            continue

        r.raise_for_status()
        data = r.json()

        # Normal summarization response
        if isinstance(data, list) and data and "summary_text" in data[0]:
            return data[0]["summary_text"]

        # API returned an error payload
        if isinstance(data, dict) and data.get("error"):
            raise RuntimeError(f"Hugging Face API error: {data['error']}")

        # Fallback: return whatever we got, stringified
        return str(data)

    raise TimeoutError("HF model did not become ready after multiple attempts.")


def _chunks(words, size):
    for i in range(0, len(words), size):
        yield " ".join(words[i : i + size])


def summarize_text(text: str, max_length=200, min_length=60) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    words = text.split()

    # Single-shot if small enough
    if len(words) <= 650:
        return _call_hf(text, max_length, min_length)

    # Map-reduce: summarize chunks then summarize the concatenated partials
    partials = []
    for chunk in _chunks(words, 650):
        partials.append(_call_hf(chunk, max_length, min_length))
        time.sleep(0.2)  # gentle pacing
    combined = " ".join(partials)
    return _call_hf(combined, max_length, min_length)


if __name__ == "__main__":
    # Quick manual test:
    sample = "This is a short test paragraph to verify the Hugging Face Inference API call works."
    try:
        print(summarize_text(sample, max_length=40, min_length=10))
    except Exception as e:
        print("Test failed:", e)