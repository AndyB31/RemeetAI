from flask import Flask, request, render_template

app = Flask(__name__, template_folder='templates', static_folder='staticFiles', )

@app.route('/')
def home():
    
    items = ["LSA","LexRank", "TextRank"]
    summarize_text = "Le résultat va s'afficher ici...!"
    return render_template('home.html', items=items, summarize_text = summarize_text)

def aboutus():
    
    return render_template('aboutus.html')

def documentation():

    return render_template('documentation.html')


if __name__ == '__main__':
    app.run(debug=True)
    
    