from flask import (
    Blueprint,
    render_template,
)


main = Blueprint(
    "main",
    __name__,
    template_folder="templates",
    static_url_path="",
    static_folder="static",
)


@main.route("/", methods=["GET"])
def index():
    return render_template("index.html")
