from __init__ import session
from __init__ import Base
from jelo import Jelo
from kategorija import Kategorija

import os 

from flask import Flask,render_template, request,redirect, url_for,flash


app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../templates'))

app.secret_key = 'ovo-je-moj-tajni-kljuc'
app.config['SESSION_TYPE'] = 'filesystem'



@app.route("/")
def index ():
    jela = session.query(Jelo).all()
    kategorije = session.query(Kategorija).all()  
    return render_template('home.html', jela=jela,kategorije=kategorije)

@app.route('/dodaj-jelo', methods=['POST'])
def dodaj_jelo():
    naziv = request.form.get('naziv')
    opis = request.form.get('opis')
    kategorija_id = request.form.get("kategorija_id")
    cijena = request.form.get('cijena')
    print("kategorija_id:", kategorija_id)  
    
    
    novo_jelo = Jelo(naziv=naziv, ID_kategorija=kategorija_id, opis=opis, cijena=cijena)
    session.add(novo_jelo)
    session.commit()

    return redirect(url_for('index'))


@app.route("/kategorija")
def kategorija():
    kategorije = session.query(Kategorija).all()
    return render_template('kategorija.html', kategorije=kategorije)

 

@app.route('/dodaj-kategoriju', methods=['POST'])
def dodaj_kategoriju():
    naziv = request.form.get('naziv')

    nova_kategorija = Kategorija(naziv=naziv)
    session.add(nova_kategorija)
    session.commit()

    flash('Kategorija je uspješno dodana.', 'success')
    return redirect(url_for('kategorija'))


@app.route('/izbrisi_kategoriju/<int:ID_kategorija>', methods=['POST'])
def izbrisi_kategoriju(ID_kategorija):
    kategorija = session.query(Kategorija).get(ID_kategorija)
    print(kategorija)
    if kategorija:
        
        session.delete(kategorija)
        session.commit()
        flash('Kategorija je uspješno obrisana.', 'warning')
    else:
        flash('Kategorija nije pronađena.', 'error')

    return redirect(url_for('kategorija'))

@app.route('/izbrisi_jelo/<int:ID_food>', methods=['POST'])
def izbrisi_jelo(ID_food):
    jelo = session.query(Jelo).get(ID_food)
    
    if jelo:
        
        session.delete(jelo)
        session.commit()  

    return redirect(url_for('index'))

@app.route('/uredi_jelo/<int:ID_food>')
def uredi_jelo(ID_food):
    jelo = session.query(Jelo).get(ID_food)
    kategorije = session.query(Kategorija).all()
    return render_template('edit_jelo.html', jelo=jelo, kategorije=kategorije)

@app.route('/azuriraj_jelo/<int:ID_food>', methods=['POST'])
def azuriraj_jelo(ID_food):
    jelo = session.query(Jelo).get(ID_food)
    if jelo:
        jelo.naziv = request.form.get('naziv')
        jelo.opis = request.form.get('opis')
        jelo.kategorija_id = request.form.get('kategorija_id')
        jelo.cijena = request.form.get('cijena')
        session.commit()
        flash('Jelo je uspješno ažurirano.', 'success')
    else:
        flash('Jelo nije pronađeno.', 'error')

    return redirect(url_for('index'))

 

app.debug = True

if __name__ == '__main__':
     app.run(host="0.0.0.0", port=5000)