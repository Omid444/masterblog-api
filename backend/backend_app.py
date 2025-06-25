from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import json
import os


app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
# CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
SWAGGER_URL="/api/docs"  # (1) swagger endpoint e.g. HTTP://localhost:5002/api/docs
API_URL="/static/masterblog.json" # (2) ensure you create this dir and file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API' # (3) You can change this if you like
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


def load_post():
    """Upload json file, if no such file exist in path or if it is empty it will return empty list"""
    if os.path.exists('data/blog_posts.json'):
        with open('data/blog_posts.json', 'r') as file:
            content = file.read().strip()
            if content:
                return json.loads(content)
    return []


def save_post(posts):
    """Write changes to jason file"""
    json_post = json.dumps(posts, indent=4)
    with open('data/blog_posts.json', 'w') as file:
        file.write(json_post)

POSTS = load_post()


def validate_post_data(data):
    """Validate if title either content are given as parameter"""
    if ("title" not in data or "content" not in data or "author" not in data or "date" not in data) or (len(data) > 4):
        return False
    return True


def find_post_by_id(post_id):
  """ Find the book with the id `book_id`.
  If there is no book with this id, return None. """
  # TODO: implement this
  for post in POSTS:
      if post['id'] == post_id:
          return post


def find_sort_item(sort_param):
    """Compare sort_param with sortin_item, return appropriate item"""
    sorting_items = {'title', 'content', 'author', 'date'}
    for item in sorting_items:
        if sort_param == item:
            return item
    return False


def find_direction_item(direction_param):
    """Compare direction_param with 'asc','desc', return appropriate item"""
    if direction_param == 'asc':
        return False
    elif direction_param == 'desc':
        return True


def implement_sort(sort_param, direction_param):
    """Sort post based on sort_param, direction_param"""
    sort_item = find_sort_item(sort_param)
    direction_item = find_direction_item(direction_param)
    if sort_item:
        return sorted(POSTS, key=lambda post: post[sort_item], reverse=direction_item)
    return False


@app.route('/api/posts', methods=['GET'])
def handle_get():
    """Make sorted list based on params and return sorted list, if no params return original list"""
    sort = request.args.get("sort")
    direction = request.args.get("direction")

    if sort in {'title', 'content', 'author', 'date'}:
        return implement_sort(sort, direction)

    elif sort is not None or direction is not None:
        return '400 Bad Request please enter valid parameter', 400

    elif sort is None and direction is None:
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

    new_id = max(post['id'] for post in POSTS) + 1
    new_post['id'] = new_id
    # Add the new post to our list
    POSTS.append(new_post)
    # Return the new post data to the client
    return jsonify(new_post),201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def handle_delete(id):
    """Delete post based on id and return success message, if invalid id return 404 error"""
    post = find_post_by_id(id)
    if post is None:
        return 'Not Found', 404

    POSTS.remove(post)
    message = {
    "message": f"Post with id {id} has been deleted successfully."
    }
    # Return the message
    return jsonify(message), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def handle_update(id):
    """Update post data, first find post by id
    if id does not exist return 'not found'"""
    post = find_post_by_id(id)
    if post is None:
        return 'Not Found', 404

    # Update the post with the new data
    new_data = request.get_json()
    post.update(new_data)

    # Return the updated book
    return jsonify(post)


@app.route('/api/posts/search', methods=['GET'])
def handle_search():
    """Find post or posts based on title (or part of it) or content (or part of it) or both,
    make new list including these posts, return list """
    searched_list = []
    title = request.args.get("title")
    content = request.args.get("content")
    for post in POSTS:
        is_title = title in post['title'].lower() if title else False
        is_content = content in post['content'].lower() if content else False
        if is_title or is_content:
            searched_list.append(post)

    return searched_list


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5002, debug=True)
