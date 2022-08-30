# import library
from ast import Delete
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
class listResource(Resource):

    def get(self):
        # menampilkan data dari database
        query = ModelDatabase.query.all()

        # melakukan iterisasi pada modelDatabase
        output = [{
            "id": data.id,
            "nama": data.nama,
            "umur": data.umur,
            "alamat": data.alamat
        } for data in query]

        response = {
            "code": 200,
            "msg": "Data berhasil ditampilkan",
            "data": output
        }

        return response, 200


class addResource(Resource):

    def post(self):
        dataNama = request.form["nama"]
        dataUmur = request.form["umur"]
        dataAlamat = request.form["alamat"]

        # masukkan data kedalam database model
        model = ModelDatabase(nama=dataNama, umur=dataUmur, alamat=dataAlamat)
        model.save()

        response = {"msg": "Data berhasil ditambahkan", "code": 200}

        return response, 200


class updateResource(Resource):

    def put(self, id):
        # konsumsi id untuk query di model database
        # pilih data yang ingin dirubah berdasarkan id yang dimasukkan
        query = ModelDatabase.query.get(id)

        # form untuk pengeditan data
        editNama = request.form["nama"]
        editUmur = request.form["umur"]
        editAlamat = request.form["alamat"]

        # merubah nilai yang ada pada field database
        query.nama = editNama
        query.umur = editUmur
        query.alamat = editAlamat

        db.session.commit()

        response = {"code": 200, "msg": "Data berhasil dirubah"}

        return response, 200


class deleteResource(Resource):
    # menghapus data berdasarkan id
    def delete(self, id):
        query = ModelDatabase.query.get(id)

        # memanggil methode untuk delete data by id
        db.session.delete(query)
        db.session.commit()

        response = {"code": 200, "msg": "Data berhasil dihapus"}

        return response, 200

class deleteAllResource(Resource):
    # menghapus semua data
    def delete(self):
        query = ModelDatabase.query.all()

        #looping
        for data in query:
            db.session.delete(data)
            db.session.commit()

        response = {"code": 200, "msg": "Data berhasil dihapus semua"}

        return response, 200


# setup resource
api.add_resource(listResource, "/api/list-data", methods=["GET"])
api.add_resource(addResource, "/api/insert-data", methods=["POST"])
api.add_resource(updateResource, "/api/<id>/update-data", methods=["PUT"])
api.add_resource(deleteResource, "/api/<id>/delete-data", methods=["DELETE"])
api.add_resource(deleteAllResource, "/api/delete-data", methods=["DELETE"])

if __name__ == "__main__":
    app.run(debug=True, port=5005)