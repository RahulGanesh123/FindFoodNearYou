from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from  whitenoise import WhiteNoise
from datetime import datetime


app = Flask(__name__)
app.wsgi_app = WhiteNoise(app.wsgi_app, root='templates/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
my_static_folders = (
    'templates/css/',
    'templates/img/',
    'templates/scss/',
    'templates/vendor/bootstrap/',
    'templates/vendor/jquery/'
)
for static in my_static_folders:
    app.wsgi_app.add_files(static)


class FoodBank(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    address = db.Column(db.String(200), nullable = False)
    donation_link = db.Column(db.String(400), nullable = False)
    zipcode = db.Column(db.String(100), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<FoodBank %r>' % self.name
@app.route('/admin', methods = ['POST','GET'])
def enterInfo():
    if(request.method == 'POST'):
        foodbank_name = request.form['name']
        foodbank_address = request.form['address']
        foodbank_donation_link = request.form['donation_link']
        foodbank_zipcode = request.form['zipcode']
        new_foodbank = FoodBank(name=foodbank_name,address=foodbank_address,donation_link=foodbank_donation_link, zipcode = foodbank_zipcode)
        try:
            db.session.add(new_foodbank)
            db.session.commit()
            return redirect('/admin')
        except:
            return 'There was an error adding the foodbank'
    else:
        foodbanks = FoodBank.query.order_by(FoodBank.date_created).all()
        return render_template('index.html', foodbanks = foodbanks)

@app.route('/admin/delete/<int:id>')
def delete(id):
    foodbank_to_delete = FoodBank.query.get_or_404(id)

    try:
        db.session.delete(foodbank_to_delete)
        db.session.commit()
        return redirect('/admin')
    except:
        return 'There was a problem deleting that task'
@app.route('/admin/update/<int:id>', methods=[ 'POST', 'GET'])
def update(id):
    foodbank_to_update = FoodBank.query.get_or_404(id)

    if request.method == 'POST':
        foodbank_to_update.name = request.form['name']
        foodbank_to_update.address = request.form['address']
        foodbank_to_update.donation_link = request.form['donation_link']
        foodbank_to_update.zipcode = request.form['zipcode']
        
        try:
            db.session.commit()
            return redirect('/admin')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', foodbank=foodbank_to_update)

@app.route('/regUser', methods = ['POST','GET'])
def foodbankInfo():
    if(request.method == 'POST'):
        foodbank_name = request.form['name']
        foodbank_address = request.form['address']
        foodbank_donation_link = request.form['donation_link']
        foodbank_zipcode = request.form['zipcode']
        new_foodbank = FoodBank(name=foodbank_name,address=foodbank_address,donation_link=foodbank_donation_link, zipcode = foodbank_zipcode)
        try:
            db.session.add(new_foodbank)
            db.session.commit()
            return redirect('/regUser')
        except:
            return 'There was an error adding the foodbank'
    else:
        foodbanks = FoodBank.query.order_by(FoodBank.date_created).all()
        return render_template('regUser.html', foodbanks = foodbanks)
@app.route('/query_by_zip', methods = ['GET'])
def findfoodbanksnearyou():
    if(request.method == 'GET'):
        foodbank_zipcode = request.args.get('zipcode')
        foodbanks = FoodBank.query.filter_by(zipcode=foodbank_zipcode).all()
        return render_template('regUser.html', foodbanks = foodbanks)

@app.route('/', methods = ['GET'])
def homepage():
    return render_template('HomePage.html')
        
if __name__ == "__main__":
    app.run(debug=True) 