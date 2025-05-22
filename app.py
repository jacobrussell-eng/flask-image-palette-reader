from flask import Flask, render_template, request
from PIL import Image, ImageOps
from numpy import array, unique, argsort

app = Flask(__name__)

def top_ten_colours(file, code):
    img = Image.open(file).convert('RGB')
    img = ImageOps.posterize(img, 4)
    img_array = array(img)

    # Pure python method (slower):
    # unique_colours = {}
    # for column in img_array:
    #     for colour in column:
    #         tuple_colour = tuple(colour)
    #         if tuple_colour in unique_colours:
    #             unique_colours[tuple_colour] += 1
    #         else:
    #             unique_colours[tuple_colour] = 1
    # unique_colours = sorted(unique_colours, key=lambda x: x[1], reverse=True)

    # Flatten to no. Pixels and RGB only:
    flat_array = img_array.reshape(-1, 3)
    # Find Unique rows and their counts:
    unique_colours, counts = unique(flat_array, axis=0, return_counts=True)

    # Using argsort() returns the indices in order, which can be iterated through the other array:
    if len(counts) <= 10:
        top_ten_id = argsort(counts)[::-1]
    else:
        top_ten_id = (-counts).argsort()[:10]
    top_ten_rgb = unique_colours[top_ten_id]
    top_ten_rgb = [tuple(colour) for colour in top_ten_rgb]
    print(top_ten_rgb)

    # If hex values are requested:
    if code == 'hex':
        top_ten_hex = []
        for key in top_ten_rgb:
            top_ten_hex.append('#%02x%02x%02x' % key)
        return top_ten_hex
    else:
        return top_ten_rgb

# Process form input and Render template:
@app.route('/', methods=['GET','POST'])
def index():
    colours = []
    colour_code = 'rgb'
    if request.method == 'POST':
        f = request.files['file']
        colour_code = request.form['colour_format']
        colours = top_ten_colours(f.stream, colour_code)
    return render_template('index.html', colours=colours, colour_code=colour_code)

# Run locally:
if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=int("8000"))