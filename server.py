from flask import Flask, render_template, request, redirect, \
    url_for, make_response
from articles import save_article, get_filename, load_article
import random
import string


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


@app.route('/', methods=['POST', 'GET'])
def form():
    if request.method == 'POST':
        header = request.form.get('header')
        signature = request.form.get('signature')
        body = request.form.get('body')
        url = get_filename(header)
        token = ''.join(random.choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits
        ) for x in range(16))
        save_article(header, signature, body, url, token)
        response = make_response(redirect(
            url_for('show_article', article=url)))
        response.set_cookie(token, value='author')
        return response
    else:
        return render_template('form.html')


@app.route('/<article>/', methods=['POST', 'GET'])
def show_article(article):
    article_data = load_article(article)
    if article_data is None:
        return render_template('404.html')
    if article_data['token'] in request.cookies:
        attribute = ""
        if request.method == 'POST':
            header = request.form.get('header')
            signature = request.form.get('signature')
            body = request.form.get('body')
            save_article(header, signature, body, article, article_data['token'])
            return redirect(url_for('show_article', article=article))
    else:
        attribute = "disabled"
    header = article_data['header']
    signature = article_data['signature']
    body = article_data['body']
    return render_template(
        'article.html', attribute=attribute, header=header,
        signature=signature, body=body)


if __name__ == "__main__":
    app.run()
