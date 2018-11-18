#Created by Shaun Spinelli 06/10/2018
import time
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw
from pathlib import Path
# from concurrent.futures import ThreadPoolExecutor


def draw_it(raw_strokes):
    image = Image.new("P", (255,255), color=255)
    image_draw = ImageDraw.Draw(image)

    for stroke in raw_strokes:
        for i in range(len(stroke[0])-1):

            image_draw.line([stroke[0][i],
                             stroke[1][i],
                             stroke[0][i+1],
                             stroke[1][i+1]],
                            fill=0, width=6)

    # image
    small_img = image.resize((31,31))
    # return small_img
    return image.convert('RGB') # maybe just return an image?


# def create_images(drawings, save_dir):
#     #need to create save dir
# 	save_dir.mkdir(parents=True, exist_ok=True)
#     # x = 0
#     for key, value in drawings.items():
#         while x > 200:
#             img = draw_it(value)
#             name = str(key)+".jpeg"
#             img.save(save_dir/name), "jpeg")
#             x = x + 1
# 		# df = pd.DataFrame(value)
# 		# df.to_csv(save_dir/str(key))
		# print(f'Saving Image {key}')


def create_images(drawings,save_dir):
    save_dir.mkdir(parents=True, exist_ok=True)
    for key, value in drawings.items():
            img = draw_it(value)
            name = str(key)+".jpeg"
            img.save(save_dir/name, "jpeg")


def get_drawings(df):
	""" retruns dict of drawing location and key id"""
	# print("Creating Dict")
	print("creating dict")
	col = ['key_id','drawing' ]
	df = df[col].head(n=1000)
	df = df.set_index('key_id').to_dict()
	return df["drawing"]


def process_csv(csv_path, name, save_dir):
    df = pd.read_csv(csv_path)
    drawings = get_drawings(df)

    create_images(drawings, save_dir)

def get_file_names(path):
   return [ i  for i in Path(path).iterdir()]

def process_files(files ,save_dir):
    #save_dir="images"
    for file in files:
    	start = time.time()
    	name = file.name[:-4]
    	print(f'processing {name}')
    	process_csv(file, name , Path(save_dir)/name)
    	end = time.time()
    	print(f'time took: {end-start}')


# def process_files(files, save_dir):
#     for file in files:
#         p = multiprocessing.Process(target=process_file, args=(file, save_dir))
#         p.start()



def main(path, save_dir):
    files = get_file_names(path)
    # with ThreadPoolExecutor(12) as e: e.map(process_files, iter(files))
    process_files(files, save_dir)

#     #need iterate through data dir and make list of classes
if __name__ == '__main__':

    main("/home/ubuntu/data/raw_data", "/home/ubuntu/data/images")






