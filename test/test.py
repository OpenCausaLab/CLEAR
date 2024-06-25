import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import argparse
import json
import fix_prompt


parser = argparse.ArgumentParser()
parser.add_argument('--model_path', default=None, type=str, required=True)
parser.add_argument('--data_file', default=None, type=str, help="A file that contains instructions (one instruction per line)")
parser.add_argument('--output_file', default="./output.jsonl", type=str, help="Output file.")
# Four prompts: basic, one-shot-IcL, three-shot-IcL and definition-guided
parser.add_argument('--prompt', default="basic", type=str, help='Choose prompt style.')
# Two criteria: normal and definition-proficiency
parser.add_argument('--criterion', default="normal", type=str,  help='Choose evaluation criterion.')
args = parser.parse_args()


# Initialize Model
print("Initializing model...", flush=True)
tokenizer = AutoTokenizer.from_pretrained(args.model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    args.model_path,
    device_map="auto",
    trust_remote_code=True,
    torch_dtype=torch.float16
)
model = model.eval()
print("Finish initialization model.", flush=True)

# Read data
data_list = []
with open(args.data_file, "r") as f:
    for line in f:
        item = json.loads(line)
        # B3: Correct utilization of causal definitions.
        if args.criterion == 'definition-proficiency' and any(question_type in item["question_type"] for question_type in ["HM", "YN", "MC", "EX"]):
            data_list.append(item)
        # B1, B2 and B4
        elif args.criterion == 'normal':
            data_list.append(item)

# Inference
print("Start Inference...", flush=True)
f_out = open(args.output_file, 'w')
for index, data in enumerate(data_list):
    if args.prompt == 'basic':
        example = data["description"] + '\n' + data["question"]
    # 1/3-shot IcL and definition-guided prompt are only used in B3
    else:
        prompt_functions = {
        'one-shot-IcL': fix_prompt.add_1example,
        'three-shot-IcL': fix_prompt.add_3example,
        'definition-guided': fix_prompt.add_def,
        }
        prompt_function = prompt_functions.get(args.prompt)
        example = prompt_function(data) + '\n' + data["description"] + '\n' + data["question"]

    chat = [ {"role": "user", "content": example} ]
    input_text = tokenizer.apply_chat_template(chat, tokenize=False)
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to(model.device)
    generation_output = model.generate(
        input_ids,
        max_new_tokens=300,
    )
    response = tokenizer.decode(generation_output[0], skip_special_tokens=True)
    prompt_length = len(
        tokenizer.decode(
        input_ids[0],
        skip_special_tokens=True,
        )
    )
    response = response[prompt_length:]

    print(f"======={index}=======", flush=True)
    print(f"query: {input_text}\n", flush=True)
    print(f"response: {response}\n", flush=True)

    data["model_response"] = response
    f_out.write(json.dumps(data, ensure_ascii=False) + '\n')
    f_out.flush()
f_out.close()
