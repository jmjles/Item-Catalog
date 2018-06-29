from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, SportCategory, MenuItem
from flask import session as login_session
import random,string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
from flask import make_response

CLIENT_ID = json.loads(
    open('client_secrets.json','r').read())['web']['client_id']
app = Flask(__name__)
engine = create_engine('sqlite:///sportmenu.db',connect_args={'check_same_thread':False},)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html',STATE = state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    print("1")

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
    print("2")
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    print("3")
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
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response
    print("4")
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    print("5")
    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    print("6")
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    print("7")
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output

@app.route('/gdisconnect')
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response
    
@app.route('/catalog/JSON')
def sportCategoryJSON():
    category = session.query(SportCategory)
    items = session.query(MenuItem)
    return jsonify(MenuItem = [i.serialize for i in items])
#logged out
@app.route('/')
@app.route('/catalog/')
def sportCategory():
    category = session.query(SportCategory).order_by(SportCategory.sport)
    items = session.query(MenuItem).order_by(MenuItem.date.desc()).limit(10)
    return render_template('mainmenu.html',category = category, items = items)

@app.route('/catalog/<int:category_id>/items/')
def categoryMainMenu(category_id):
    category = session.query(SportCategory).order_by(SportCategory.sport)
    sport = session.query(SportCategory).filter_by(id = category_id)
    items = session.query(MenuItem).filter_by(sport_id = category_id)
    return render_template('menu.html',category = category,items = items, sport = sport)

@app.route('/catalog/<int:category_id>/<int:menu_item_id>')
def categoryMenu(category_id,menu_item_id):
    category = session.query(SportCategory).filter_by(id = category_id)
    items = session.query(MenuItem).filter_by(id = menu_item_id)
    return render_template('desc.html',category = category,items = items,category_id = category_id,menu_item_id = menu_item_id)

#Logged in

@app.route('/catalog/new', methods = ['GET','POST'])
def categoryMenuNew():
    category = session.query(SportCategory).order_by(SportCategory.sport)
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        c = session.query(SportCategory).filter_by(sport=request.form['category']).one()
        newitem = MenuItem(name = request.form['name'],
                           price = request.form['price'],
                           description = request.form['description'],
                           sport_id = c.id,
                           date = datetime.datetime.now())
        session.add(newitem)
        session.commit()
    return render_template('newitem.html', category = category)

@app.route('/catalog/<int:category_id>/<int:menu_item_id>/edit', methods = ['GET','POST'])
def categoryMenuEdit(category_id,menu_item_id):
    category = session.query(SportCategory).order_by(SportCategory.sport)
    if 'username' not in login_session:
        return redirect('/login')
    items = session.query(MenuItem).filter_by(id = menu_item_id).one()
    if request.method == 'POST':
        if request.form['name']:items.name = request.form['name']
        session.add(items)
        session.commit()
    if request.method == 'POST':
        if request.form['description']:items.description = request.form['description']
        session.add(items)
        session.commit()
    if request.method == 'POST':
        if request.form['category']:c = session.query(SportCategory).filter_by(sport=request.form['category']).one()
        items.sport_id = c.id
        session.add(items)
        session.commit()
        return redirect(url_for('categoryMenu', category_id = category_id, menu_item_id = menu_item_id))
    
    return render_template('edititem.html',category_id = category_id,menu_item_id = menu_item_id, i = items, category = category)

@app.route('/catalog/<int:category_id>/<int:menu_item_id>/delete', methods = ['GET','POST'])
def categoryMenuDelete(category_id,menu_item_id):
    items = session.query(MenuItem).filter_by(id = menu_item_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        session.delete(items)
        session.commit()
        return redirect(url_for('sportCategory'))
    return render_template('delete.html',category_id = category_id,menu_item_id = menu_item_id, i = items)

if __name__ == '__main__':
    app.secret_key = 'Fl50YS3lP4JtxoNwiuz4KyC-'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
