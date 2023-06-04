import uuid
from multiprocessing import Process
from flask import Flask, request, abort
from media_transcript_remeetai import process_media, text_summarization

# threaded.ThreadPooled.configure(max_workers=3)

thread = {}

app = Flask(__name__)

@app.route("/")
def hello_world():
  return "<p>Hello, World!</p>"

def run_subprocess(tool, filename, uid):
  transcript, _, _, _ = process_media.trancript(filename)
  if tool == "bart":
    report = text_summarization.bart_sum(text_base = transcript)
  elif tool == "lexrank":
    report = text_summarization.lexrank_sum(text_base = transcript)
  elif tool == "textrank_lsa":
    report = text_summarization.textrank_lsa_sum(text_base = transcript)

  thread[uid]["report"] = report
  thread[uid]["is_done"] = True


@app.post("/summarize/")
@app.post("/summarize/<tool>")
def summarize(tool = "bart"):
  if not request.files['file']:
    return {"message": "Need to upload a file"}, 400
  f = request.files['file']
  f.save(f'../../res/data/{f.filename}')
  uid = uuid.uuid1()
  process = Process(target=run_subprocess, args=(tool, f'../../res/data/{f.filename}', uid))
  process.start()
  thread[str(uid)] = {
    "process": process,
    "is_done": False
  }  
  return {"id": f"{uid}"}
  

@app.get("/summary/<uid>")
def get_summary(uid):
  print(uid)
  print(thread)
  try:
    th = thread[uid]
  except:
    return {"error": "uid not exist."}, 404
  if th["is_done"]:
    return {"done": True, "report": th["report"]}
  return {"done": False, "message": "still processing..."}

app.run(port=8000)