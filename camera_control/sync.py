"""
Title: sync_v2.py
By: ET
Description: script handles downloading images from camera and updating pictures_list.txt
"""



class image_grabber:

    def __init__(string,gps_loc):
        self.grabber = threading.Thread(target=self.grab_pics)
        self.image_loc = string
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
        print 'got image at: '+self.gps_loc