import matplotlib.pyplot as plt
import csv
import numpy as np
from datetime import datetime
import pytesseract
from PIL import Image
import cv2

def draw_graph():
    dates = []
    ratings = []

    with open('history/rating.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dates.append(datetime.strptime(row['date'], '%Y-%m-%d'))
            ratings.append(int(row['rating']))

    plt.figure(figsize=(10, 5))
    plt.plot(dates, ratings)
    plt.xlabel('Date')
    plt.ylabel('Rating')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('history/rating.jpg')
    
def draw_real_graph():
    dates = []
    ratings = []

    with open('history/realrating.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dates.append(datetime.strptime(row['date'], '%Y-%m-%d'))
            ratings.append(int(row['rating']))

    plt.figure(figsize=(10, 5))
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=['orange'])
    plt.plot(dates, ratings)
    plt.xlabel('Date')
    plt.ylabel('Rating')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('history/realrating.jpg')
    
def main():
    scoreb50 = "scoreb50.jpg"
    realb50 = "realb50.jpg"
    img = Image.open(scoreb50)
    img_real = Image.open(realb50)
    cropped_img = img.crop((26, 21, 114, 51))
    cropped_img = cv2.normalize(np.array(cropped_img), None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    cropped_img = cv2.threshold(cropped_img, 100, 255, cv2.THRESH_BINARY)[1]
    cropped_img = cv2.GaussianBlur(cropped_img, (1, 1), 0)
    cropped_img = cv2.bitwise_not(cropped_img)
    cropped_img = cv2.copyMakeBorder(cropped_img, 100, 100, 100, 100, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    cropped_img_real = img_real.crop((245, 59, 314, 78))
    cropped_img_real = cv2.normalize(np.array(cropped_img_real), None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    cropped_img_real = cv2.threshold(cropped_img_real, 100, 255, cv2.THRESH_BINARY)[1]
    cropped_img_real = cv2.GaussianBlur(cropped_img_real, (1, 1), 0)
    hsv_img_real = cv2.cvtColor(np.array(cropped_img_real), cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv_img_real, (20, 100, 100), (30, 255, 255))
    mask_inv = cv2.bitwise_not(mask)
    cropped_img_real[mask == 255] = [0, 0, 0]
    cropped_img_real[mask_inv == 255] = [255, 255, 255]
    cropped_img_real = cv2.copyMakeBorder(cropped_img_real, 100, 100, 100, 100, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    current_rating = pytesseract.image_to_string(cropped_img).strip().replace('\n', '')
    current_real_rating = pytesseract.image_to_string(cropped_img_real).strip().replace('\n', '')
    time = datetime.now().strftime('%Y-%m-%d')
    with open('history/rating.csv', 'r') as csvfile:
        # Read the last line of the file and get the rating
        reader = csv.reader(csvfile)
        for row in reader:
            pass
        last_rating = row[1]
    with open('history/realrating.csv', 'r') as realcsvfile:
        # Read the last line of the file and get the real rating
        reader = csv.reader(realcsvfile)
        for row in reader:
            pass
        last_real_rating = row[1]
    print(f"Last rating: {last_rating}")
    print(f"Current rating: {current_rating}")
    diff = int(current_rating) - int(last_rating)
    print(f"Diff: {diff}")
    print(f"Real rating: {last_real_rating}")
    print(f"Current real rating: {current_real_rating}")
    real_diff = int(current_real_rating) - int(last_real_rating)
    print(f"Diff: {real_diff}")
    if diff > 0:
        with open('history/rating.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([time, last_rating])
            writer.writerow([time, current_rating])
        draw_graph()
    else:
        print("No change in rating")
    if real_diff > 0:
        with open('history/realrating.csv', 'a', newline='') as realcsvfile:
            writer = csv.writer(realcsvfile)
            writer.writerow([time, last_real_rating])
            writer.writerow([time, current_real_rating])
        draw_real_graph()
    else:
        print("No change in real rating")

if __name__ == "__main__":
    main()
