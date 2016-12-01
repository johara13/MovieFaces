import subprocess
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import base64
from PIL import Image, ImageDraw
import os




def get_vision_service():
    credentials = GoogleCredentials.get_application_default()
    return discovery.build('vision', 'v1', credentials=credentials)

def detect_face(face_file, max_results=4):
    image_content = face_file.read()
    batch_request = [{
        'image': {
            'content': base64.b64encode(image_content).decode('utf-8')
        },
        'features': [{
            'type': 'FACE_DETECTION',
            'maxResults': max_results,
        }]
    }]
    service = get_vision_service()
    request = service.images().annotate(body={
        'requests': batch_request,
    })
    response = request.execute()

    return response['responses'][0]['faceAnnotations']

def highlight_faces(image,faces):
    im = Image.open(image)
    draw = ImageDraw.Draw(im)

    for face in faces:
        box = [(v.get('x',0.0), v.get('y',0.0))
               for v in face['fdBoundingPoly']['vertices']]
        draw.line(box + [box[0]], width=5, fill='#00ff00')
    image.seek(0)
    im.save(image)

def main(input_filename, max_results):
    with open('.'+input_filename, 'r+b') as image:
        faces = detect_face(image, max_results)
        image.seek(0)
        highlight_faces(image, faces)

def grab_frame(videofile):
    filepath = os.path.dirname(videofile)
    outpath = filepath+'/out%03d.png'
    #subprocess.call('ffmpeg -i %s -vf "select=gte(n\,100)" -vframes 1 %s'% (videofile, outpath))
    subprocess.call('ffmpeg -i %s -vf fps=1/2 %s'% (videofile, outpath))

def get_totalframes(videofile):
    return subprocess.check_output('ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1 %s'% videofile)