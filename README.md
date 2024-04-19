# EngWordResearch_py
テキストファイルを読み込み、カーソルで範囲指定した単語を検索する。検索結果の保存したい範囲を取り出したり、メモを残したりできる。テキストファイル名、検索した単語、意味、メモの４つの項目をデータベースに保存できる。データベースにはsqliteを使用している。

# 使用方法
![1](https://github.com/hamu-zer0/EngWordResearch_py/assets/88695666/c6702752-e196-411c-8194-74f2f7ffde4d)
起動すると上画像のような画面になる。
![2](https://github.com/hamu-zer0/EngWordResearch_py/assets/88695666/89641430-d2f0-4d34-ac03-3bd4c0a14acd)
"ファイルを選択して開く"を押すとテキストファイルを選択でき、選択したファイルの中身が表示される。
![3](https://github.com/hamu-zer0/EngWordResearch_py/assets/88695666/62a2d87f-337a-45ae-bf35-2355cfd20516)
左のエリアから検索した単語をカーソルで範囲指定し、"選択したテキストを検索"ボタンを押すと、上画像のように右上のエリアに検索結果が表示される。
![5](https://github.com/hamu-zer0/EngWordResearch_py/assets/88695666/ba2c0e23-99d2-4a34-b455-f3834f741397)
同様に、検索結果のエリアの保存したい範囲を範囲指定し、"意味を保存"ボタンを押すと右下エリアの'meaning'で挟まれた範囲に保存される。この'meaning'で挟まれた範囲がデータベースの意味の項目として保存される。'memo'はメモの項目として保存される。
![6](https://github.com/hamu-zer0/EngWordResearch_py/assets/88695666/9318f1a2-8250-4559-bd1d-89c92270ca6a)
上画像のように、'meaning'と'memo'には直接入力することができる。
![7](https://github.com/hamu-zer0/EngWordResearch_py/assets/88695666/11f25022-f941-4f0c-b5c9-a2f757eefb5f)
"データベースの中身を表示"ボタンを押すと、新しいウィンドウが開き、データベースに保存した内容が確認できる。保存された単語にはidがつけられており(上の画像では1)、そのidを右の入力欄に記入して"選択された内容を削除"ボタンを押すことで削除できる。
![8](https://github.com/hamu-zer0/EngWordResearch_py/assets/88695666/4fd312c6-ddce-4731-b4f0-d46b27087aa3)
また、次の単語を左のエリアから範囲指定して、検索すると'meaning'と'memo'のエリアが初期化されるようになっている。