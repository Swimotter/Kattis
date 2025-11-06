#!/usr/bin/env python

import sys
import os
from pathlib import Path
import subprocess
import yaml

def test(problem_folder):
	build_dir = os.path.join(os.curdir, "build")
	if not os.path.exists(build_dir):
		os.mkdir(build_dir)

	solution_files = list(Path(problem_folder).glob("*.cpp"))
	compile_command = ["g++", "-g", "-O2", "-std=gnu++20", "-static"]
	compile_command += [str(f) for f in solution_files]
	compile_command += ["-o", "build/soln.exe"]
	compile_result = subprocess.run(
		compile_command,
		capture_output=True,
		text=True
	)
	if compile_result.returncode != 0:
		print("Compilation failed")
		print(compile_result.stderr)
		sys.exit(1)

	test_folder = os.path.join(problem_folder, "test")
	test_files = list(Path(test_folder).glob("*.in"))
	for file in test_files:
		with open(file, "r") as f:
			run_result = subprocess.run(
				["./soln.exe"],
				stdin=f,
				capture_output=True,
				text=True
			)

		solution_file = file.with_suffix(".out")
		solution = solution_file.read_text().strip()
		actual = run_result.stdout.strip()

		if actual != solution:
			print("There was an error with the solution!")
			print("Expected:")
			print(solution)
			print("Got:")
			print(actual)
			return False

	print("All tests passed!")
	return True

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

	if not os.path.exists(problem_folder):
		print(f"Problem folder does not exist", file=sys.stderr)
		sys.exit(1)

	if not test(problem_folder):
		sys.exit(0)

	print("Attempting to submit")
	solution_files = list(Path(problem_folder).glob("*.cpp"))
	submit_command = [sys.executable, "kattis-cli/submit.py", "-p", problem_id]
	submit_command += [str(f) for f in solution_files]
	submit_result = subprocess.run(
		submit_command,
		text=True
	)

	if submit_result.returncode != 0:
		sys.exit(0)

	if len(sys.argv) == 3:
		sys.exit(0)
	metadata_file = os.path.join(os.curdir, sys.argv[3])

	with open(metadata_file, "r") as f:
		data = yaml.safe_load(f)
	if not data["problems"][problem_id]["solved"]:
		data["solved"] += 1
		data["problems"][problem_id]["solved"] = True
	with open(metadata_file, "w") as f:
		yaml.dump(data, f, sort_keys=False)

	generate_readme(metadata_file)

