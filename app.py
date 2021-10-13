from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, Response
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
from s3details import get_bucket, get_buckets_list


import os, signal

app = Flask(__name__)
Bootstrap(app)
app.secret_key ='secret'


@app.route('/')
def index():
    buckets = get_buckets_list()
    return render_template("index.html", buckets=buckets)


@app.route('/files')
def files():
    my_bucket = get_bucket()
    summaries = my_bucket.objects.all()

    return render_template('files.html', my_bucket=my_bucket, files=summaries)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    my_bucket = get_bucket()
    my_bucket.Object(file.filename).put(Body=file)
    flash('File uploaded successfully')
    return redirect(url_for('files'))


@app.route('/delete', methods=['POST'])
def delete():
        key = request.form['key']
        my_bucket = get_bucket()
        my_bucket.Object(key).delete()

        flash('File deleted successfully')
        return redirect(url_for('files'))


@app.route('/download', methods=['POST'])
def download():
    key = request.form['key']

    my_bucket = get_bucket()
    file_obj = my_bucket.Object(key).get()

    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )


if __name__ == "__main__":

    app.run()


@app.route('/stop', methods=['GET'])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({ "success": True, "message": "Server is shutting down..." })
