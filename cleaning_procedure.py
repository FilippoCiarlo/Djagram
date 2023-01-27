import os
from social import settings

def cleaning(path):
	for file in os.listdir(path):
		if not file.startswith("test_image"):
			continue
		os.remove(os.path.join(path, file))

cleaning(str(settings.BASE_DIR) + "/media/images/")
cleaning(str(settings.BASE_DIR) + "/media/profile_images/")

