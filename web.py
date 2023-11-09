import io
import contextlib
from flask import Flask, render_template, request, make_response
import chat_downloader.cli
from chat_downloader.sites.twitch import TwitchChatDownloader

app = Flask(__name__)

def die():
    raise RuntimeError("Program reached and unexpected state.")

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        url = request.form['url']
        message = request.form['message']
        author_name = request.form['author_name']

        cli_args = []
        filters = []

        if not url:
            return "URL is required!"
        if message:
            filters.append(f"message={message}")
        if author_name:
            if TwitchChatDownloader.matches(url):
                filters.append(f"author.display_name={author_name}")
            else:
                filters.append(f"author.name={author_name}")
        
        if filters:
            cli_args.append("--filter")
            cli_args.append(",".join(filters))
        cli_args.append(url)

        with contextlib.redirect_stdout(io.StringIO()) as res:
            chat_downloader.cli.main(cli_args)
        response = make_response(res.getvalue(), 200)
        response.mimetype = "text/plain"
        return response
    else:
        die()
