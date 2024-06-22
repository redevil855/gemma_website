from flask import Flask, render_template, request, redirect, url_for, flash, g,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from models import db, User , Building

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = '123'  # Set a secret key for Flask-Login
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET','POST'])
def vistor():
    return render_template('vistor.html')

@app.route('/jobs', methods=['GET','POST'])
def jobs():
    return render_template('jobs.html')

@app.route('/human_resource_train', methods=['GET','POST'])
def human_resource_train():
    return render_template('human_resource_train.html')

@app.route('/human_resource_train/performance_evaluation', methods=['GET','POST'])
def performance_evaluation():
    return render_template('performance_evaluation.html')

@app.route('/human_resource_train/appointment_employe', methods=['GET','POST'])
def appointment_employe():
    return render_template('appointment_employe.html')

@app.route('/GHR', methods=['GET','POST'])
def GHR():
    return render_template('GHR.html')

@app.route('/application_page', methods=['GET', 'POST'])
def application_page():
    if request.method == 'POST':
        # Handle form submission logic here
        # For example, save the form data to a database
        
        # Redirect back to the jobs page
        return redirect(url_for('jobs'))
    return render_template('application_page.html')

@app.route('/a', methods=['GET', 'POST'])  
def login():
    # Check if the user is logged in
    if current_user.is_authenticated:
        # Fetch the user from the database based on the current_user ID
        # Replace the line below with your actual implementation
        user = User.query.get(current_user.id)
        
        # Set the user in the global context
        g.user = user
    
    return render_template('a.html')
    

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(name=name, password=password).first()
        
        if user:
            session['user_id'] = user.id
            return render_template('home.html', user = user)
    else:
        user_id = session.get('user_id')
        if user_id:
            # Retrieve the user from the database
            user = User.query.get(user_id)
            if user:
                return render_template('home.html', user=user)
            else:
                return 'Access Denied'
        else:
            return redirect(url_for('home'))



@app.route('/employer_dashboard', methods=['GET', 'POST'])  
def employer_dashboard():
    return render_template('employer_dashboard.html')
    
@app.route('/admin_dashboard', methods=['GET', 'POST'])  
def admin_dashboard():
    user_id = session.get('user_id')
    if user_id:
            # Retrieve the user from the database
            user = User.query.get(user_id)
            if user and user.access >= 1:  # Check user access level, assuming 1 as a threshold
                access_zero_count = User.query.filter_by(access=0).count()
                return render_template('admin_dashboard.html', access_zero_count=access_zero_count)
              
            return 'Access Denied'
    else:
           return 'Access Denied'
            
                  

@app.route('/admin_dashboard/current-employers', methods=['GET', 'POST'])  
def currentemployers():
    user_id = session.get('user_id')
    if user_id:
        # Retrieve the user from the database
        user = User.query.get(user_id)
        if user and user.access >= 1:  # Check user access level, assuming 1 as a threshold
            # Fetch data from the database
            employers = User.query.all()  # Assuming User is the model for employers
            access_zero_count = User.query.filter_by(access=0).count()
            
            return render_template('current-employers.html', employers=employers,access_zero_count=access_zero_count)
              
        return 'Access Denied'
    else:
        return 'Access Denied'   
 
@app.route('/admin_dashboard/current-buildings', methods=['GET', 'POST'])  
def currentbuildings():
       
    if request.method == 'GET':
        user_id = session.get('user_id')
        if user_id:
            # Retrieve the user from the database
            user = User.query.get(user_id)
            if user and user.access >= 1:  # Check user access level, assuming 1 as a threshold
                # Fetch buildings from the database
                buildings = Building.query.all()  # Assuming Building is the model for buildings
            
                return render_template('current-buildings.html', buildings=buildings)

            return 'Access Denied'
        else:
            return 'Access Denied'
        

@app.route('/bus_schedules', methods=['GET', 'POST'])  
def bus_schedules():
    return render_template('bus_schedules.html')   

@app.route('/about_us', methods=['GET', 'POST'])  
def about_us():
    return render_template('about_us.html') 

@app.route('/admin_dashboard/new_employer', methods=['GET', 'POST'])
def new_employer():
    return render_template('new_employer.html')

@app.route('/admin_dashboard/new_building', methods=['GET', 'POST'])
def new_building():
    return render_template('new_building.html')

@app.route('/admin_dashboard/work_evaluation', methods=['GET', 'POST'])
def work_evaluation():
    return render_template('work_evaluation.html')



@app.route('/add_employer', methods=['POST'])
def add_employer():
    if request.method == 'POST':
        try:
            name = request.form['name']
            password = request.form['password']
            access = request.form['access']
            building = request.form['building']

            # Create a new Employer instance with the provided form data
            new_employer = User(name=name, password=password, access=access,building=building)

            # Add the new employer to the database session
            db.session.add(new_employer)
            db.session.commit()  # Commit here to generate the employer ID

            # Commit the changes to the database
            db.session.commit()

            # Redirect to the admin dashboard after successfully adding the employer
            flash('Employer and building added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            # Rollback the database session in case of an error
            print(str(e))
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('admin_dashboard'))


@app.route('/add_building', methods=['POST'])
def add_building():
    if request.method == 'POST':
        try:
            
            department = request.form['department']
            

            # Create a new Employer instance with the provided form data
            new_building =Building(department=department)

            # Add the new employer to the database session
            db.session.add(new_building)

            # Commit the changes to the database
            db.session.commit()

            # Redirect to the admin dashboard after successfully adding the employer
            flash('Building added successfully!', 'success')  # Optionally, you can flash a success message
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            # Rollback the database session in case of an error
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'error')  # Flash an error message
            return redirect(url_for('admin_dashboard')) 
        
if __name__ == '__main__':
    app.run(debug=True)
