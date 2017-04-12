#!/usr/bin/env python2

import kairos_face, json, time

face_gal_name = 'tes1'

"""
recognize faces from photo
return dictionary
"""
def recognize(facePhoto=None):
	try:
		#dict_responJSON = {}
		dict_responJSON = kairos_face.recognize_face(file=facePhoto, gallery_name=face_gal_name)
		
		"""
		loop over images object, find transaction with status=success
		"""
		dict_faces = {'cnt':0}
		#face_count = 0
		faces = dict_responJSON['images']
		for idx in faces:
			if idx['transaction']['status'] == 'success':
				#face_count++
				dict_faces['cnt'] = 1
				dict_faces['result'] = idx['transaction']
				#print(idx['transaction'])
				break
				
		dict_responJSON = dict_faces
	except Exception, err:		
		if err.__class__ == kairos_face.exceptions.ServiceRequestError:
			dict_responJSON = {'error': err.response_msg['Errors'][0]['Message']}
		else:
			dict_responJSON = {'error': str(err)}
			
	return dict_responJSON
	
"""
enroll faces from photo
return dictionary
"""
def enroll(facePhoto=None, subjectName=str(int(round(time.time() * 1000)))):
	try:
		#dict_responJSON = {}
		dict_responJSON = kairos_face.enroll_face(file=facePhoto, subject_id=subjectName, gallery_name=face_gal_name)
		
		"""
		loop over images object, find transaction with status=success
		"""
		if dict_responJSON['images'][0]['transaction']['status'] == 'success':
			dict_faces = {'cnt':1}
		else:
			dict_faces = {'cnt':0}
		
		#dict_responJSON = dict_faces
	except Exception, err:		
		if err.__class__ == kairos_face.exceptions.ServiceRequestError:
			dict_responJSON = {'error': err.response_msg['Errors'][0]['Message']}
		else:
			dict_responJSON = {'error': str(err)}
			
	return dict_responJSON	
	
"""
detect faces from photo
return dictionary
"""
def detect(facePhoto=None):
	try:
		dict_responJSON = kairos_face.detect_face(file=facePhoto)
	except Exception, err:
		dict_responJSON = None
	
	return dict_responJSON	
	
"""
clear faces gallery
return dictionary
"""
def clear_faces(galleryName=None):
	try:
		#dict_responJSON = {}
		dict_responJSON = kairos_face.remove_gallery(galleryName)
		print(dict_responJSON)
		
		"""
		status=Complete
		"""
		if dict_responJSON['status'] == 'Complete':
			dict_faces = {'cnt':1}
		else:
			dict_faces = {'cnt':0}
		
		dict_responJSON = dict_faces
	except Exception, err:		
		if err.__class__ == kairos_face.exceptions.ServiceRequestError:
			dict_responJSON = {'error': err.response_msg['Errors'][0]['Message']}
		else:
			dict_responJSON = {'error': str(err)}
			
	return dict_responJSON	

"""
get enrolled faces
return dictionary
"""
def get_enrolled_faces(galleryName=None):
	try:
		#dict_responJSON = {}
		dict_responJSON = kairos_face.get_gallery(galleryName)
		print(dict_responJSON)
		
		"""
		status=Complete
		"""
		if dict_responJSON['status'] == 'Complete':
			dict_faces = {'cnt':len(dict_responJSON['subject_ids']), 'subjects': dict_responJSON['subject_ids']}
		else:
			dict_faces = {'cnt':0}
		
		dict_responJSON = dict_faces
	except Exception, err:		
		if err.__class__ == kairos_face.exceptions.ServiceRequestError:
			dict_responJSON = {'error': err.response_msg['Errors'][0]['Message']}
		else:
			dict_responJSON = {'error': str(err)}
			
	return dict_responJSON	
	
def dump_respon_json(arespon):
	return json.dumps(arespon, indent=4, sort_keys=True)