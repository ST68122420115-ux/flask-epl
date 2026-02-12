from flask import Blueprint ,render_template , url_for, request , flash ,redirect
from epl.extensions import db
from epl.models import Club , Player


player_bp = Blueprint('players', __name__ , template_folder='templates')

@player_bp.route('/')
def index():
  players = db.session.scalars(db.select(Player)).all()
  return render_template('players/index.html', title='Players Page', players=players)


@player_bp.route('/new', methods=['GET', 'POST'])
def new_player():
  clubs = db.session.scalars(db.select(Club)).all()
  if request.method == 'POST':
    name = request.form['name']
    position = request.form['position']
    nationnality = request.form['nationnality']
    goals_value = request.form.get('goals')
    goals = int(goals_value) if goals_value else 0
    clean_sheets_value = request.form.get('clean_sheets')
    squad_no = int(request.form['squad_no'])
    img = request.form['img']
    club_id = int(request.form['club_id'])
    if position == "Goalkeeper":
        clean_sheets = int(clean_sheets_value) if clean_sheets_value else 0
    else:
        clean_sheets = None

    player = Player(name=name, position=position, nationnality=nationnality, goals=goals, squad_no=squad_no, img=img, club_id=club_id , clean_sheets=clean_sheets)
    db.session.add(player)
    db.session.commit()
    flash('add new player successfully', 'success')
    return redirect(url_for('players.index'))
  return render_template('players/new_player.html', title='New Player Page', clubs=clubs)


@player_bp.route('/search', methods=['GET','POST'])
def search_player():
  if request.method == 'POST':
    player_name = request.form['player_name']
    players = db.session.scalars(db.select(Player).where(Player.name.like(f'%{player_name}%'))).all()
    return render_template('players/search_player.html', title='Search Player Page', players=players)
  
@player_bp.route('<int:id>/info')
def info_player(id):
  player = db.session.get(Player,id)
  return render_template('players/info_player.html' , title='Info Player Page', player=player)


@player_bp.route('<int:id>/update' , methods=['GET', 'POST'])
def update_player(id):
  player = db.session.get(Player, id)
  clubs = db.session.scalars(db.select(Club)).all()
  
  if request.method == 'POST':
    name = request.form['name']
    position = request.form['position']
    nationnality = request.form['nationnality']
    goals_value = request.form.get('goals')
    goals = int(goals_value) if goals_value else 0
    clean_sheets_value = request.form.get('clean_sheets')
    squad_no = int(request.form['squad_no'])
    img = request.form['img']
    club_id = int(request.form['club_id'])
    if position == "Goalkeeper":
        clean_sheets = int(clean_sheets_value) if clean_sheets_value else 0
    else:
        clean_sheets = None
    
    player.name = name
    player.position = position
    player.nationnality = nationnality
    player.goals = goals
    player.squad_no = squad_no
    player.img = img
    player.club_id = club_id
    player.clean_sheets = clean_sheets

    db.session.commit()
    flash('update player successfully', 'success')
    return redirect(url_for('players.index'))
  return render_template('players/update_player.html' , title='Update Player Page', player=player , clubs=clubs)
  