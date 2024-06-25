import google.generativeai as genai
import os
import sys
import json
import time
import fix_prompt

safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

# Your own api key
genai.configure(api_key='')

for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)

def gemini_api(input_text, model_name, retries=3):
  retry_cnt = 0
  backoff_time = 30
  model = genai.GenerativeModel(model_name)
  while retry_cnt < retries:
    try:
      response = model.generate_content(input_text, safety_settings=safety_settings)
      return response.text
    except Exception as e:
      print(input_text)
      print(e)
      time.sleep(backoff_time)
      backoff_time *= 1.5
      retry_cnt += 1
  return None


if __name__ == "__main__":
  # Four prompts: basic, one-shot-IcL, three-shot-IcL and definition-guided
  # Two criteria: normal and definition-proficiency
  
  filename, model_name, outname, prompt, criterion = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
  lines = open(filename).readlines()

  old_lines_len = 0
  old_lines = []
  if os.path.exists(outname):
    old_lines = open(outname, encoding='utf8').readlines()
    old_lines_len = len(old_lines)

  f_out = open(outname, 'w', encoding='utf8')
  for line in old_lines:
    f_out.write(line)
    f_out.flush()

  data_list = []
  for index in range(old_lines_len, len(lines)):
    line = lines[index]
    item = json.loads(line)
    if criterion == 'definition-proficiency' and any(question_type in item["question_type"] for question_type in ["HM", "YN", "MC", "EX"]):
            data_list.append(item)
        # B1, B2 and B4
    elif criterion == 'normal':
            data_list.append(item)

  for index, data in enumerate(data_list):
    if prompt == 'basic':
        input_text = data["description"] + '\n' + data["question"]
    # 1/3-shot IcL and definition-guided prompt are only used in B3
    else:
        prompt_functions = {
        'one-shot-IcL': fix_prompt.add_1example,
        'three-shot-IcL': fix_prompt.add_3example,
        'definition-guided': fix_prompt.add_def,
        }
        prompt_function = prompt_functions.get(prompt)
        input_text = prompt_function(data) + '\n' + data["description"] + '\n' + data["question"]

    response = gemini_api(input_text, model_name)
    if response is None:
      print('error')
      exit()
    print(f"======={index}=======", flush=True)
    print(f"query: {input_text}\n", flush=True)
    print(f"response: {response}\n", flush=True)

    data["model_response"] = response
    f_out.write(json.dumps(data, ensure_ascii=False) + '\n')
    f_out.flush()
  f_out.close()