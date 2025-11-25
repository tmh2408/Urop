from generator import generate_code_baseline
from output_store import save_run

def main():
    prompt = "Write a function to return the sum of all elements in a list of integers.(have a syntax error)"

    code = generate_code_baseline(prompt)

    print("=== GENERATED CODE ===")
    print(code)

    save_run(prompt, code)
    print("\nSaved to outputs/runs.jsonl")

if __name__ == "__main__":
    main()
