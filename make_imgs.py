from PIL import Image, ImageDraw, ImageFont
import re
import os

# Resizing factor
scale = 2.0
# Fraction from bottom of screen to place image
imgfrac = 0.475
# Fraction of screen between bottom of image and caption
capfrac = 0.020
# Fraction of screen for caption width
widthfrac = 0.55
# Font and colour for caption
fontSize = 56
color = 'rgb(255,255,255)'


# load source image
blackImg = Image.open('blackS20.jpg')


# load captions into list
with open("captions.txt") as file_in:
    captions = []
    for caption in file_in:
        captions.append(caption)


imagesList = os.listdir("./img/")
for img in imagesList:
    print(img)
    index = int(re.findall(r"\d+",img)[0])

    # load each target and corresponding caption in loop
    targetImg = Image.open("./img/"+img)
    caption = captions[index]

    # Create copy of image to work with
    bgImg = blackImg.copy()

    # resize selected image
    xScale = round(scale*targetImg.size[0])
    yScale = round(scale*targetImg.size[1])
    targetImg = targetImg.resize((xScale, yScale), Image.ANTIALIAS)

    # Get essential dimensions
    x1Res, y1Res = blackImg.size
    x2Res, y2Res = targetImg.size

    # Paste resized image on background
    xPaste = round(x1Res/2 - x2Res/2)
    yPaste = round((1-imgfrac)*y1Res - y2Res/2)
    bgImg.paste(targetImg, (xPaste, yPaste))

    # split caption into substrings
    font = ImageFont.truetype('FiraSans-Book.otf', size=fontSize)
    maxWidth = x1Res*widthfrac
    lines = []
    if font.getsize(caption)[0] <= maxWidth:
        lines.append(caption)
    else:
        # split by spaces to get words
        words = caption.split(" ")
        i = 0
        # append each word to a line while width is shorter
        while i < len(words):
            line = ""
            while i < len(words) and font.getsize(line + words[i])[0] <= maxWidth:
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            lines.append(line)

    # draw centered caption on image
    draw = ImageDraw.Draw(bgImg)
    lineSpace = font.getsize(caption)[1]
    for i, line in enumerate(lines):
        wLine = font.getsize(line)[0]
        xCaption = round(x1Res/2 - wLine/2)
        yCaption = round((1-imgfrac)*y1Res + y2Res/2 + capfrac*y1Res + i*lineSpace)
        draw.text((xCaption,yCaption), line, fill=color, font=font)

    # save output
    bgImg.save("./out/"+img, quality=100)



