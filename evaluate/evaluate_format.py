import sys
import json
import re


input_filename, question_type, output_filename = sys.argv[1], sys.argv[2], sys.argv[3]
lines = open(input_filename, encoding='utf-8').readlines()

is_yn = (question_type == "YN" or question_type == "EX")
is_mc = (question_type == "MC")
is_hm = (question_type == "HM")
assert is_yn or is_mc or is_hm


result_dict = dict()
result_dict["total"] = {
    "tp": 0,
    "fn": 0,
    "fp": 0,
    "tn": 0,
    "correct": 0,
    "wrong": 0
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

for line in lines:
    obj = json.loads(line)
    if question_type != obj["question_type"]: continue
    task_type = obj["task_type"]
    if is_yn:
        pattern_0 = r'([\s\W]+no)|(^no)'
        pattern_1 = r'([\s\W]+yes)|(^yes)'
        pattern_2 = r'([\s\W]+unknown)|(^unknown)'
        assert obj["answer"] in ["Yes.", "No."], obj["answer"]
        obj_0 = re.search(pattern_0, obj["format_response"], re.I)
        obj_1 = re.search(pattern_1, obj["format_response"], re.I)
        obj_2 = re.search(pattern_2, obj["format_response"], re.I)
        if obj_0 is not None and obj_1 is None and obj_2 is None:
            pred = "No."
        elif obj_0 is None and obj_1 is not None and obj_2 is None:
            pred = "Yes."
        elif obj_0 is None and obj_1 is None and obj_2 is not None:
            pred = "Unknown."
        else:
            print(obj_0, obj_1, obj_2, obj["format_response"])
            pred = "Unknown"
            # assert False
        # print(obj["format_response"], pred)
        if task_type not in result_dict:
            result_dict[task_type] = {
                "tp": 0,
                "fn": 0,
                "fp": 0,
                "tn": 0,
                "correct": 0,
                "wrong": 0
            }
        for key in ["total", task_type]:
            if obj["answer"] == "Yes.":
                if pred == "Yes.":
                    result_dict[key]["tp"] += 1
                    result_dict[key]["correct"] += 1
                else:
                    result_dict[key]["fn"] += 1
                    result_dict[key]["wrong"] += 1
            else:
                if pred == "No.":
                    result_dict[key]["tn"] += 1
                    result_dict[key]["correct"] += 1
                else:
                    result_dict[key]["fp"] += 1
                    result_dict[key]["wrong"] += 1
    elif is_mc:
        assert obj["answer"] in ["A", "B", "C", "D"]
        pattern_0 = r'([\s\W]+A)|(^A)'
        pattern_1 = r'([\s\W]+B)|(^B)'
        pattern_2 = r'([\s\W]+C)|(^C)'
        pattern_3 = r'([\s\W]+D)|(^D)'
        obj_0 = re.search(pattern_0, obj["format_response"])
        obj_1 = re.search(pattern_1, obj["format_response"])
        obj_2 = re.search(pattern_2, obj["format_response"])
        obj_3 = re.search(pattern_3, obj["format_response"])
        # if obj["format_response"] not in ["A", "B", "C", "D", "unknown"]:
        #     print(obj["format_response"])
        if obj_0 is not None and obj_1 is None and obj_2 is None and obj_3 is None:
            pred = "A"
        elif obj_1 is not None and obj_0 is None and obj_2 is None and obj_3 is None:
            pred = "B"
        elif obj_2 is not None and obj_0 is None and obj_1 is None and obj_3 is None:
            pred = "C"
        elif obj_3 is not None and obj_0 is None and obj_1 is None and obj_2 is None:
            pred = "D"
        else:
            # print(obj["format_response"])
            pred = "unknown"
        if task_type not in result_dict:
            result_dict[task_type] = {
                "correct": 0,
                "wrong": 0
            }
        for key in ["total", task_type]:
            if obj["answer"] == pred:
                result_dict[key]["correct"] += 1
            else:
                result_dict[key]["wrong"] += 1
    elif is_hm:
        gt = int(obj["answer"])
        try:
            dt = int(obj["format_response"])
        except Exception as e:
            dt = -1
        if task_type not in result_dict:
            result_dict[task_type] = {
                "correct": 0,
                "wrong": 0
            }
        for key in ["total", task_type]:
            if gt == dt:
                result_dict[key]["correct"] += 1
            else:
                result_dict[key]["wrong"] += 1        

f_out = open(output_filename, 'w')
for key in task_types + ['total']:
    if key not in result_dict:
        continue
    result_dict[key]["accuracy"] = result_dict[key]["correct"] / (result_dict[key]["correct"] + result_dict[key]["wrong"]) * 100


if is_yn:
    f_out.write('''
|task | TP | FN | FP | TN | Correct | Wrong | accuracy |
|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|
''')
    for task_type in task_types + ["total"]:
        f_out.write(f"|{task_type}|")
        if task_type not in result_dict:
            f_out.write("- | - | - | - | - | - | - |\n")
            continue
        for item in ["tp", "fn", "fp", "tn", "correct", "wrong"]:
            f_out.write(f"{result_dict[task_type][item]} |")
        f_out.write(f"{result_dict[task_type]['accuracy']:.2f} |")
        f_out.write(f"\n")
elif is_mc or is_hm:
    f_out.write('''
|task |  Correct | Wrong | accuracy |
|:------:|:------:|:------:|:------:|
''')
    for task_type in task_types + ["total"]:
        f_out.write(f"|{task_type}|")
        if task_type not in result_dict:
            f_out.write("- | - | - |\n")
            continue
        for item in [ "correct", "wrong"]:
            f_out.write(f"{result_dict[task_type][item]} |")
        f_out.write(f"{result_dict[task_type]['accuracy']:.2f} |")
        f_out.write(f"\n")    