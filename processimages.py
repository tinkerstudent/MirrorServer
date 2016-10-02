from twisted.internet import defer, reactor
import utils as u
import cv2

# processes image parts

class ImagePart:
	_image_parts = {}
	@staticmethod
	def process_images(label):
		file_name = ImagePart.join_image_file_parts(label)
		if file_name:
			video_capture = cv2.VideoCapture(file_name)
			if video_capture.isOpened():
				print 'video capture is open'
				video_capture.release()
	@staticmethod
	def join_image_file_parts(label):
		image_parts = ImagePart._image_parts[label]
		sorted(image_parts, key=lambda image_part: image_part._counter)
		if len(image_parts) > 0:
			image_part = image_parts[0]
			file_name = image_part._base_file_name
			file_ = open(file_name, 'wb')
			for image_part in image_parts:
				part_file_name = image_part._file_name
				part_file = open(part_file_name, 'rb')
				part_data = part_file.read(u.MB_64)
				while part_data:
					file_.write(part_data)
					part_data = part_file.read(u.MB_64)
		return file_name
	@staticmethod
	def update_and_process_images(image_part):
		label = image_part._label
		total = image_part._total
		image_parts = ImagePart._image_parts
		image_parts.setdefault(label, [])
		image_parts[label].append(image_part)
		if len(image_parts[label]) == total:
			reactor.callInThread(ImagePart.process_images, label)
	def add_image_part(self, label, counter, total, bytes, callback):
		self._deferred = defer.Deferred()
		self._label = label
		self._counter = counter
		self._total = total
		self._bytes = bytes
		self._callback = callback
		reactor.callInThread(self.process_image_part)
		return self._deferred
	def process_image_part(self):
		base_file_name = self._label + ".mp4"
		self._base_file_name = base_file_name
		file_name = base_file_name + ".part." + str(self._counter) 
		self._file_name = file_name
		file_ = open(file_name, 'wb')
		file_.write(self._bytes)
		file_.close()
		deferred, self._deferred  = self._deferred, None
		self._callback(deferred)
		ImagePart.update_and_process_images(self)


