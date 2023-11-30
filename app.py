from bson import ObjectId
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, request, flash

import utils

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)


@app.route('/')
def main():
    return render_template('home.html', session=session.get('user'))


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(redirect_uri=url_for("callback", _external=True))


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("main", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


@app.route('/editor', methods=('GET', 'POST'))
def editor():
    if session.get('user'):
        username = session.get('user').get('userinfo').get('email')
        titles = utils.get_titles(username)
        if request.method == 'POST':
            if 'save' in request.form:
                title = request.form.get('curr_title')
                content = request.form.get('body')
                utils.save_content(username, title, content)
                return render_template('index.html', session=session.get('user'), content=content, titles=titles, title=title)
            elif 'load' in request.form:
                title = request.form.get('title_select')
                content = utils.get_content(username, title)
                return render_template('index.html', session=session.get('user'), content=content, titles=titles, title=title)
            elif 'gen_bib' in request.form:
                title = request.form.get('curr_title')
                content = request.form.get('body')
                updated_content = utils.generate_bibliography(username, title, content)
                return render_template('index.html', session=session.get('user'), content=updated_content, titles=titles, title=title)

        return render_template('index.html', session=session.get('user'), titles=titles)
    return redirect("/login")


@app.route('/creator', methods=('GET', 'POST'))
def creator():
    if session.get('user'):
        username = session.get('user').get('userinfo').get('email')
        titles = utils.get_titles(username)
        if request.method == 'POST':
            if 'doc_submit' in request.form:
                title = request.form['title']
                template = request.form.get('template_select')
                citation = request.form.get('citation_select')
                if not title:
                    flash('Title is required!')
                elif not template:
                    flash('Content is required!')
                elif not citation:
                    flash("Citation style is required!")
                else:
                    info = [title, template, citation]
                    utils.create_doc(username, info)
                    return redirect("/editor")
            elif 'cite_submit' in request.form:
                cite_doc = request.form.get('title_select')
                doi = request.form['doi']
                pdf_link = request.form['pdf_link']

                if not pdf_link:
                    pdf_link = ''

                if not cite_doc:
                    flash('Document title is required!')
                elif not doi:
                    flash("doi is required!")
                elif not utils.is_valid_doi(doi):
                    flash("Invalid doi entered")
                else:
                    utils.add_citation(cite_doc, doi, pdf_link, username)
                    return redirect("/creator")
        return render_template('create.html', session=session.get('user'), titles=titles)
    return redirect("/login")


@app.route('/manage', methods=('GET', 'POST'))
def manage():
    if session.get('user'):
        username = session.get('user').get('userinfo').get('email')
        if request.method == 'POST':
            object_id = list(request.form.to_dict().keys())[0]
            utils.delete_doc(ObjectId(object_id))
        items = utils.get_titles(username)
        return render_template('manage.html', items=items, session=session.get('user'))
    return redirect("/login")


if __name__ == ' __main__':
    app.debug = True
    app.run()
