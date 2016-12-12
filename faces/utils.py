import subprocess
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import base64
from PIL import Image, ImageDraw
import os
from faces.models import Document, Picture

RATINGS = ['LIKELY','VERY_LIKELY']

def likely_sentiment(face):
    #returns the sentiment felt in the face data
    if face['sorrowLikelihood'] in RATINGS:
        return 'SORROW'
    if face['surpriseLikelihood'] in RATINGS:
        return 'SURPRISE'
    if face['angerLikelihood'] in RATINGS:
        return 'ANGER'
    if face['joyLikelihood'] in RATINGS:
        return 'JOY'


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

    #doesn't crash when there are no faces
    if response['responses'] and 'faceAnnotations' in response['responses'][0]:
        return response['responses'][0]['faceAnnotations']
    else:
        return None

def highlight_faces(image,faces):
    im = Image.open(image)
    draw = ImageDraw.Draw(im)

    for face in faces:
        box = [(v.get('x',0.0), v.get('y',0.0))
               for v in face['fdBoundingPoly']['vertices']]
        draw.line(box + [box[0]], width=5, fill='#00ff00')
    image.seek(0)
    im.save(image)

def main(videodoc, max_results):
    #grabs directory videofile is in and runs every .png file through the vision api
    dirname = os.path.dirname(videodoc.docfile.url)

    for file in os.listdir('.'+dirname):
        if file.endswith(".png"):
            with open('.'+dirname+'/'+file, 'r+b') as image:
                newpic = Picture(video_loc=videodoc, picfile=(dirname+'/'+file)[6:])
                faces = detect_face(image, max_results)
                newpic.analyzed = True
                image.seek(0)
                if faces is not None:
                    newpic.numFaces=len(faces)
                    if newpic.numFaces==1:
                        newpic.face1=likely_sentiment(faces[0])
                    elif newpic.numFaces==2:
                        newpic.face1=likely_sentiment(faces[0])
                        newpic.face2=likely_sentiment(faces[1])
                    elif newpic.numFaces==3:
                        newpic.face1=likely_sentiment(faces[0])
                        newpic.face2=likely_sentiment(faces[1])
                        newpic.face3=likely_sentiment(faces[2])
                    elif newpic.numFaces==4:
                        newpic.face1=likely_sentiment(faces[0])
                        newpic.face2=likely_sentiment(faces[1])
                        newpic.face3=likely_sentiment(faces[2])
                        newpic.face4=likely_sentiment(faces[3])
                    highlight_faces(image, faces)
                    if newpic.face1=='JOY' or newpic.face2=='JOY' or newpic.face3=='JOY' or newpic.face4=='JOY':
                        videodoc.v_scoreHappy = videodoc.v_scoreHappy + 1
                    if newpic.face1=='SORROW' or newpic.face2=='SORROW' or newpic.face3=='SORROW' or newpic.face4=='SORROW':
                        videodoc.v_scoreSad = videodoc.v_scoreSad + 1
                    if newpic.face1=='SURPRISE' or newpic.face2=='SURPRISE' or newpic.face3=='SURPRISE' or newpic.face4=='SURPRISE':
                        videodoc.v_scoreSurprise = videodoc.v_scoreSurprise + 1
                    if newpic.face1=='ANGER' or newpic.face2=='ANGER' or newpic.face3=='ANGER' or newpic.face4=='ANGER':
                        videodoc.v_scoreAngry = videodoc.v_scoreAngry + 1
                newpic.save()
                videodoc.save()


def grab_frame(videofile):
    #grabs the video file and splits it into an image ~every 2-4 seconds
    filepath = os.path.dirname(videofile)
    outpath = filepath+'/out%03d.png'
    #subprocess.call('ffmpeg -i %s -vf "select=gte(n\,100)" -vframes 1 %s'% (videofile, outpath))
    subprocess.call('ffmpeg -i %s -vf fps=1/2 %s'% ('.'+videofile, '.'+outpath))

#not used
def get_totalframes(videofile):
    return subprocess.check_output('ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1 %s'% videofile)