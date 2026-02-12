from flask import Blueprint ,render_template , url_for, request , flash ,redirect
from epl.extensions import db
from epl.models import Club

club_bp = Blueprint('clubs', __name__ , template_folder='templates')

#@club_bp.route('/')
#def index():
 # query = db.select(Club)
 # clubs = db.session(query).all()
 # render_template('clubs/index.html', title='Clubs Page' , clubs=clubs)
  
@club_bp.route('/')
def index():
  query = db.select(Club)
  clubs = db.session.execute(query).scalars().all()
  return render_template('clubs/index.html', title='Clubs Page', clubs=clubs)


@club_bp.route('/new', methods=['GET', 'POST'])
def new_club():
    if request.method == 'POST':
        name = request.form['name']
        stadium = request.form['stadium']
        year = int(request.form['year'])
        logo = request.form['logo']

        existing_club = db.session.scalar(db.select(Club).where(Club.name == name))

        if existing_club:
            flash('this club already exists!', 'danger')
            return redirect(url_for('clubs.new_club'))

        club = Club(name=name, stadium=stadium, year=year, logo=logo)
        db.session.add(club)
        db.session.commit()

        flash('Add new club successfully', 'success')
        return redirect(url_for('clubs.index'))

    return render_template('clubs/new_club.html', title='New Club Page')


@club_bp.route('/search', methods=['GET', 'POST'])
def search_club():
  if request.method == 'POST':
    club_name = request.form['club_name']
    clubs = db.session.scalars(db.select(Club).where(Club.name.like(f'%{club_name}%'))).all()
    return render_template('clubs/search_club.html', title='Search Club Page', clubs=clubs)
  
  
@club_bp.route('/<int:id>/info')
def info_club(id):
  club = db.session.get(Club, id)
  return render_template('clubs/info_club.html', title='Info Club Page', club=club)


@club_bp.route('/<int:id>/update', methods=['GET','POST'])
def update_club(id):
  club = db.session.get(Club, id)
  if request.method == 'POST':
    name = request.form['name']
    stadium = request.form['stadium']
    year = int(request.form['year'])
    logo = request.form['logo']

    club.name = name
    club.stadium = stadium
    club.year = year
    club.logo = logo

    db.session.add(club)
    db.session.commit()

    flash('update club successfully', 'success')
    return redirect(url_for('clubs.index'))
  return render_template('clubs/update_club.html', title='Update Club Page', club=club)