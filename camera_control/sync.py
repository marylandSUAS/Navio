"""
Title: sync_v2.py
By: ET
Description: script handles downloading images from camera and updating pictures_list.txt
"""



class image_grabber:

    def __init__(string,gps_loc,pic_type):
        self.grabber = threading.Thread(target=self.grab_pics)
        self.image_loc = string

        self.typ = pic_type
        self.gps_loc = gps_loc

        self.pic_loc_addr = '/home/pi/Pictures/'
        self.grabber.start()



    #grabs pics from the camera
    def grab_pics(self):
        #print ('GRABBER!')
        line = self.image_loc.split(",")
        pic_loc = line[0]
        pic_id = pic_loc.split("/")
        pic_id = pic_id[3]
        print(pic_id)

        # Download Image
        cmd = 'curl -s ' + '\"http://10.98.32.1:80' + pic_loc + '\" > ' + self.pic_loc_addr + pic_id
        # print(cmd)
        proc1 = Popen(cmd, shell=True, stdout=PIPE)
        proc1.communicate()
        proc1.wait()

        with open('/home/pi/imaging/camera_control/Logs/imageLog.txt','a+') as locFile:
            locFile.write(str(time.time())+' '+pic_id+' '+self.gps_loc)

        with open('/home/pi/imaging/camera_control/Pictures/image_locs.txt','a+') as locFile:
            gps_loc = locFile.write(pic_id+','+self.gps_loc+','+self.typ)

        print 'got image at: '+self.gps_loc