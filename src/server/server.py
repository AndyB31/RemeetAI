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
  L: {"e": 12, "g": 3},
  M: {"e": 8, "g": 2},
  S: {"e": 5, "g": 1},
  X: {"e": 2, "g": 0},
}

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
  return "<p>Hello, World!</p>"

def run_subprocess_chunk(tool, filename, uid, data, size, text):
  # data = {}
  try:
    if len(text) > 0:
      transcript = text
    else:
      audio = filename.split('.')[-1] in ['mp3', 'wav']
      if audio:
        transcript, _, _, _ = process_media.trancript(filename, audio=audio)
      else:
        it = process_media.iter_transcript_chunk(filename)
        i = 0
        for trscpt in it:
          print(f"chunk_{i}")
          i += 1
    data["report"] = "test"
    data["transcript"] = "transcript"
    data["is_done"] = True
    data["error"] = False
    print(f"{uid} => done")
    return
    
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


def run_subprocess(tool, filename, uid, data, size, text):
  # data = {}
  try:
    if filename:
      audio = filename.split('.')[-1] in ['mp3', 'wav']
      transcript, _, _, _ = process_media.trancript(filename, audio=audio)
    else:
      transcript = text
    # data["report"] = "test"
    # data["transcript"] = "transcript"
    # data["is_done"] = True
    # data["error"] = False
    # print(f"{uid} => done")
    # return
    
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
    data["msg"] = str("Une erreur est survenue. Rafraichissez la page.")
    print(f"{uid} => error")
    print(f"{e}")


@app.post("/summarize/")
@app.post("/summarize/<tool>")
def summarize(tool = "bart"):
  if not request.files['file'] and not request.form['text']:
    return {"message": "Need to upload a file of a text"}, 400
  
  print("file or text")
  try:
    size = int(request.form["size"])
  except:
    size = 2
  try:
    f = request.files['file']
    f.save(f'../../res/data/{f.filename}')
    filename = f.filename
    print(filename)
  except:
    filename = None
  try:
    text = request.form['text']
  except:
    text = None
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