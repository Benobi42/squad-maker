"""Flask Application for Hockey Squad Builder."""

from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def main():
    """Render the default page for application."""
    return render_template('index.html')


if __name__ == "__main__":
    """When calling this file in the command line, run the application"""
    app.run(host="0.0.0.0")
