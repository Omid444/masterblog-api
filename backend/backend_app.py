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


def find_post_by_id(post_id):
  """ Find the book with the id `book_id`.
  If there is no book with this id, return None. """
  # TODO: implement this
  for post in POSTS:
      if post['id'] == post_id:
          return post


@app.route('/api/posts', methods=['GET'])
def handle_get():
    """Make sorted list based on params and return sorted list, if no params return original list"""
    sort = request.args.get("sort")
    direction = request.args.get("direction")
    is_sort_title = True if sort == 'title'  else False
    is_direction_asc = True if direction == 'asc' else False
    is_sort_content = True if sort == 'content' else False
    is_direction_desc = True if direction == 'desc' else False
    if is_sort_title and is_direction_asc:
        sorted_list =sorted(POSTS, key=lambda post:post['title'])
        return sorted_list

    elif is_sort_title and is_direction_desc:
        sorted_list = sorted(POSTS, key=lambda post: post['title'], reverse=True)
        return sorted_list

    elif is_sort_content and is_direction_asc:
        sorted_list = sorted(POSTS, key=lambda post: post['content'])
        return sorted_list

    elif is_sort_content and is_direction_desc:
        sorted_list = sorted(POSTS, key=lambda post: post['content'], reverse=True)
        return sorted_list

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
    app.run(host="0.0.0.0", port=5002, debug=True)
