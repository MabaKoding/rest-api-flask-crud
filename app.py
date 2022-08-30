# import library
from urllib import response
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

# inisiasi object flask
app = Flask(__name__)

# inisiasi object flask_restful
api = Api(app)

# inisiasi object flask_cors
CORS(app)

# insiasi object flask alchemy
db = SQLAlchemy(app)

# konfigurasi database
basedir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = database


# membuat database model
class ModelDatabase(db.Model):
    # membuat field/kolom
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    umur = db.Column(db.Integer)
    alamat = db.Column(db.TEXT)

    # membuat methode untuk menyimpan data
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False


# create database
db.create_all()

# variabel global bertipe json
identitas = {}


# membuat class Resource
class ContohResource(Resource):
    # method get and post
    def get(self):
        # menampilkan data dari database
        query = ModelDatabase.query.all()

        # melakukan iterisasi pada modelDatabase
        output = [{
            "nama": data.nama,
            "umur": data.umur,
            "alamat": data.alamat
        } for data in query]

        response = {
            "code" : 200,
            "msg"  : "Data berhasil ditampilkan",
            "data" : output
        }

        return response, 200

    def post(self):
        dataNama = request.form["nama"]
        dataUmur = request.form["umur"]
        dataAlamat = request.form["alamat"]

        # masukkan data kedalam database model
        model = ModelDatabase(nama=dataNama, umur=dataUmur, alamat=dataAlamat)
        model.save()

        response = {"msg": "Data berhasil ditambahkan", "code": 200}

        return response, 200


# setup resource
api.add_resource(ContohResource, "/api", methods=["GET", "POST"])

if __name__ == "__main__":
    app.run(debug=True, port=5005)