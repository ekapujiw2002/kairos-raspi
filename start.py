#!/usr/bin/env python2

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.process
import tornado.template
import tornado.log
import gen
import os
import sys
import video
import configuration
import kairos_face
import face_api

# default configuration
config_file = sys.argv[1]
web_server_port = int(configuration.ini(cfg_file=config_file).get_data("web-server","port"))
web_doc_root = configuration.ini(cfg_file=config_file).get_data("web-server","doc")
kairos_id = configuration.ini(cfg_file=config_file).get_data("kairos","id")
kairos_key = configuration.ini(cfg_file=config_file).get_data("kairos","key")
kairos_request_timeout = int(configuration.ini(cfg_file=config_file).get_data("kairos","timeout"))

cam = None
#html_page_path = dir_path = os.path.dirname(os.path.realpath(__file__)) + '/www/'
html_page_path = dir_path = web_doc_root


class HtmlPageHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, file_name='index.html'):
        # Check if page exists
        index_page = os.path.join(html_page_path, file_name)
        if os.path.exists(index_page):
            # Render it
            #self.render('www/' + file_name)
            self.render(html_page_path + file_name)
        else:
            # Page not found, generate template
            err_tmpl = tornado.template.Template("<html> Err 404, Page {{ name }} not found</html>")
            err_html = err_tmpl.generate(name=file_name)
            # Send response
            self.finish(err_html)


class SetParamsHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        # print self.request.body
        # get args from POST request
        width = int(self.get_argument('width'))
        height = int(self.get_argument('height'))
        # try to change resolution
        try:
            cam.set_resolution(width, height)
            self.write({'resp': 'ok'})
        except:
            self.write({'resp': 'bad'})
            self.flush()
            self.finish()


class StreamHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        """
        functionality: generates GET response with mjpeg stream
        input: None
        :return: yields mjpeg stream with http header
        """
        # Set http header fields
        self.set_header('Cache-Control',
                         'no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0')
        self.set_header('Connection', 'close')
        self.set_header('Content-Type', 'multipart/x-mixed-replace;boundary=--boundarydonotcross')

        while True:
            # Generating images for mjpeg stream and wraps them into http resp
            if self.get_argument('fd') == "true":
                img = cam.get_frame(True)
            else:
                img = cam.get_frame(False)
            self.write("--boundarydonotcross\n")
            self.write("Content-type: image/jpeg\r\n")
            self.write("Content-length: %s\r\n\r\n" % len(img))
            self.write(str(img))
            yield tornado.gen.Task(self.flush)

class FaceAPIHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        # print self.request.body
        # get args from GET request
        cmdx = int(self.get_argument('c'))
        namex = self.get_argument('n')
        # try to run command
        
        try:
            if cmdx == 1:
                tornado.log.app_log.info('Recognizing...')
                
                # save last frame
                cam.save_last_camera_frame()
                
                # recognize
                dictRespon = face_api.recognize('/dev/shm/kairos.jpg')
                dictRespon['cmd'] = 1
                
                #log
                tornado.log.app_log.info(face_api.dump_respon_json(dictRespon))
                
                #get response
                self.write(face_api.dump_respon_json(dictRespon))
                    
            elif cmdx == 2:
                tornado.log.app_log.info('Enrolling...')
                
                # save last frame
                cam.save_last_camera_frame()
                
                # recognize
                dictRespon = face_api.enroll('/dev/shm/kairos.jpg',subjectName=namex)
                dictRespon['cmd'] = 2

                #log
                tornado.log.app_log.info(face_api.dump_respon_json(dictRespon))
                
                #get response
                self.write(face_api.dump_respon_json(dictRespon))
                
            elif cmdx == 3:
                tornado.log.app_log.info('Clearing faces...')
                
                # clear
                dictRespon = face_api.clear_faces(namex)
                dictRespon['cmd'] = 3

                #log
                tornado.log.app_log.info(face_api.dump_respon_json(dictRespon))
                
                #get response
                self.write(face_api.dump_respon_json(dictRespon))
                
            elif cmdx == 4:
                tornado.log.app_log.info('Get enrolled faces...')
                
                # clear
                dictRespon = face_api.get_enrolled_faces(namex)
                dictRespon['cmd'] = 4

                #log
                tornado.log.app_log.info(face_api.dump_respon_json(dictRespon))
                
                #get response
                self.write(face_api.dump_respon_json(dictRespon))
                
            else:
                tornado.log.app_log.info('Unknown command...')
                self.write({'error': 'Unknown command'})
                
        except Exception, err:
            self.write({'error': 'Unknown error'})
            print(err)
            
        self.flush()
        self.finish()
            
def make_app():
    # add handlers
    return tornado.web.Application([
        (r'/', HtmlPageHandler),
        (r'/video_feed', StreamHandler),
        (r'/setparams', SetParamsHandler),
        (r'/face', FaceAPIHandler),
        (r'/(?P<file_name>[^\/]+htm[l]?)+', HtmlPageHandler),
        (r'/(?:image)/(.*)', tornado.web.StaticFileHandler, {'path': html_page_path + 'image'}),
        (r'/(?:css)/(.*)', tornado.web.StaticFileHandler, {'path': html_page_path + 'css'}),
        (r'/(?:js)/(.*)', tornado.web.StaticFileHandler, {'path': html_page_path + 'js'}),
        (r'/(?:fonts)/(.*)', tornado.web.StaticFileHandler, {'path': html_page_path + 'fonts'})
        ],
    )


if __name__ == "__main__":
    try:
        # register kairos app
        kairos_face.settings.app_id = kairos_id
        kairos_face.settings.app_key = kairos_key
        kairos_face.settings.request_timeout = kairos_request_timeout
        
        # creates camera
        cam = video.UsbCamera()
        
        # get first frame
        cam.get_frame(False)
        
        # bind server on 8080 port
        tornado.log.enable_pretty_logging()
        tornado.log.app_log.info('KAIROS FACEX on port %d with timeout %ds and root at %s' % (web_server_port, kairos_face.settings.request_timeout, dir_path))    
        
        sockets = tornado.netutil.bind_sockets(web_server_port)
        server = tornado.httpserver.HTTPServer(make_app())
        server.add_sockets(sockets)
        tornado.ioloop.IOLoop.current().start()
    except:
        tornado.log.app_log.error('Bye...')
        pass
