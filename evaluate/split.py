import sys
import json
import os


question_types = ['FA', 'FO', 'HM', 'YN', 'MC', 'EX']
input_filename = sys.argv[1]
output_dirname = sys.argv[2]
os.makedirs(output_dirname, exist_ok=True)

f_out = dict()
for question_type in question_types:
    output_filename = os.path.join(output_dirname, question_type + '.jsonl')
    f_out[question_type] = open(output_filename, 'w', encoding='utf=8')


lines = open(input_filename, encoding='utf-8').readlines()
for line in lines:
    obj = json.loads(line)
    if obj["question_type"] == "MC":
        format_prompt = '''The following is a robot's answer to a multiple-choice question. Please summarize which option it answered and output "A", "B", "C" or "D". If you cannot summarize, please output "unknown" . Do not output other redundant content.'''
        format_prompt += '\n\n'
        format_prompt += "Question: " + obj["question"]
        format_prompt += '\n\n'
        format_prompt += "Answer: " + obj['model_response']
        obj["format_prompt"] = format_prompt
    elif obj["question_type"] == "YN" or obj["question_type"] == "EX":
        format_prompt = '''The following is a robot's answer to a yes-or-no question. Please summarize which option it answered and output "yes" or "no". If you cannot summarize, please output "unknown" . Do not output other redundant content.'''
        format_prompt += '\n\n'
        format_prompt += "Question: " + obj["question"]
        format_prompt += '\n\n'
        format_prompt += "Answer: " + obj['model_response']
        obj["format_prompt"] = format_prompt
    elif obj["question_type"] == "HM":
        format_prompt = '''The following is a robot's answer to a how-many question. Please summarize its answer and output an integer. If you cannot summarize, please output "unknown" . Do not output other redundant content.'''
        format_prompt += '\n\n'
        format_prompt += "Question: " + obj["question"]
        format_prompt += '\n\n'
        format_prompt += "Answer: " + obj['model_response']
        obj["format_prompt"] = format_prompt

    f_out[obj["question_type"]].write(json.dumps(obj, ensure_ascii=False) + '\n')

for key in f_out:
    f_out[key].close()