from utils.mongoconnect import mongoConnect

cluster = mongoConnect()
db = cluster['discord']
conta = db['conta']
site = db['site']
