#!/usr/bin/env python

import os
import sys
import requests
from bs4 import BeautifulSoup
import yaml
import zipfile
import io
import shutil

def download_problem_tests(problem_id, problem_folder):
	url = f"https://open.kattis.com/problems/{problem_id}/file/statement/samples.zip"

	response = requests.get(url)
	# We may not have tests
	if response.status_code != 200:
		return

	test_folder = os.path.join(problem_folder, "tests")
	os.makedirs(test_folder)
	with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zip:
		zip.extractall(test_folder)


def get_kattis_problem_metadata(problem_id):
	url = f"https://open.kattis.com/problems/{problem_id}"

	response = requests.get(url)

	html = BeautifulSoup(response.text, "html.parser")

	title = html.find("h1", class_="book-page-heading").get_text()

	metadata_grid = html.find("div", class_="metadata-grid")
	difficulty = float(metadata_grid.select_one(f"span[class*=\"difficulty_number\"]").get_text())

	return {
		"title": title,
		"difficulty": difficulty,
		"url": url,
	}

def generate_readme(metadata_file, output_file="README.md"):
	with open(metadata_file, "r") as f:
		data = yaml.safe_load(f)

	solved = data.get("solved", 0)
	attempted = data.get("attempted", 0)
	problems = data.get("problems", {})

	readme	= "# Swimotter's Kattis Tracker\n"
	readme += "Solutions to problems from the [Kattis archives](https://open.kattis.com/)\n\n"

	solved_problems = []
	attempted_problems = []
	for _, metadata in problems.items():
		title = metadata.get("title", "")
		difficulty = metadata.get("difficulty", 0)
		url = metadata.get("url", "")
		solution = metadata.get("solution", "")

		is_solved = metadata.get("solved", False)
		if is_solved:
			solved_problems.append({"title": title, "difficulty": difficulty, "url": url, "solution": solution})
		else:
			attempted_problems.append({"title": title, "difficulty": difficulty, "url": url, "solution": solution})

	solved_problems = sorted(solved_problems, key=lambda problem: problem["difficulty"], reverse=True)
	attempted_problems = sorted(attempted_problems, key=lambda problem: problem["difficulty"], reverse=True)

	readme += f"## Solved Problems ({solved})\n"
	readme += "| Solution | Difficulty | :link: |\n"
	readme += "| - | - | - |\n"
	for problem in solved_problems:
		readme += f"| [{problem["title"]}]({problem["solution"]}) | {problem["difficulty"]} | [![](https://open.kattis.com/favicon)]({problem["url"]}) |\n"

	readme += "\n"
	if len(attempted_problems) > 0:
		readme += f"## Attempted Problems ({attempted - solved})\n"
		readme += "| Attempt | Difficulty | :link: |\n"
		readme += "| - | - | - |\n"
		for problem in attempted_problems:
			readme += f"| [{problem["title"]}]({problem["solution"]}) | {problem["difficulty"]} | [![](https://open.kattis.com/favicon)]({problem["url"]}) |\n"

	with open(output_file, 'w') as f:
		f.write(readme)

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print(f"Usage: {sys.argv[0]} <problemId> <problems_folder> [metadata_file]")
		sys.exit(2)

	problem_id = sys.argv[1]
	problems_folder = sys.argv[2]
	problem_folder = os.path.join(os.curdir, problems_folder, problem_id)

	if os.path.exists(problem_folder):
		print(f"Problem folder already exists", file=sys.stderr)
		sys.exit(1)

	url = f"https://open.kattis.com/problems/{problem_id}"
	response = requests.get(url)
	if response.status_code != 200:
		print(f"Problem ID '{problem_id}' not found", file=sys.stderr)
		sys.exit(1)

	template_file = os.path.join(os.curdir, "template.cpp")
	solution_file = os.path.join(problem_folder, f"{problem_id}.cpp")
	shutil.copyfile(template_file, solution_file)

	download_problem_tests(problem_id, problem_folder)

	if len(sys.argv) == 3:
		sys.exit(0)
	metadata_file = os.path.join(os.curdir, sys.argv[3])
	metadata = get_kattis_problem_metadata(problem_id)
	metadata["solution"] = problem_folder
	metadata["solved"] = False

	with open(metadata_file, "r") as f:
		data = yaml.safe_load(f)
	data["attempted"] += 1
	data["problems"][problem_id] = metadata
	with open(metadata_file, "w") as f:
		yaml.dump(data, f, sort_keys=False)

	generate_readme(metadata_file)
