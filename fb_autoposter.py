import facebook
#Some facebook token specific stuff

def init_token(token,page_id):   
    cfg = {
        "page_id"      : page_id,
        "access_token" : token
    }
    return cfg

def get_api(cfg):
    graph = facebook.GraphAPI(access_token = cfg['access_token'], version='2.12', timeout=15)
    print(graph)
    resp = graph.get_object("me/accounts")
    page_access_token = None
    for page in resp['data']:
        if page['id'] == cfg['page_id']:
      	    page_access_token = page['access_token']
    graph = facebook.GraphAPI(page_access_token)
    return graph

def post_msg(msg, api):

    api.put_object('me', 'feed', message=msg)
