from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_post_data(data):
    if "title" not in data or "content" not in data:
        return False
    return True


@app.route('/api/posts', methods=['GET'])
def handle_get():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def handle_posts():
    """
    Get POST requests and validate it,
    if it is ok generate id and return json file,
    otherwise return error.
    log is created as well.
    """
    app.logger.info('GET request received for /api/books  POST log')  # Log a message
    new_post = request.get_json()
    if not validate_post_data(new_post):
        return jsonify({"error": "Invalid post data"}), 400

    new_id = max(book['id'] for book in POSTS) + 1
    new_post['id'] = new_id
    # Add the new post to our list
    POSTS.append(new_post)
    # Return the new post data to the client
    return jsonify(new_post),201


#@app.route('/api/posts/<id>', methods=['DELETE'])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
