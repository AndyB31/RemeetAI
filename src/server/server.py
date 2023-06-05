import uuid
from multiprocessing import Process, Manager, Queue
from flask import Flask, request, abort
from media_transcript_remeetai import process_media, text_summarization

from media_transcript_remeetai.text_summarization import bart_summarization, lexrank_summarization, textrank_lsa
from flask_cors import CORS

# threaded.ThreadPooled.configure(max_workers=3)

process_registry = {}

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
  return "<p>Hello, World!</p>"

def run_subprocess(tool, filename, uid, data):
  # data = {}
  try:
    transcript, _, _, _ = process_media.trancript(filename)
    if tool == "bart":
      report = bart_summarization.bart_sum(text_base = transcript)
    elif tool == "LexRank":
      report = lexrank_summarization.lexrank_sum(text_base = transcript)
    elif tool == "LSA":
      report = textrank_lsa.lsa_sum(text_base = transcript)
    elif tool == "TextRank":
      report = textrank_lsa.textrank_sum(text_base = transcript)

    # thread[uid]["report"] = report
    # thread[uid]["is_done"] = True
    # thread[uid]["error"] = False
    data["report"] = report
    data["is_done"] = True
    data["error"] = False
    print(f"{uid} => done")
  except Exception as e:
    data["is_done"] = True
    data["error"] = True
    data["msg"] = str(e.args[0])
    print(f"{uid} => error")


@app.post("/summarize/")
@app.post("/summarize/<tool>")
def summarize(tool = "bart"):
  if not request.files['file']:
    return {"message": "Need to upload a file"}, 400
  f = request.files['file']
  f.save(f'../../res/data/{f.filename}')
  uid = uuid.uuid1()
  manager = Manager()
  thread = manager.dict()
  thread["is_done"] = False
  process = Process(target=run_subprocess, args=(tool, f'../../res/data/{f.filename}', str(uid), thread))
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
    return {"done": True, "report": th["report"]}
  elif th["is_done"]:
    return {"error": f"internal error: {th['msg']}"}
  return {"done": False, "message": "still processing..."}

app.run(port=8000)