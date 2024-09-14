import os
import json

# 创建一个空列表来存储歌曲信息
songs = []

# 如果文件已存在且不为空，读取已存在的数据
if os.path.exists("songs.json") and os.path.getsize("songs.json") > 0:
    with open("songs.json", "r", encoding='utf-8') as f:
        songs = json.load(f)

while True:
    # 获取歌曲信息
    song_name = input("Enter the song name: ")
    difficulty = int(input("Enter the difficulty: "))
    chart_type = int(input("Enter the chart type: "))
    achievement = float(input("Enter the achievement: "))

    # 创建一个字典来存储歌曲信息
    song = {
        "songName": song_name,
        "difficulty": difficulty,
        "chartType": chart_type,
        "achievement": achievement
    }

    # 将歌曲信息添加到列表中
    songs.append(song)

    # 将列表保存为JSON文件
    with open("songs.json", "w", encoding='utf-8') as f:
        json.dump(songs, f, indent=4, ensure_ascii=False)