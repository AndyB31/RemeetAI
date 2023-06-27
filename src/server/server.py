import uuid
from multiprocessing import Process, Manager, Queue
from flask import Flask, request, abort
from media_transcript_remeetai import process_media, text_summarization

from media_transcript_remeetai.text_summarization import bart_summarization, lexrank_summarization, textrank_lsa
from flask_cors import CORS
import json

# threaded.ThreadPooled.configure(max_workers=3)

process_registry = {}

L = 3
M = 2
S = 1
X = 0

sizes_chart = {
  L: {"e": 20, "g": 3},
  M: {"e": 15, "g": 2},
  S: {"e": 10, "g": 1},
  X: {"e": 5, "g": 0},
}



app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
  return "<p>Hello, World!</p>"

def run_subprocess(tool, filename, uid, data, size, text):
  # data = {}
  try:
    if len(text) > 0:
      transcript = text
    else:
      transcript, _, _, _ = process_media.trancript(filename)
    print()
    if tool == "bart":
      report = bart_summarization.bart_sum(text_base = transcript, text_length=size["g"])
    elif tool == "LexRank":
      report = lexrank_summarization.lexrank_sum(text_base = transcript, sentences_number=size["e"])
    elif tool == "LSA":
      report = textrank_lsa.lsa_sum(text_base = transcript, sentences_number=size["e"])
    elif tool == "TextRank":
      report = textrank_lsa.textrank_sum(text_base = transcript, sentences_number=size["e"])

    # thread[uid]["report"] = report
    # thread[uid]["is_done"] = True
    # thread[uid]["error"] = False
    # try:
    #   report = json.dumps(report)
    # except:
      
    data["report"] = report
    data["transcript"] = transcript
    data["is_done"] = True
    data["error"] = False
    print(f"{uid} => done")
  except Exception as e:
    data["is_done"] = True
    data["error"] = True
    data["msg"] = str(e)
    print(f"{uid} => error")


@app.post("/summarize/")
@app.post("/summarize/<tool>")
def summarize(tool = "bart"):
  if not request.files['file'] and not request.form['text']:
    return {"message": "Need to upload a file of a text"}, 400
  
  print("filw or text")
  if request.form["size"]:
    size = int(request.form["size"])
  else:
    size = 2
  try:
    text = request.form['text']
  except:
    text = ""
  if request.files['file']:
    f = request.files['file']
    f.save(f'../../res/data/{f.filename}')
    filename = f.filename
  else:
    filename = ""
  print("if if if")
  uid = uuid.uuid1()
  manager = Manager()
  thread = manager.dict()
  thread["is_done"] = False
  print("process")
  process = Process(target=run_subprocess, args=(tool, f'../../res/data/{filename}', str(uid), thread, sizes_chart[size], text))
  process.start()
  process_registry[str(uid)] = {"p": process, "data": thread} 
  return {"id": f"{uid}"}
  

@app.get("/summary/<uid>")
def get_summary(uid):
  print(uid)
  try:
    print(process_registry[uid]["p"].exitcode)
    if process_registry[uid]["p"].exitcode != None:
      process_registry[uid]["p"].join()
    print(process_registry[uid]["data"])
    print(process_registry[uid]["p"])
    th = process_registry[uid]["data"]
  except Exception as e:
    return {"error": str(e)}, 404
  if th["is_done"] and not th["error"]:
    return {"done": True, "report": th["report"], "transcript": th["transcript"]}
  elif th["is_done"]:
    return {"error": f"internal error: {th['msg']}"}
  return {"done": False, "message": "still processing..."}

app.run(port=8000)