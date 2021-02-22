# Imports API
from flask import jsonify
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_migrate import Migrate
import mysql.connector
from mysql.connector.constants import ClientFlag

config = {
    'user': 'root',
    'password': 'challenge48h',
    'host': '104.197.252.23',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'ssl/server-ca.pem',
    'ssl_cert': 'ssl/client-cert.pem',
    'ssl_key': 'ssl/client-key.pem',
    'database': 'challenge'
}

cnxn = mysql.connector.connect(**config)
cursor = cnxn.cursor()

# try :
#     cursor.execute("DROP TABLE picture")
# except :
#     pass
# cursor.execute("CREATE TABLE picture ("
#                "id int AUTO_INCREMENT PRIMARY KEY,"
#                "picture VARCHAR(8000),"
#                "category VARCHAR(255) )")
# cnxn.commit()

# try :
#     cursor.execute("DROP TABLE tag")
# except :
#     pass
# cursor.execute("CREATE TABLE tag ("
#                "id int AUTO_INCREMENT PRIMARY KEY,"
#                "name VARCHAR(255) )")
# cnxn.commit()

# cnxn = mysql.connector.connect(**config)
# cursor = cnxn.cursor()

# try :
#     cursor.execute("DROP TABLE picture_tag")
# except :
#     pass
# cursor.execute("CREATE TABLE picture_tag ("
#                "id_picture int(255),"
#                "id_tag int(255))")
# cnxn.commit()

# cnxn.close()

# add_pic = ("INSERT INTO picture "
#               "(picture, category)"
#               "VALUES (%(picture)s, %(category)s)")
# data_pic = {
#   'picture': "qwerty",
#   'category': "ambiance"
# }
# cursor.execute(add_pic, data_pic)
# cnxn.commit() 

# add_tag = ("INSERT INTO tag "
#               "(name)"
#               "VALUES (%(name)s)")
# data_tag = {
#   'name': "test"
# }
# cursor.execute(add_tag, data_tag)
# cnxn.commit() 

# add_pic = ("INSERT INTO picture_tag "
#               "(id_picture, id_tag)"
#               "VALUES (%(picture)s, %(tag)s)")
# data_pic = {
#   'picture': "1",
#   'tag': "1"
# }
# cursor.execute(add_pic, data_pic)
# cnxn.commit() 

# cursor.execute("SELECT * FROM picture")
# fetch = cursor.fetchall()
# for i in fetch:
#     print(i)

# cursor.execute("SELECT * FROM tag")
# fetch = cursor.fetchall()
# for i in fetch:
#     print(i)

# cursor.execute("SELECT * FROM picture_tag")
# fetch = cursor.fetchall()
# for i in fetch:
#     print(i)

cnxn.close()

# Initiate APP
app = Flask(__name__)
# Initiate API
api = Api(app)

# Create Img, Delete Img (picture + picture_tag)
# Update sur picture_tag
# Crud sur tag

# Pictures
class GetImages(Resource):
    #Vérifier les doublons
    def get(self):
        cnxn = mysql.connector.connect(**config)
        cursor = cnxn.cursor(buffered=True)
        # On récupère les tags dans le body de la request
        req = request.json
        tags = req["names"]
        formated_tags = "("
        for tag in tags :
            formated_tags = formated_tags + "\'" + tag + "\',"
        formated_tags = formated_tags[:-1] + ")"
        print(formated_tags)
        # On Récupère les ids des tags
        search_tags = "SELECT id FROM tag where name IN " + formated_tags
        print(search_tags)
        id_tags = cursor.execute(search_tags)
        cnxn.commit() 
        print("///////////////////// ID TAGS /////////////////////")
        print(id_tags)
        # traitement a faire sur id_tags pour que la string ai cette gueule : ('1','2'...)
        # On récupère les ids des pictures en fonction des tags
        get_pics = ("SELECT id_picture FROM picture_tag where "
              "id_tag IN " + id_tags)
        id_pics = cursor.execute(get_pics)
        cnxn.commit() 
        # récupérer les paths des pictures
        get_paths = ("SELECT picture, category FROM picture where "
              "id IN " + id_pics)
        cnxn.commit() 
        print(get_paths)
        # Send
        cnxn.close()
        return 

class Image(Resource):
    # récupérer
    def get(self):
        cnxn = mysql.connector.connect(**config)
        cursor = cnxn.cursor()

        cnxn.close()
        return
    
    # Ajouter
    def post(self):
        cnxn = mysql.connector.connect(**config)
        cursor = cnxn.cursor()

        cnxn.close()
        return
    
    # Mettre a jour
    def update(self):
        cnxn = mysql.connector.connect(**config)
        cursor = cnxn.cursor()

        cnxn.close()
        return

    def delete(self):
        cnxn = mysql.connector.connect(**config)
        cursor = cnxn.cursor()

        cnxn.close()
        return

# Tags
class GetTags(Resource):
    def get(self):
        cnxn = mysql.connector.connect(**config)
        cursor = cnxn.cursor()

        cnxn.close()
        return

class Tag(Resource):
    def get(self):
        cnxn = mysql.connector.connect(**config)
        cursor = cnxn.cursor()

        cnxn.close()
        return

    def post(self):
        cnxn = mysql.connector.connect(**config)
        cursor = cnxn.cursor()

        cnxn.close()
        return

    def update(self):
        cnxn = mysql.connector.connect(**config)
        cursor = cnxn.cursor()

        cnxn.close()
        return

    def delete(self):
        cnxn = mysql.connector.connect(**config)
        cursor = cnxn.cursor()

        cnxn.close()
        return

api.add_resource(GetImages, "/images")
api.add_resource(Image,     "/image")
api.add_resource(GetTags,   "/tags")
api.add_resource(Tag,       "/tag")

if __name__ == "__main__":
    app.run(debug=True)