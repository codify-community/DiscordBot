from utils.mongoconnect import mongoConnect

cluster = mongoConnect()
db = cluster['discord']
site = db['site']

site.insert_one({'_id':1})