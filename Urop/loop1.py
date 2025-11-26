
import ast
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# 1) Load API key từ API.env (nằm cùng thư mục với file .py)
env_path = Path(__file__).resolve().parent / "API.env"
load_dotenv(env_path, override=True)

client = OpenAI()


def loop_syntax_fix(code: str, max_retries: int = 3) -> str:
    """
    Loop 1: kiểm tra và sửa lỗi cú pháp (SyntaxError) của code Python.
    - code: chuỗi Python code do LLM tạo ra
    - max_retries: số lần tối đa cho LLM sửa

    Trả về: code đã được sửa (hoặc code gốc nếu ngay từ đầu đã không lỗi).
    """

    for attempt in range(max_retries):
        try:
            # Thử parse code. Nếu không lỗi -> return luôn
            ast.parse(code)
            # Nếu parse thành công -> không còn SyntaxError
            return code

        except SyntaxError as e:
            # Nếu đã hết số lần sửa thì dừng, báo lỗi
            if attempt == max_retries - 1:
                raise RuntimeError(
                    f"Loop 1: Hết số lần sửa nhưng vẫn SyntaxError: {e}"
                )

            # Tạo prompt nhờ LLM sửa code
            repair_prompt = (
                "The following Python code has a syntax error.\n\n"
                f"Error:\n{e}\n\n"
                "Code:\n"
                f"{code}\n\n"
                "Please fix ONLY the syntax error(s) and return ONLY corrected "
                "Python code.\n"
                "No explanation, no comments, no markdown.\n"
            )

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert Python programmer. "
                            "You fix syntax errors in Python code. "
                            "Return ONLY valid runnable Python code."
                        ),
                    },
                    {"role": "user", "content": repair_prompt},
                ],
                temperature=0,
            )

            # Cập nhật code để thử lại ở vòng lặp tiếp theo
            code = response.choices[0].message.content.strip()

    # Về lý thuyết sẽ không tới đây (vì hoặc return, hoặc raise)
    return code
