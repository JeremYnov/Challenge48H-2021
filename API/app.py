# Imports API
from flask import jsonify
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
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

# add_pic = ("INSERT INTO picture "
#               "(image)"
#               "VALUES (\"azerty\")")
# cursor.execute(add_pic)
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
#   'picture': "2",
#   'tag': "2"
# }
# cursor.execute(add_pic, data_pic)
# cnxn.commit() 

cursor.execute("SELECT * FROM picture")
fetch = cursor.fetchall()
for i in fetch:
    print(i)

cursor.execute("SELECT * FROM tag")
fetch = cursor.fetchall()
for i in fetch:
    print(i)

cursor.execute("SELECT * FROM picture_tag")
fetch = cursor.fetchall()
for i in fetch:
    print(i)

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
        get_no_tagged = 0
        imgs = []
        # On récupère les tags dans le body de la request
        req = request.json
        tags = req["tags"]
        # Test si on veut avoir les images sans tags
        if 'notags' in tags:
            get_no_tagged = 1
        # S'ils y a des tags et que 'notag' n'est pas le seul tag
        if tags and get_no_tagged == 1 and len(tags) >= 2 :
            # On formate une string avec les tags pour concaténer a la requete SQL
            formated_tags = "("
            for tag in tags :
                formated_tags = formated_tags + "\'" + tag + "\',"
            formated_tags = formated_tags[:-1] + ")"
            # On Récupère les ids des tags
            search_tags = "SELECT * FROM tag where name IN " + formated_tags
            cursor.execute(search_tags)
            id_tags = cursor.fetchall()
            # On formate une string avec les tags pour concaténer a la requete SQL
            formated_result = "("
            for id_tag in id_tags :
                formated_result = formated_result +  str(id_tag[0]) + ","
            formated_result = formated_result[:-1] + ")"
            # On récupère les ids des pictures en fonction des tags
            get_pics = ("SELECT id_picture FROM picture_tag where id_tag IN " + formated_result)
            cursor.execute(get_pics)
            id_pics = cursor.fetchall()
            # On formate une string avec les tags pour concaténer a la requete SQL
            formated_pics = "("
            for id_pic in id_pics :
                formated_pics = formated_pics + str(id_pic[0]) + ","
            formated_pics = formated_pics[:-1] + ")"
            # récupérer les paths des pictures
            get_paths = ("SELECT * FROM picture where id IN " + formated_pics)
            cursor.execute(get_paths)
            imgs.append(cursor.fetchall())
        # Si le seul tag c'est les images sans tag
        if tags and get_no_tagged == 1 and len(tags) == 1:
            # on récupère tous les ids des photos qui ne sont pas dans la table de relation entre tags et images
            get_pics_ids = ("SELECT * FROM picture_tag")
            cursor.execute(get_pics_ids)
            get_pics_ids = cursor.fetchall()
            # On formate une string avec les tags pour concaténer a la requete SQL
            formated_pics_ids = "("
            for id_pic_id in get_pics_ids :
                formated_pics_ids = formated_pics_ids + str(id_pic_id[0]) + ","
            formated_pics_ids = formated_pics_ids[:-1] + ")"
            # On recherche les images qui ont un id pas dans le résultat de la requête précédente
            get_imgs_not_tagged = ("SELECT * FROM picture where id NOT IN " + formated_pics_ids)
            cursor.execute(get_imgs_not_tagged)
            imgs.append(cursor.fetchall())
        cnxn.close()
        print(imgs)
        return

class Image(Resource):
    # récupérer
    def get(self):
        cnxn = mysql.connector.connect(**config)
        cursor = cnxn.cursor()
        # On récupère les tags dans le body de la request
        req = request.json
        img_id = req['id']
        get_paths = ("SELECT * FROM picture where id = " + str(img_id))
        cursor.execute(get_paths)
        image = cursor.fetchall()
        print(image)
        cnxn.close()
        return
    
    # Ajouter
    def post(self):
        cnxn = mysql.connector.connect(**config)
        cursor = cnxn.cursor()
        req = request.json
        img_nom                             = req['nom']
        type_image                          = req['type_image']
        photo_avec_produit                  = req['photo_avec_produit']
        photo_avec_humain                   = req['photo_avec_humain']
        photo_institutionnelle              = req['photo_institutionnelle']
        format_img                          = req['format_img']
        credits_photo                       = req['credits_photo']
        droits_utilisation_limite           = req['droits_utilisation_limite']
        copyright_img                       = req['copyright_img']
        date_de_fin_droits_utilisation      = req['date_de_fin_droits_utilisation']
        image                               = req['image']
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