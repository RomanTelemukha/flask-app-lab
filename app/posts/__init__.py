from flask import Blueprint

post_bp = Blueprint(
    "post", 
    __name__, 
    template_folder="templates/posts",
    static_folder="static",
    static_url_path="/posts/static"
)