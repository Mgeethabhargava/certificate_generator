from PIL import Image, ImageDraw, ImageFont

def certificategenerate(fullname,registeredno,CourseName,courseyear,specialization,joiningyear,courseduration,emailid):
    # name = input("ENTER Candidate Name:")
    # companyname = input("ENTER Your Company Name:")
    # city = input("Enter Your Location(Especially City):")
    # fromdate = input("Enter From Date:")
    # todate = input("Enter till Date:")
    # lastdesignation = input("Enter the last Designation of candidate:")
    url = r'.\static\img\bonafied.jpg'
    joiningyear = int(joiningyear)
    courseduration = int(courseduration)
    endyear = joiningyear + courseduration
    # create Image object with the input image 
    # image = Image.open(r'G:\certificate-Generator projevct\001.jpg')
    image = Image.open(url)
    # initialise the drawing context with
    # the image object as background
    draw = ImageDraw.Draw(image)
    # create font object with the font file and specify
    # desired size
    font = ImageFont.truetype("arial.ttf", size=100)
    spacing = 20
    # starting position of the message
    #(x, y) = (200,200)
    #message = "This is to certify that "+fullname+" "+"with Register No."+registeredno+"\nis a student of"+" "+courseyear +" "+"in"+" "+CourseName+" "+"for the academic year "+str(joiningyear)+" "+"to"+" "+str(endyear)+".\nHe/She is bonafide student of our University."
    message = "This is to certify that "+fullname+" "+"with Register No."
    msg1 = "\n"+registeredno+" is a student of"+" "+courseyear +" "+"in"+" "+CourseName+" for the academic year "
    msg2 = "\n"+str(joiningyear)+" "+"to"+" "+str(endyear)+" He/She is bonafide student of our University."     
    tm = message+msg1+msg2
    color = 'rgb(0, 0, 0)' # black color
 
    # draw the message on the background
    draw.text((175,1240), tm, fill ="black", font = font,spacing = spacing)  
#****draw.text((x, y), message, fill=color, font=font)
# (x, y) = (200,200)
# name = '\n\n na vaala kadu '
# color = 'rgb(255, 255, 255)' # white color
# draw.text((x, y), name, fill=color, font=font)
 
# save the edited image
    fullname = registeredno + ".jpg"
    print(fullname)
    url = "G:/certificate-Generator projevct/downlodds/"+fullname
    image.save(url)
    #optimize = fullname+"_____"+"optimize.png"
    #image.save('optimized.png', optimize=True, quality=20)

