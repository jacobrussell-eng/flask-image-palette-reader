from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        f = request.files['file']
    return render_template('index.html')

# Run locally:
if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=int("8000"))