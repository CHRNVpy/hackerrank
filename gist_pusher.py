import requests
import json

with open('reports.json', 'r') as file:
    data = json.load(file)

ext = {
    "Python3": [".py"], "Java8": [".java"], "JavaScript": [".js"], "C": [".c"], "C++": [".cpp"], "C#": [".cs"],
    "Go": [".go"], "Ruby": [".rb"], "Swift": [".swift"], "Kotlin": [".kt"], "PHP": [".php"], "HTML": [".html"],
    "CSS": [".css"], "TypeScript": [".ts"], "R": [".r"], "SQL": [".sql"], "Perl": [".pl"], "Scala": [".scala"],
    "Lua": [".lua"], "MATLAB": [".m"], "Objective-C": [".m"], "Visual Basic": [".vb"], "Haskell": [".hs"],
    "Shell": [".sh"], "PowerShell": [".ps1"], "Dart": [".dart"], "Assembly": [".asm"], "Rust": [".rs"],
    "Elixir": [".ex"], "Erlang": [".erl"], "Julia": [".jl"], "Groovy": [".groovy"], "CoffeeScript": [".coffee"],
    "D": [".d"], "OCaml": [".ml"]
}

for report in data:
    test_id = report.get('test_id')
    candidate_test_id = report.get('candidate_test_id')
    score1 = report.get('question_1').get('score')
    code_language1 = report.get('question_1').get('code_language')
    code1 = report.get('question_1').get('candidate_code')
    score2 = report.get('question_2').get('score')
    code_language2 = report.get('question_2').get('code_language')
    code2 = report.get('question_2').get('candidate_code')
    if report.get('question_1').get('code_language'):
        file_extension = ext.get(code_language1)[0].strip()
    elif report.get('question_2').get('code_language'):
        file_extension = ext.get(code_language2)[0].strip()
    else:
        file_extension = '.None'


    url = "https://api.github.com/gists"
    headers = {
        "Authorization": "token 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",
        "Content-Type": "application/json"
    }
    info = {
        "accept": "application/vnd.github+json",
        "description": f"Report {test_id}",
        "public": True,
        "files": {
            f"{test_id}-{candidate_test_id}{file_extension}": {
                "content": f'QUESTION 1:\n'
                           f'Score: {score1}\n'
                           f'Programming Language: {code_language1}\n'
                           f'{code1}\n'
                           f'\n'
                           f'QUESTION 2:\n'
                           f'Score: {score2}\n'
                           f'Programming Language: {code_language1}\n'
                           f'{code1}\n'
            }
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(info))
    if response.status_code == 201:
        print("Gist created:", response.json()["html_url"])
    else:
        print("Failed to create Gist:", response.content)
