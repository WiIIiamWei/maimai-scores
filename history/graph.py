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
    
def main():
    scoreb50 = "scoreb50.jpg"
    img = Image.open(scoreb50)
    cropped_img = img.crop((26, 21, 114, 51))
    cropped_img = cv2.normalize(np.array(cropped_img), None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    cropped_img = cv2.threshold(cropped_img, 100, 255, cv2.THRESH_BINARY)[1]
    cropped_img = cv2.GaussianBlur(cropped_img, (1, 1), 0)
    cropped_img = cv2.bitwise_not(cropped_img)
    cropped_img = cv2.copyMakeBorder(cropped_img, 100, 100, 100, 100, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    plt.imshow(cropped_img, cmap='gray')
    text = pytesseract.image_to_string(cropped_img).strip().replace('\n', '')
    time = datetime.now().strftime('%Y-%m-%d')
    with open('history/rating.csv', 'r') as csvfile:
        # Read the last line of the file and get the rating
        reader = csv.reader(csvfile)
        for row in reader:
            pass
        last_rating = row[1]
    print(f"Last rating: {last_rating}")
    print(f"Current rating: {text}")
    print(f"Diff: {int(text) - int(last_rating)}")
    with open('history/rating.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([time, last_rating])
        writer.writerow([time, text])

if __name__ == "__main__":
    main()
    draw_graph()