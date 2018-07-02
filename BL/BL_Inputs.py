from DC import DC_Inputs


def insertTweet(connection, name, created_at, usuario, text, source, location, tweet):
    resp = DC_Inputs.insertTweet(connection, name, created_at, usuario, text, source, location, tweet)
    if resp != 0:
        return resp
    else:
        return 0
