import os
from openai import OpenAI
import sys
import json
import time

# Your own api key
client = OpenAI(
  api_key= "", 
)

def openai_api(input_text, model_name, retries=3):
  retry_cnt = 0
  backoff_time = 30
  while retry_cnt < retries:
    try:
      response = client.chat.completions.create(
          model=model_name, 
          messages=[
              {"role": "system", "content": "You are a helpful assistant."},
              {"role": "user", "content": input_text}
          ]
      )
      return response.choices[0].message.content
    except:
      time.sleep(backoff_time)
      backoff_time *= 1.5
      retry_cnt += 1
  return None

if __name__ == "__main__":
  filename, model_name, outname = sys.argv[1], sys.argv[2], sys.argv[3]
  lines = open(filename, encoding='utf-8').readlines()

  old_lines_len = 0
  old_lines = []
  if os.path.exists(outname):
    old_lines = open(outname, encoding='utf8').readlines()
    old_lines_len = len(old_lines)

  
  f_out = open(outname, 'w', encoding='utf8')
  for line in old_lines:
    f_out.write(line)
    f_out.flush()

  for index in range(old_lines_len, len(lines)):
    line = lines[index]
    data = json.loads(line)
    input_text = data["format_prompt"]
    response = openai_api(input_text, model_name)
    if response is None:
      print('error')
      exit()
    print(f"======={index}=======", flush=True)
    print(f"query: {input_text}\n", flush=True)
    print(f"response: {response}\n", flush=True)

    data["format_response"] = response
    f_out.write(json.dumps(data, ensure_ascii=False) + '\n')
    f_out.flush()
  f_out.close()

