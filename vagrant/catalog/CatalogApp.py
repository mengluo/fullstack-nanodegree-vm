from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, GameGenre, Game, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"

engine = create_engine('sqlite:///categories.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code, now compatible with Python3
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output

# User Helper Functions

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

def userLoggedIn():
    loggedIn = False
    if 'username' in login_session:
        loggedIn = True;
    return loggedIn

def popUpInfo(game, operation_name, game_genre_id, game_id):
    if login_session['user_id'] != game.user_id:
        return """<script>function myFunction() {{
                                    var ok = confirm('You are not authorized to {0} this game. Please create your own game in order to {0} them.');
                                    if(ok == true){{ window.location.href = '/';}}
                                    else{{ window.location.href = '/{1}/{2}';}}
                                }}
                    </script><body onload='myFunction()''>""".format(operation_name, game_genre_id, game_id)
    else: return "";

# revoke the token for the session

@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view game Information

@app.route('/gamegenres/<int:game_genre_id>/JSON')
def gamesJSON(game_genre_id):
    games = session.query(Game).filter_by(game_genre_id=game_genre_id).all()
    return jsonify(games=[g.serialize for g in games])

@app.route('/gamegenres/<int:game_genre_id>/games/<int:game_id>/JSON')
def menuItemJSON(game_genre_id, game_id):
    game = session.query(Game).filter(Game.id==game_id, Game.game_genre_id==game_genre_id).one()
    return jsonify(game=game.serialize)

@app.route('/gamegenres/JSON')
def gameGenresJSON():
    game_genres = session.query(GameGenre).all()
    return jsonify(game_genres=[gg.serialize for gg in game_genres])


# Show home page

@app.route('/')
@app.route('/gamegenres/')
def showHomePage():
    games = session.query(Game).order_by(Game.id.desc()).limit(8).all()
    game_genres = session.query(GameGenre).all()
    # return "This page will show both game genres and recently added games"
    return render_template('HomePage.html', games=games, game_genres=game_genres, loggedIn=userLoggedIn())

# Show games for a game genre

@app.route('/<int:game_genre_id>/')
@app.route('/<int:game_genre_id>/games/')
@app.route('/gamegenres/<int:game_genre_id>/')
@app.route('/gamegenres/<int:game_genre_id>/games/')
def showGames(game_genre_id):
    game_genres = session.query(GameGenre).all()

    for game_genre in game_genres:
        if game_genre.id == game_genre_id:
            selected_game_genre_name = game_genre.name

    games = session.query(Game).filter_by(game_genre_id=game_genre_id).all()

    return render_template('games.html', game_genres=game_genres, selected_game_genre_name=selected_game_genre_name, games=games, loggedIn=userLoggedIn())
    # return 'This page is the list of games for game genre %s' % game_genre_id


# Show a game

@app.route('/<int:game_genre_id>/<int:game_id>/')
@app.route('/<int:game_genre_id>/games/<int:game_id>/')
@app.route('/gamegenres/<int:game_genre_id>/<int:game_id>/')
@app.route('/gamegenres/<int:game_genre_id>/games/<int:game_id>/')
def showGame(game_genre_id, game_id):
    game_genres = session.query(GameGenre).all()
    game = session.query(Game).filter_by(id=game_id).one()

    return render_template('gamePage.html', game_genres=game_genres, game=game, game_genre=game.game_genre, loggedIn=userLoggedIn())
    # return 'This page is displaying details for a game %s' % game_id


# add a new game

@app.route('/new/', methods=['GET', 'POST'])
def newGame():
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        game_genre = session.query(GameGenre).filter_by(id=request.form['game_genre']).one()
        newGame = Game(user_id=login_session['user_id'], name=request.form['name'], description=request.form[
                           'description'], game_genre=game_genre)
        session.add(newGame)
        session.commit()
        flash('New Game %s Successfully Added' % (newGame.name))
        return redirect(url_for('showHomePage'))
    else:
        game_genres = session.query(GameGenre).all()
        return render_template('newGame.html', game_genres=game_genres, loggedIn=userLoggedIn())
    # return 'This page is for adding a new game for game genre %s'
    # %game_genre_id

# Edit a game

@app.route('/gamegenres/<int:game_genre_id>/<int:game_id>/edit')
@app.route('/gamegenres/<int:game_genre_id>/games/<int:game_id>/edit', methods=['GET', 'POST'])
@app.route('/<int:game_genre_id>/<int:game_id>/edit')
@app.route('/<int:game_genre_id>/games/<int:game_id>/edit', methods=['GET', 'POST'])
def editGame(game_genre_id, game_id):
    if 'username' not in login_session:
        return redirect('/login')

    game_to_edit = session.query(Game).filter_by(id=game_id).one()
    auth_messsage = popUpInfo(game_to_edit, "edit", game_genre_id, game_id)
    if len(auth_messsage) != 0:
        return auth_messsage

    if request.method == 'POST':
        if request.form['name']:
            game_to_edit.name = request.form['name']
        if request.form['game_genre']:
            game_genre = session.query(GameGenre).filter_by(id=request.form['game_genre']).one()
            game_to_edit.game_genre = game_genre
        if request.form['description']:
            game_to_edit.description = request.form['description']

        session.add(game_to_edit)
        session.commit()
        flash('Game Successfully Edited')
        return redirect(url_for('showHomePage'))
    else:
        game_genres = session.query(GameGenre).all()
        return render_template('editPage.html', game_genres=game_genres, game_to_edit=game_to_edit, selected_game_genre=game_to_edit.game_genre, loggedIn=userLoggedIn())


# Delete a game

@app.route('/gamegenres/<int:game_genre_id>/<int:game_id>/delete')
@app.route('/gamegenres/<int:game_genre_id>/games/<int:game_id>/delete', methods=['GET', 'POST'])
@app.route('/<int:game_genre_id>/<int:game_id>/delete')
@app.route('/<int:game_genre_id>/games/<int:game_id>/delete', methods=['GET', 'POST'])
def deleteGame(game_genre_id, game_id):
    if 'username' not in login_session:
        return redirect('/login')

    game_to_delete = session.query(Game).filter_by(id=game_id).one()
    auth_messsage = popUpInfo(game_to_delete, "delete", game_genre_id, game_id)
    if len(auth_messsage) != 0:
        return auth_messsage

    if request.method == 'POST':
        session.delete(game_to_delete)
        session.commit()
        flash('Game Successfully Deleted')
        return redirect(url_for('showGames', game_genre_id=game_genre_id))
    else:
        game_genres = session.query(GameGenre).all()
        return render_template('deletePage.html', game_genres=game_genres, game_to_delete=game_to_delete, game_genre=game_to_delete.game_genre, loggedIn=userLoggedIn())


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
