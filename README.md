# PyJuggler
コマンドライン上でジャグラーを遊びたい

## つかいかた
`python main.py`

## 動作環境
Python 2.7.13  
Numpy 1.12.1  
Matplotlib 2.0.2

## 問題点(気が向いたら修正)
- juggler.show_graph()
    - なんかもうちょい情報を足した画像にしたい
- juggler.show_counter()
    - ゼロ除算対策で1e-07を入れてるけど表示するときに美しくないからなんか変えたい
- juggler.draw()
    - 各小役の挙動をメソッド化して,サイコロの出目に応じてそれを呼び出す形にしたい