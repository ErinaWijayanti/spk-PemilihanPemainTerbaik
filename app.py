from flask import Flask, redirect, render_template, session, request, jsonify, url_for
from datetime import timedelta
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os
import requests
import json

# init dotenv
load_dotenv()

URL_ENDPOINT = os.getenv('URL_ENDPOINT')
API_KEY = os.getenv('API_KEY')
DATA_SOURCE = os.getenv('DATA_SOURCE')
DATABASE = os.getenv('DATABASE')
COLLECTION = os.getenv('COLLECTION')

headers = {
	'Content-Type': 'application/json',
	'Access-Control-Request-Headers': '*',
	'api-key': API_KEY, 
}

app = Flask(__name__)
# app.secret_key digunakan sebagai kunci rahasia untuk menandatangani cookie sesi dan mengamankan data sesi dari manipulasi.
app.secret_key = os.getenv('SECRET_KEY')

@app.before_request
def sesi():
	app.permanent_session_lifetime = timedelta(minutes=60)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

# Konfigurasi untuk tempat penyimpanan file
# UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'csv', 'json'}
# MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Fungsi untuk memeriksa ekstensi file yang diizinkan
# def allowed_file(filename):
# 	return '.' in filename and \
# 		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# Fungsi untuk meng-handle permintaan pengunggahan file
# @app.route('/upload', methods=['POST'])
# def upload_file():
# 	# Memeriksa apakah ada file yang dikirim dalam permintaan
# 	if 'file' not in request.files:
# 			return 'File not found', 400

# 	file = request.files['file']

# 	# Memeriksa apakah file diperbolehkan
# 	if file and allowed_file(file.filename):
# 		filename = secure_filename(file.filename)
# 		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# 		return 'File uploaded successfully', 200
# 	else:
# 		return 'File type not allowed', 400

@app.route('/', methods=['GET', 'POST'])
def home():
	if 'username' and 'password' in session:
		return render_template('home.html')
	return redirect('/login')

@app.route("/tambah-data",  methods=['POST'])
def tambah_data():
	if 'username' and 'password' in session:
		# mengambil data dari form
		namaPemain = request.form['namaPemain']
		averageGpm = request.form['averageGpm']
		averageKda = request.form['averageKda']
		averageDamage = request.form['averageDamage']
		averageDamageDiterima = request.form['averageDamageDiterima']
		komunikasi = request.form['komunikasi']
		teamFight = request.form['teamFight']
		turnYgDijuarai = request.form['turnYgDijuarai']
		namaHero = request.form['namaHero']
		heroPower = request.form['heroPower']
		pertandingan = request.form['pertandingan']
		winRate = request.form['winRate']

		if namaPemain != '' and averageGpm  != 0 and averageKda != 0 and averageDamage != 0 and averageDamageDiterima != 0 and komunikasi  != 0 and teamFight != 0 and turnYgDijuarai != 0 and namaHero != '' and heroPower != 0 and pertandingan != 0 and winRate != 0:
			url = URL_ENDPOINT+"/action/insertOne"
			payload = json.dumps({
				"dataSource": DATA_SOURCE,
				"collection": COLLECTION,
				"database": DATABASE,
				"document": {
					'nama_pemain': namaPemain,
					'avg_gpm': int(averageGpm),
					'avg_kda': averageKda,
					'avg_damage': averageDamage,
					'avg_dmg_diterima': averageDamageDiterima,
					'komunikasi': int(komunikasi),
					'team_fight': teamFight,
					'tourn_yg_dijuarai': turnYgDijuarai,
					'nama_hero': namaHero,
					'hero_power': heroPower,
					'pertandingan': pertandingan,
					'win_rate': winRate,
				}
			})
			
			response = requests.request("POST", url, headers=headers, data=payload)
			json_response = response.json()
			if json_response['insertedId'] != '':
				return jsonify({
					'status': True,
					'msg':'Data berhasil ditambahkan'
				})
			return jsonify({
				'status': False,
				'msg':'Data gagal ditambahkan'
			})
		return jsonify({
			'status':False,
			'msg':'Inputan data tidak valid, mohon inputkan data dengan sesuai'
		})
	return redirect('/login')

@app.route("/edit-data",  methods=['POST'])
def edit_data():
	if 'username' and 'password' in session:
		status = False
		msg = ''
		# mengambil data dari form
		_id= request.form['id-edit-pemain']
		namaPemain = request.form['edit-nama-pemain']
		averageGpm = request.form['edit-avg-gpm']
		averageKda = request.form['edit-avg-kda']
		averageDamage = request.form['edit-avg-damage']
		averageDamageDiterima = request.form['edit-avg-damage-diterima']
		komunikasi = request.form['edit-komunikasi']
		teamFight = request.form['edit-team-fight']
		turnYgDijuarai = request.form['edit-turn-yg-dijuarai']
		namaHero = request.form['edit-nama-hero']
		heroPower = request.form['edit-hero-power']
		pertandingan = request.form['edit-pertandingan']
		winRate = request.form['edit-win-rate']

		if namaPemain != '' and averageGpm != 0 and averageKda != 0 and averageDamageDiterima != 0 and komunikasi != 0 and teamFight != 0 and turnYgDijuarai != 0 and namaHero != 0 and heroPower != 0 and pertandingan != 0 and winRate != 0:
			url = URL_ENDPOINT+"/action/updateOne"
			payload = json.dumps({
				"dataSource": DATA_SOURCE,
				"collection": COLLECTION,
				"database": DATABASE,
				"filter": {
					"_id": {"$oid":_id},
				},
				"update": {
					"$set":
						{
						'nama_pemain': namaPemain,
						'avg_gpm': averageGpm,
						'avg_kda': averageKda,
						'avg_damage': averageDamage,
						'avg_dmg_diterima': averageDamageDiterima,
						'komunikasi': komunikasi,
						'team_fight': teamFight,
						'tourn_yg_dijuarai': turnYgDijuarai,
						'nama_hero': namaHero,
						'hero_power': heroPower,
						'pertandingan': pertandingan,
						'win_rate': winRate,
					}
				}
			})
			
			response = requests.request("POST", url, headers=headers, data=payload)
			if response.status_code == 200:
				json_response = response.json()
				if json_response['matchedCount'] != 1:
					msg = 'Edit data gagal karena id data tidak ditemukan!'
					return
				elif json_response['modifiedCount'] != 1:
					msg = 'data ditemukan, tetapi gagal melakukan edit data!'
					return
				else:
					status = True
					msg = 'Berhasil melakukan edit data :)'
			else:
				msg = f'''Gagal melakukan edit data dengan status code {response.status_code}'''
		return jsonify({
			'status': status,
			'msg': msg,
		})
	return redirect('/login')

@app.route('/get-one-data/<string:id>', methods=['POST'])
def get_one_data(id):
	if 'username' and 'password' in session:
		status = False
		msg = ''
		data = {}
		url = URL_ENDPOINT+"/action/findOne"
		payload = json.dumps({
			"dataSource": DATA_SOURCE,
			"collection": COLLECTION,
			"database": DATABASE,
			"filter": {
				"_id": {"$oid":id},
			}
		})

		response = requests.request("POST", url, headers=headers, data=payload)
		json_response = response.json()

		if json_response['document'] != None:
			status = True
			data = json_response['document']
		else:
			msg = 'Data not found'
		data = {
			'status' : status,
			'msg': msg,
			'data': data,
		}
		return jsonify(data)
	return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST':
		msg = ''

		# mengambil data dari form
		username = request.form['username']
		password = request.form['password']

		url = URL_ENDPOINT+"/action/findOne"
		payload = json.dumps({
			"dataSource": DATA_SOURCE,
			"collection": "user",
			"database": DATABASE,
			"filter": {
				"username": username,
				"password": password
			}
		})

		response = requests.request("POST", url, headers=headers, data=payload)
		json_response = response.json()

		if json_response['document'] != None:
			if username == json_response['document']['username'] and password == json_response['document']['password']:
				session['username'] = username
				session['password'] = password
				return redirect('/')
			else:
				msg = 'Username atau Password yang anda masukkan salah, silahkan coba lagi'
		else:
			msg = 'Username atau Password tidak ditemukan'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	# Menghapus data sesi
	session.pop('username', None)
	session.pop('password', None)
	# Redirect ke halaman login atau halaman beranda
	return redirect(url_for('login'))

@app.route('/indexData', methods=['POST'])
def index_data():
	if 'username' and 'password' in session:
		status = False
		data = []
		url = URL_ENDPOINT+"/action/find"
		payload = json.dumps({
			"dataSource": DATA_SOURCE,
			"collection": COLLECTION,
			"database": DATABASE,
			"filter": {},
			"sort": {"_id": -1}
		})
		response = requests.request("POST", url, headers=headers, data=payload)
		json_response = response.json()
		# print(json_response)

		if json_response != 'undefined':
			text = ''
			documents = json_response['documents']
			for doc in documents:
				_id = doc['_id']
				namaPemain = doc['nama_pemain']
				averageGpm = doc['avg_gpm']
				averageKda = doc['avg_kda']
				averageDamage = doc['avg_damage']
				averageDamageDiterima = doc['avg_dmg_diterima']
				komunikasi = doc['komunikasi']
				teamFight = doc['team_fight']
				turnYgDijuarai = doc['tourn_yg_dijuarai']
				namaHero = doc['nama_hero']
				heroPower = doc['hero_power']
				pertandingan = doc['pertandingan']
				winRate = doc['win_rate']

				text += f'''
				<tr>
					<td style="display: none;">{_id}</td>
					<td>{namaPemain}</td>
					<td>{averageGpm}</td>
					<td>{averageKda}</td>
					<td>{averageDamage}</td>
					<td>{averageDamageDiterima}</td>
					<td>{komunikasi}</td>
					<td>{teamFight}</td>
					<td>{turnYgDijuarai}</td>
					<td>{namaHero}</td>
					<td>{heroPower}</td>
					<td>{pertandingan}</td>
					<td>{winRate}</td>
				<td>
					<div class="button-group">
						<button id="{_id}" class="btn btn-info btn-edit"><i class="fas fa-edit" title="Edit Data"></i></button>
						<button id="{_id}" class="btn btn-danger btn-hapus"><i class="fas fa-trash" title="Hapus Data"></i></button>
					</div>
				</td>
				</tr>
				'''
				status = True

		data = {
			'status' : status,
			'res': text,
			'documents': documents,
		}
		return data
	return redirect('/login')

@app.route('/delete-one/<string:id>', methods=['DELETE'])
def delete_one(id):
	if 'username' and 'password' in session:
		status = False
		msg = ''

		url = URL_ENDPOINT+"/action/deleteOne"
		payload = json.dumps({
			"dataSource": DATA_SOURCE,
			"collection": COLLECTION,
			"database": DATABASE,
			"filter": {
				"_id": {"$oid":id},
			}
		})

		response = requests.request("POST", url, headers=headers, data=payload)
		json_res = response.json()
		if json_res['deletedCount'] == 1:
			status = True
			msg = 'Data Berhasil dihapus'
			return jsonify(
				{
					'status':status,
					'msg':msg,
				}
			)
		return jsonify(
			{
				'status':status,
				'msg':msg,
			}
		)
	return redirect('/login')

@app.route("/metodesaw", methods=['GET', 'POST'])
def methode_saw():
	if 'username' and 'password' in session:
		return render_template('metode-spk-saw.html')
	return redirect('/login')

def getData(id):
	if 'username' and 'password' in session:
		url = URL_ENDPOINT+"/action/findOne"
		payload = json.dumps({
			"dataSource": DATA_SOURCE,
			"collection": COLLECTION,
			"database": DATABASE,
			"filter": {
				"_id": {"$oid":id},
			}
		})
		response = requests.request("POST", url, headers=headers, data=payload)
		json_response = response.json()
		return json_response['document']
	return redirect('/login')

def getAllDataTraining():
	if 'username' and 'password' in session:
		data = {}
		_id = []

		url = URL_ENDPOINT+"/action/find"
		payload = json.dumps({
			"dataSource": DATA_SOURCE,
			"collection": COLLECTION,
			"database": DATABASE,
			"filter": {}
		})
		response = requests.request("POST", url, headers=headers, data=payload)
		json_response = response.json()
		if json_response != 'undefined':
			documents = json_response['documents']
			# print(documents)
			for doc in documents:
				data[doc['_id']]={
					'C1':float(doc['avg_gpm']),
					'C2':float(doc['avg_kda']),
					'C3':float(doc['avg_damage']),
					'C4':float(doc['avg_dmg_diterima']),
					'C5':float(doc['komunikasi']),
					'C6':float(doc['team_fight']),
					'C7':float(doc['tourn_yg_dijuarai']),
					'C8':float(doc['hero_power']),
					'C9':float(doc['pertandingan']),
					'C10':float(doc['win_rate']),
				}
				_id.append({doc['_id'] : doc['_id']})
			return {'data':data, 'id':_id}
		return redirect('/login')

@app.route("/indexRanking", methods=['POST'])
def index_ranking():
	if 'username' and 'password' in session:
		paramKriteria = request.get_json()
		test = {}
		j = 1
		for i in paramKriteria:
			test['C' + str(j)] = {'rating': i['rating'], 'atribut': i['atribut']}
			j += 1
		
		status = False
		res = []

		allData = getAllDataTraining()
		data = allData["data"]
		if len(data) != 0:
			status = True

			kriteria = test

			# mendapatkan rating kriteria 
			rating =[kriteria[i]['rating'] for i in kriteria.keys()]

			# normalisasi bobot 
			bobot = [val/sum(rating) for val in rating]

			C_MaxMin = []

			#perulangan utk dpt atribut kriteria
			for key in kriteria.keys():
				C = [
					data[i][key] for i in data.keys()
				]

				#periksa atribut apkah cost / benefit
				if kriteria[key]['atribut'] == 'benefit':
					C_MaxMin.append(max(C))
				else:
					C_MaxMin.append(min(C))
			
			#normalisasi
			norms = []
			v = []
			n=0
			for vals in data.values():
				norm = []
				i = 0
				vn = 0
				#langkah mendapat atribut kriteria
				for key, val in vals.items():
					#cek atribut apakah cost / benefit
					if kriteria[key]['atribut'] == 'benefit':
						n = val/C_MaxMin[i] #menyimpan normalisasi dlam var n
					else:
						C_MaxMin.append(min(C))
					
					#menghitung vn
					vn += (n * bobot[i])
					norm.append(n)
					i+=1
				#simpan hasil normalisasi
				norms.append(norm)
				#simpan vn ke dalam vektor v
				v.append(round(vn,3))
			
			#langkah perangkingan
			rank = {}
			i = 0
			for key in data.keys():
				rank[key] = v[i]
				i+=1

			sorted_rank = sorted(
				[
					(value, key) for (key, value) in rank.items()
				], reverse=True
			)

			for i in sorted_rank:
				cek = getData(i[1])
				res.append([i[0],cek])

		return jsonify({'status': status,'res': res,})
	return redirect('/login')


# testing local
# if __name__ == "__main__":
# 	app.run(debug=True)