from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy





app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///promacruds.db'
app.config['SQLALCHEMY_TRACE_MODIFICATION'] = False
app.config['SECRET_KEY'] = '38686699db8a350e76a19df4'
db = SQLAlchemy(app)
app.app_context().push()


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    handler = db.Column(db.String(100))
    
    
    def __init__(self, name, description, handler):
        self.name = name
        self.description = description
        self.handler = handler



@app.route("/")
def index():
    all_data = Data.query.all()
    return render_template("index.html", projects = all_data)


@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        
        name = request.form['name']
        description = request.form['description']
        handler = request.form['handler']
        
        
        my_data = Data(name, description, handler)
        db.session.add(my_data)
        db.session.commit()
        
        flash("Project added successfully")
        
        
        return redirect(url_for('index'))
    
    
@app.route('/update/', methods = ['GET', 'POST'])
def update():
    
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
        
        my_data.name = request.form['name']
        my_data.description = request.form['description']
        my_data.handler = request.form['handler'] 
        
        
        db.session.commit()
        flash("Project Updated Successfully")
        
        return redirect(url_for('index'))
    
    
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Project Deleted Successfully")
    
    return redirect(url_for('index'))
    
    


if __name__ == "__main__":
    app.run(debug=True)
    