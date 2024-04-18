import tkinter as tk
from tkinter import filedialog
import requests
from bs4 import BeautifulSoup
import re
import sqlite3


# SQLite3データベースに接続
conn = sqlite3.connect('text_data.db')

# カーソルを取得
cursor = conn.cursor()

# テーブルを作成
cursor.execute('''CREATE TABLE IF NOT EXISTS text_data (
                    id INTEGER PRIMARY KEY,
                    text_content TEXT
                    )''')

# 変更をコミット
conn.commit()


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            file_contents = file.read()
            text.config(state=tk.NORMAL)  # テキストウィジェットを編集可能にする
            text.delete("1.0", tk.END)  # テキストウィジェットをクリア
            text.insert(tk.END, file_contents)  # ファイル内容を表示
            text.config(state=tk.DISABLED)  # テキストウィジェットを読み取り専用に戻す

def search_word():
    start_index = text.index(tk.SEL_FIRST)
    end_index = text.index(tk.SEL_LAST)
    selected_text = text.get(start_index, end_index)
    if selected_text:
        search_results = google_search(selected_text)
        show_search_results(search_results)

def save_meaning():
    # 単語と意味をテキストファイルの下部に保存するコードを追加
    start_index = result_text.index(tk.SEL_FIRST)
    end_index = result_text.index(tk.SEL_LAST)
    selected_text = result_text.get(start_index, end_index)
    if selected_text:
        current_text = edited_text.get("1.0", "end-14c")  # 現在のテキストを取得
        new_text = current_text.rstrip()  # 末尾の空白（改行含む）を削除
        new_text += f"\n\n{selected_text}\n\n</hamu_zer0>"  # 新しい文章を追加
        edited_text.delete("1.0", tk.END)  # テキストをクリア
        edited_text.insert(tk.END, new_text)  # 新しいテキストを挿入

        

def remove_html_tags(text):
    # BeautifulSoupを使用してHTMLタグを解析
    soup = BeautifulSoup(text, 'html.parser')
    # <span>タグで囲まれた部分を削除する
    #span_tags = soup.find_all('span')
    # class="kana" がついている<span>タグをすべて取得
    kana_spans = soup.find_all('span', class_='kana')
    for span in kana_spans:
        span.decompose()
    # テキスト部分のみを取得
    clean_text = soup.get_text()
    # 2回以上の改行を1回の改行に置換し、それ以外の改行を削除
    clean_text = re.sub(r'\n{2,}', '\n\n', clean_text)

    return clean_text

def google_search(query):
    search_url = f"https://eow.alc.co.jp/search?q={query}"
    print("requestする")
    response = requests.get(search_url)
    print("requestした")
    if response.status_code == 200:
        web_content = response.text
        # BeautifulSoupでHTMLを解析
        soup = BeautifulSoup(web_content, 'html.parser')
        # idがresultsAreaのdiv要素を抽出
        results_area = soup.find('div', {'id': 'resultsArea'})
        
        if results_area:
            # results_area内のHTMLコンテンツを文字列として返す
            cleaned_text = remove_html_tags(str(results_area))
            return cleaned_text
        else:
            return "検索結果が見つかりませんでした。"
    else:
        return "ウェブページを取得できませんでした。"

def show_search_results(results):
    result_text.config(state=tk.NORMAL)  # テキストウィジェットを編集可能にする
    result_text.delete("1.0", tk.END)  # テキストウィジェットをクリア
    result_text.insert(tk.END,results)  # ウェブページのコンテンツを表示
    result_text.config(state=tk.DISABLED)  # テキストウィジェットを読み取り専用に戻す


def save_to_database():
    start_index = result_text.index(tk.SEL_FIRST)
    end_index = result_text.index(tk.SEL_LAST)
    selected_text = result_text.get(start_index, end_index)
    if selected_text:
        # SQLite3データベースに接続
        conn = sqlite3.connect('text_data.db')
        cursor = conn.cursor()

        # データベースにテキストを挿入
        cursor.execute("INSERT INTO text_data (text_content) VALUES (?)", (selected_text,))
        
        # 変更をコミット
        conn.commit()
        
        # データベース接続を閉じる
        conn.close()

# delete_entry をプログラムの上部で宣言
delete_entry = None
database_window= None

def delete_selected_content():
    global delete_entry  # delete_entry をグローバル変数として宣言
    # 入力されたIDを取得
    selected_id = int(delete_entry.get())

    # データベースから選択された内容を削除
    conn = sqlite3.connect('text_data.db')
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM text_data WHERE id=?", (selected_id,))
    conn.commit()
    conn.close()
    
    global database_window
    # ウィンドウを閉じる
    database_window.destroy()
    # ウィンドウを更新して削除後のデータを表示
    show_database_contents()


def show_database_contents():
    global database_window
    # 新しいウィンドウを作成
    database_window = tk.Toplevel(root)
    database_window.title("データベースの中身")

    # データベースからテキストデータを取得
    conn = sqlite3.connect('text_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM text_data")
    database_contents = cursor.fetchall()
    conn.close()

    # テキストウィジェットを作成してデータベースの中身を表示
    database_text = tk.Text(database_window, wrap=tk.WORD, width=100, height=20)
    database_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    for row in database_contents:
        database_text.insert(tk.END, f"{row[0]}: {row[1]}\n")
    database_text.config(state=tk.DISABLED)  # テキストウィジェットを読み取り専用に設定


    global delete_entry  # delete_entry をグローバル変数として宣言
    # テキストボックスを作成してIDを入力する
    delete_entry = tk.Entry(database_window)
    delete_entry.pack()
    # ボタンを作成して選択された内容を削除する関数を関連付ける
    delete_button = tk.Button(database_window, text="選択された内容を削除", command=delete_selected_content)
    delete_button.pack()


root = tk.Tk()
root.title("テキストファイルビューア")

# ボタン: ファイルを開く
open_button = tk.Button(root, text="ファイルを選択して開く", command=open_file)
open_button.pack()

# テキストウィジェット: ファイル内容を表示
text = tk.Text(root, wrap=tk.WORD, width=100, height=20)
text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
text.config(state=tk.DISABLED)  # テキストウィジェットを最初は読み取り専用に設定

# フレームを作成してボタンとテキストウィジェットを配置
frame = tk.Frame(root)
frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# フレームを作成してボタンを配置
button_frame = tk.Frame(frame)
button_frame.pack(side=tk.TOP, fill=tk.X, pady=5)  # 上部に配置

# ボタン: 検索
search_button = tk.Button(button_frame, text="選択したテキストを検索", command=search_word)
search_button.pack(side=tk.LEFT, padx=5)

# ボタン: 意味を保存
save_button = tk.Button(button_frame, text="意味を保存", command=save_meaning)
save_button.pack(side=tk.LEFT, padx=5)

# ボタン: データベースに保存
save_database_button = tk.Button(button_frame, text="データベースに保存", command=save_to_database)
save_database_button.pack(side=tk.LEFT, padx=5)

# ボタン: データベースの中身を表示
show_database_button = tk.Button(button_frame, text="データベースの中身を表示", command=show_database_contents)
show_database_button.pack(side=tk.LEFT, padx=5)

# テキストウィジェット: 検索結果を表示
result_text = tk.Text(frame, wrap=tk.WORD, width=50, height=1)
result_text.pack(fill=tk.BOTH, expand=True)
result_text.config(state=tk.DISABLED)  # テキストウィジェットを読み取り専用に設定


# テキストウィジェット: 新しいテキストを編集
edited_text = tk.Text(frame, wrap=tk.WORD, width=50, height=1)
edited_text.pack( fill=tk.BOTH, expand=True)
edited_text.insert(tk.END, "<hamu_zer0>\n\n</hamu_zer0>")




root.mainloop()

# データベース接続を閉じる
conn.close()

