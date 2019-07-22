from tornado.httpserver import  HTTPServer
from tornado.wsgi import WSGIContainer
from app import app
from tornado.ioloop import IOLoop
from global_vars import dictionary
from build_dict import Dict
import pickle
if __name__ == '__main__':
    with open('E:\\COCO\\dict\\dict.pkl', 'rb') as f:
        dictionary['value'] = pickle.load(f)
    s = HTTPServer(WSGIContainer(app))
    s.listen(5000, address='127.0.0.1')
    print("server listening")
    IOLoop.current().start()