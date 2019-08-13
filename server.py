from flask import Flask, render_template, request, redirect, url_for
import data_handler
import connection

app = Flask(__name__)

@app.route('/list', methods=["GET","POST"])
def route_list():
    return render_template("list.html")

    
if __name__ == '__main__':
    app.run(
        port=5000,
        debug=True,
    )
