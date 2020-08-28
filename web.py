from flask import *
from shouhin import Shouhin,ShouhinDB
from uriage import Uriage,UriageDB
app = Flask(__name__)

@app.route('/')
def index():
    db = ShouhinDB()
    shouhins = db.find_all()
    db.close()
    return render_template("index.html",title="販売管理",shouhins=shouhins)

@app.route('/add',methods=['post'])
def add():
    sname = request.form['sname']
    tanka = request.form['tanka']

    if not sname:
        return redirect('/')
    if not tanka:
        return redirect('/')

    s = Shouhin(0,sname,tanka)

    return render_template("add.html",title="商品の追加",shouhin=s)

@app.route('/',methods=['post'])
def add_post():
    sname = request.form['sname']
    tanka = request.form['tanka']
    db = ShouhinDB()
    s = Shouhin(0,sname,tanka)
    db.insert(s)
    db.close()
    return redirect('/')

@app.route('/del')
def del_kakunin():
    sid = request.args.get('sid')
    db = ShouhinDB()
    s = db.find(sid)
    db.close()
    return render_template("del.html",title="商品の削除",shouhin=s)

@app.route('/del',methods=['post'])
def del_post():
    sid = request.form['sid']
    db = ShouhinDB()
    db.delete(sid)
    db.close()
    return redirect('/')

@app.route('/update')
def update():
    sid = request.args.get('sid')
    db = ShouhinDB()
    s = db.find(sid)
    db.close()
    return render_template("update.html",title="商品の更新",shouhin=s)

@app.route('/update',methods=['post'])
def update_post():
    sid = request.form['sid']
    sname = request.form['sname']
    tanka = request.form['tanka']
    
    db = ShouhinDB()
    s = Shouhin(sid,sname,tanka)
    db.update(s)
    db.close()
    return redirect('/')

@app.route('/uriage')
def uriage():
    sid = request.args.get('sid')
    sdb = ShouhinDB()
    s = sdb.find(sid)
    sdb.close()

    udb = UriageDB()
    uriages = udb.find_by_sid(sid)
    udb.close()

    return render_template("uriage.html",title=f"{s.sname} 売り上げ",shouhin=s,uriages=uriages)

@app.route('/uadd',methods=['post'])
def uadd_post():
    sid = request.form['sid']
    kosu = request.form['kosu']

    db = UriageDB()
    u = Uriage(0,sid,kosu,None)
    db.insert(u)
    db.close()
    return redirect('/uriage?sid=' + sid)

app.run(debug=True)
