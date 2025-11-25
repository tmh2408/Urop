import json
from pathlib import Path
from datetime import datetime

def save_run(prompt: str, code: str, model: str = "gpt-4o-mini", temperature: float = 0):
    """
    Lưu mỗi lần generate thành 1 record JSONL (1 dòng / 1 run).
    File output: outputs/runs.jsonl
    """
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)

    record = {
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "model": model,
        "temperature": temperature,
        "code": code
    }

    with open(out_dir / "runs.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
