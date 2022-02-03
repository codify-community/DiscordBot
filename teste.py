def get_update(user, db_user):
    user = list(user.items())
    db_user = list(db_user.items())

    update = {}

    for i in range(0,len(user)):
        if(user[i][1]!=db_user[i][1]):
            update[user[i][0]] = user[i][1]

    return update


user = {
    "name": "Sla",
    "id": 13245645614,
    "pfp": "https://googdssdajsdakjle.com.br"
}

db_user = {
    "name": "Nome",
    "id": 123,
    "pfp": "https://google.com.br",
}

db_user_complete = {
    "name": "Nome",
    "id": 123,
    "pfp": "https://google.com.br",
    "habilidades": [],
    "outroPropQualquer": 123
}

update = get_update(user, db_user)

db_user_complete.update(update)
print(db_user_complete)