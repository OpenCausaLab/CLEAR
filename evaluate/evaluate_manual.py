import sys
import json
import os


input_filename, question_type, output_filename = sys.argv[1], sys.argv[2], sys.argv[3]
obj = json.load(open(input_filename, encoding='utf-8'))


result_dict = dict()
result_dict["total"] = {
    "result_correct": 0,
    "process_correct": 0,
    "total": 0,
}

task_types = [
    "node",
    "edge",
    "2_node_relation",
    "3_node_relation",
    "path",
    "cycle",
    "topological",
    "blocked_path",
    "d-separation",
    "markov_equivalent",
    "markov_blanket",
    "directed_path",
    "backdoor_path",
    "c-component",
    "c-tree",
    "c-forest",
    "maximal_root_set",
    "backdoor_adjustment_set",
    "frontdoor_adjustment_set",
    "identification",
]




for item in obj["judgedList"]:
    assert item["is_result_correct"] in [0, 1]
    
    if item["is_process_correct"] == -1:
        item["is_process_correct"] = item["is_result_correct"]
    assert item["is_process_correct"] in [0, 1]
    if item["task_type"] not in result_dict:
        result_dict[item["task_type"]] = {
            "result_correct": 0,
            "process_correct": 0,
            "total": 0
        }
    if item["is_result_correct"] == 1:
        result_dict[item["task_type"]]["result_correct"] += 1
        result_dict["total"]["result_correct"] += 1
    if item["is_process_correct"] == 1:
        result_dict[item["task_type"]]["process_correct"] += 1
        result_dict["total"]["process_correct"] += 1
    result_dict[item["task_type"]]["total"] += 1
    result_dict["total"]["total"] += 1

f_out = open(output_filename, 'w')
f_out.write('''
|task |  total | result_correct | process_correct | result_accuracy | process_accuracy |
|:------:|:------:|:------:|:------:|:------:|:------:|
''')
for task_type in task_types + ["total"]:
    f_out.write(f"|{task_type}|")
    if task_type not in result_dict:
        f_out.write("- | - | - | - |- |\n")
        continue
    for item in ["total", "result_correct", "process_correct"]:
        f_out.write(f"{result_dict[task_type][item]} |")
    result_accuracy = result_dict[task_type]["result_correct"] / result_dict[task_type]["total"] * 100.0
    process_accuracy = result_dict[task_type]["process_correct"] / result_dict[task_type]["total"] * 100.0
    f_out.write(f" {result_accuracy:.2f} | {process_accuracy:.2f} |\n")