from flask import Flask, request, render_template
import os
from flask_cors import CORS

app = Flask(__name__, template_folder='templates', static_folder='staticFiles', )
CORS(app)

img = os.path.join('staticFiles', 'Image')

@app.route('/')
def home():
    items = ["LSA","LexRank", "TextRank"]
    summarize_text = "Le résultat va s'afficher ici...!"
    img_bg = os.path.join(img, 'home_bg.png')
    arrowdown = os.path.join(img, 'down.png')
    return render_template('home.html', items=items, summarize_text = summarize_text, img_bg=img_bg, arrowdown=arrowdown)

@app.route('/aboutus')
def aboutus():
    fileandy = os.path.join(img, 'andy.jpg')
    filelorenzo = os.path.join(img, 'lorenzo.jpg')
    return render_template('aboutus.html', imageandy=fileandy, imagelorenzo=filelorenzo)


@app.route('/documentation')

def documentation():
    file = os.path.join(img, 'remeetai_simple_schema2.png')
    return render_template('documentation.html', image=file)


if __name__ == '__main__':
    app.run(debug=False, port=8080)
    
    
