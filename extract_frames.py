#!/usr/bin/env python

import os, sys
import numpy as np
import cv2
import skvideo.io
import time

from os import listdir
from os.path import isfile, join, isdir


##############################################################################################################
def collect_files(dir_name, file_ext=".mp4", sort_files=True):
	allfiles = [os.path.join(dir_name,f) for f in listdir(dir_name) if isfile(join(dir_name,f))]

	these_files = []
	for i in range(0,len(allfiles)):
		_, ext = os.path.splitext(os.path.basename(allfiles[i]))
		if ext == file_ext:
			these_files.append(allfiles[i])

	if sort_files and len(these_files) > 0:
		these_files = sorted(these_files)

	return these_files


##############################################################################################################
def main(args=None, parser=None):

	data_dir = '/media/ye/Seagate Expansion Drive/moments_in_time/Moments_in_Time_256x256_30fps/validation'
	images_dir = '/media/ye/Seagate Expansion Drive/moments_in_time/images/validation'

	label_list = listdir(data_dir)
	print 'Total ', len(label_list), ' of files'

	for idx, f in enumerate(label_list):

		print '\nThis is the ', idx, '/', len(label_list), 'file, the label is : ', f

		folder = join(images_dir, f)

		if (isdir(folder) == False):
			os.mkdir(folder)

		file_dir = join(data_dir, f)
		video_files = collect_files(file_dir, file_ext='.mp4')
		nVideos = len(video_files)

		start_time = time.time()
		for i in range(0,nVideos):
			if i%50 == 0:
				print i, '/', nVideos

			vid_file = video_files[i]
			bn = os.path.basename(vid_file)
			# print "bn: ",bn 
			prefix = os.path.splitext(bn)[0]
			imgae_folder = join(folder, prefix)

			if (isdir(imgae_folder) == False):
				os.mkdir(imgae_folder)

				try:
					videodata = skvideo.io.vread(vid_file)
					for id, img in enumerate(videodata):
						position = join(join(folder, prefix),"image_{:03d}.jpg".format(id))
						cv2.imwrite(position, img)
				except:
					os.remove(imgae_folder)


	print '\nDONE\n'
	elapsed_time = time.time() - start_time
	print 'time: ', elapsed_time

	return 0


##############################################################################################################
if __name__ == '__main__':
	sys.exit(main())
