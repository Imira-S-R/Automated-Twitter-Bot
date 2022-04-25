from io import BytesIO
import requests
from PIL import Image, ImageDraw, ImageFont
import textwrap
import tweepy
import os

# Path to save image
PATH = ''

def post_to_twitter():
    # API keys that you saved earlier
    api_key = ""
    api_secrets = ""
    access_token = ""
    access_secret = ""
    
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(api_key,api_secrets)
    auth.set_access_token(access_token,access_secret)
    
    api = tweepy.API(auth)
    
    try:
        api.verify_credentials()
        print('Successful Authentication')
    except:
        print('Failed authentication')


    request = requests.get('https://api.quotable.io/random')
    data = request.json()

    req = requests.get("https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Regular.ttf?raw=true")

    def draw_multiple_line_text(image, text, font, text_color, text_start_height):
        draw = ImageDraw.Draw(image)
        image_width, image_height = image.size
        y_text = text_start_height
        lines = textwrap.wrap(text, width=30)
        for line in lines:
            line_width, line_height = font.getsize(line)
            draw.text(((image_width - line_width) / 2, y_text), 
                    line, font=font, fill=text_color)
            y_text += line_height


    image = Image.new('RGB', (800, 600), color = (0, 0, 0))
    fontsize = 40  # starting font size
    font = ImageFont.truetype(BytesIO(req.content), fontsize)
    text1 = f'''{data['content']}'''
    text2 = data['author']
    text_color = (200, 200, 200)
    text_start_height1 = 200
    text_start_height2 = 500
    draw_multiple_line_text(image, text1, font, text_color, text_start_height1)
    draw_multiple_line_text(image, text2, font, text_color, text_start_height2)
    image.save(PATH)

    # Send the tweet.
    file = open(PATH, 'rb')
    r2 = str(api.media_upload(filename=PATH, file=file))
    r3 = r2.split('media_id=')[1]
    media_id = r3.split(', ')[0]
    media_ids = []
    media_ids.append(media_id)
    api.update_status(media_ids=media_ids, status="")
    file.close()
    os.remove(PATH)
