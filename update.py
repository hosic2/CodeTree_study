import os
from urllib.parse import quote
import re

HEADER = """#
# 코드트리 문제 풀이 목록
// 여기에 실력진단을 넣어주면 귀엽게 구현이 된다.
## 🌳 코드트리 문제 목록
"""

SUPPORTED_LANGUAGES = {
    "Python": ".py",
    "Java": ".java",
    "C++": ".cpp",
    "JavaScript": ".js",
    "C": ".c",
    "Ruby": ".rb",
    "Go": ".go",
    "Kotlin": ".kt",
    "Swift": ".swift",
    "Rust": ".rs"
}

DIFFICULTY_IMAGES = {
    "쉬움": "https://img.shields.io/badge/쉬움-%235cb85c.svg?for-the-badge",
    "보통": "https://img.shields.io/badge/보통-%23FFC433.svg?for-the-badge",
    "어려움": "https://img.shields.io/badge/어려움-%23D24D57.svg?for-the-badge",
    "easy": "https://img.shields.io/badge/easy-%235cb85c.svg?for-the-badge",
    "medium": "https://img.shields.io/badge/medium-%23FFC433.svg?for-the-badge",
    "hard": "https://img.shields.io/badge/hard-%23D24D57.svg?for-the-badge"
}

DIFFICULTY_EMOJIS = {
    "쉬움": "🟢",
    "보통": "🟡",
    "어려움": "🔴"
}

DIFFICULTY_MAP = {
    "쉬움": "쉬움",
    "보통": "보통",
    "어려움": "어려움",
    "easy": "쉬움",
    "medium": "보통",
    "hard": "어려움"
}

def get_language_from_extension(file_name):
    for language, ext in SUPPORTED_LANGUAGES.items():
        if file_name.lower().endswith(ext):
            return language
    return None

def extract_problem_difficulty(readme_path):
    problem_difficulty = "쉬움"
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                if "|난이도|" in line:
                    match = re.search(r"\|난이도\|\s*(.*?)\s*\|", line)
                    if match:
                        raw_difficulty = match.group(1).strip().lower()
                        problem_difficulty = DIFFICULTY_MAP.get(raw_difficulty, "쉬움")
    except Exception as e:
        print(f"Error reading {readme_path}: {e}")
    return problem_difficulty

def generate_readme():
    problems_by_difficulty = {
        "쉬움": [],
        "보통": [],
        "어려움": []
    }

    modified = False

    for date_folder in sorted(os.listdir(".")):
        date_path = os.path.join(".", date_folder)
        if not date_folder.isdigit() or len(date_folder) != 6 or not os.path.isdir(date_path):
            continue

        for problem_folder in os.listdir(date_path):
            problem_path = os.path.join(date_path, problem_folder)
            if not os.path.isdir(problem_path):
                continue

            problem_readme = os.path.join(problem_path, "README.md")
            problem_difficulty = extract_problem_difficulty(problem_readme) if os.path.exists(problem_readme) else "쉬움"

            difficulty_image = DIFFICULTY_IMAGES.get(problem_difficulty, DIFFICULTY_IMAGES["쉬움"])

            problem_info = {
                "date": date_folder,
                "folder": problem_folder,
                "difficulty": problem_difficulty,
                "difficulty_image": difficulty_image,
                "path": problem_path
            }

            found_language = None
            for file_name in os.listdir(problem_path):
                language = get_language_from_extension(file_name)
                if language:
                    found_language = language
                    break

            problem_info["language"] = found_language if found_language else "알 수 없음"
            problems_by_difficulty[problem_difficulty].append(problem_info)
            modified = True

    if modified:
        content = HEADER

        for difficulty in ["쉬움", "보통", "어려움"]:
            if problems_by_difficulty[difficulty]:
                emoji = DIFFICULTY_EMOJIS[difficulty]
                content += f"### {emoji} {difficulty}\n"
                content += "| 업로드 날짜 | 문제 폴더 | 언어 | 링크 | 난이도 |\n"
                content += "| ----------- | --------- | ---- | ----- | ------- |\n"
                for problem in problems_by_difficulty[difficulty]:
                    content += f"| {problem['date']} | [{problem['folder']}]({quote(problem['path'])}) | {problem['language']} | [링크]({quote(problem['path'])}) | ![{problem['difficulty']}]({problem['difficulty_image']}) |\n"

        with open("README.md", "w", encoding="utf-8") as fd:
            fd.write(content)
        print("README.md has been updated successfully.")
    else:
        print("No changes were made to README.md.")

if __name__ == "__main__":
    generate_readme()
