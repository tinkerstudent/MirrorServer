from klein import run, route
from twisted.internet import reactor
import processimages as pi
import utils as u

def handle_train_response(deferred):
	deferred.callback("OK")

@route('/status')
def status(request):
	return "OK"

@route('/train')
def train(request):
	label = request.getHeader('XX-Mirror-Label')
	label = label and label.lower()
	label = label and label.replace(' ', '')
	counter = int(request.getHeader('XX-Mirror-Counter'))
	total = int(request.getHeader('XX-Mirror-Total'))
	bytes = request.content.read()
	image_part = pi.ImagePart()
	deferred = image_part.add_image_part(label, counter, total, bytes, handle_train_response)
	return deferred

ip = u.get_ip()
print ip

run(ip, 8080)

#### 

