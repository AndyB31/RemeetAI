from flask import Flask, request, abort, render_template
from media_transcript_remeetai import process_media
from media_transcript_remeetai.text_summarization import lexrank_summarization, textrank_lsa
import os

app = Flask(__name__, template_folder='templates', static_folder='staticFiles')

@app.route("/")
def home():
    items = ["LexRank", "TextRank", "LSA", "Bart"]
    return render_template('home.html', items=items)

@app.post("/summarize")
@app.post("/summarize/")
@app.post("/summarize/<tool>")
def summarize(tool = "textrank_lsa"):
  print(request.files)
  print(request.form)
  if not request.files['file']:
    return {"message": "Need to upload a file"}, 400
  f = request.files['file']
  print (f)
  f.save(f'./res/data/{f.filename}')
  abs_path = os.path.abspath(f'./res/data/{f.filename}')
  transcript, _, _, _ = process_media.trancript(abs_path)
  if request.form['tool']:
    tool = request.form['tool']
  # if tool == "bart":
  #   report = bart_summarization.bart_sum(text_base = transcript)
  if tool == "LexRank":
    report = lexrank_summarization.lexrank_sum(text_base = transcript)
  elif tool == "textrank_lsa" or tool=="TextRank" or tool=="LSA":
    report = textrank_lsa.textrank_lsa_sum(text_base = transcript)
  else:
    report = textrank_lsa.textrank_lsa_sum(text_base = transcript)

  return {"report": f"{report}"}