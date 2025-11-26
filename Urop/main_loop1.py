# main_loop1.py

import json
from pathlib import Path

from loop1 import loop_syntax_fix


def load_latest_code_from_jsonl(path: str = "outputs/runs.jsonl") -> str:
    """
    Đọc dòng cuối cùng trong file JSONL (run mới nhất)
    và trả về trường 'code'.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Không tìm thấy file {path}")

    lines = p.read_text(encoding="utf-8").strip().splitlines()
    if not lines:
        raise ValueError(f"File {path} rỗng, chưa có run nào.")

    last_record = json.loads(lines[-1])
    if "code" not in last_record:
        raise KeyError("Không tìm thấy field 'code' trong record JSONL.")

    return last_record["code"]


def main():
    # 1) Lấy code LLM mới nhất từ runs.jsonl (baseline code)
    original_code = load_latest_code_from_jsonl()

    # 2) Cho code chạy qua Loop 1: sửa SyntaxError (nếu có)
    fixed_code = loop_syntax_fix(original_code, max_retries=3)

    # 3) In ra so sánh
    print("=== ORIGINAL LLM CODE ===")
    print(original_code)

    print("\n=== CODE AFTER LOOP 1 (SYNTAX FIX) ===")
    print(fixed_code)

    # 4) Lưu ra file để sau này tiện so sánh / dùng tiếp cho loop sau
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)

    (out_dir / "loop1_original_code.py").write_text(original_code, encoding="utf-8")
    (out_dir / "loop1_fixed_code.py").write_text(fixed_code, encoding="utf-8")

    print("\nSaved to:")
    print(" - outputs/loop1_original_code.py")
    print(" - outputs/loop1_fixed_code.py")


if __name__ == "__main__":
    main()
