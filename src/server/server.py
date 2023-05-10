from flask import Flask, request, abort
from media_transcript_remeetai import process_media, text_summarization

app = Flask(__name__)

@app.route("/")
def hello_world():
  return "<p>Hello, World!</p>"

@app.post("/summarize/")
@app.post("/summarize/<tool>")
def summarize(tool = "bart"):
  if not request.files['file']:
    return {"message": "Need to upload a file"}, 400
  f = request.files['file']
  f.save(f'../../res/data/{f.filename}')
  transcript, _, _, _ = process_media.trancript(f.filename)
  if tool == "bart":
    report = text_summarization.bart_sum(text_base = transcript)
  elif tool == "lexrank":
    report = text_summarization.lexrank_sum(text_base = transcript)
  elif tool == "textrank_lsa":
    report = text_summarization.textrank_lsa_sum(text_base = transcript)

  return {"report": f"{report}"}