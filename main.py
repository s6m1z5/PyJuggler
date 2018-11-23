# coding: utf-8
# python 2.7
# main.py

import numpy as np # __version__ = 1.12.1
import sys, os

import juggler


def main():
    
    print("PyJuggler by s6m1z5")
    print("--------------------")

    dic_models = {"ImEXAE":"アイムジャグラーEXAE"}
    print("[機種選択]")
    for key, value in dic_models.iteritems():
        print "%s\t:%s" %(key, value)

    while(True):
        key_in = raw_input("選択してください[例:ImEXAE]:")
        if key_in not in dic_models.keys():
            print("Error! 正しい名前を選んでください")
        else:
            print(dic_models[key_in]+"で遊びます")
            break
    
    print("--------------------")
    print("[設定選択]")
    print("1~6の中から設定を選んでください")
    while(True):
        settei = int(raw_input("設定:"))
        if settei not in range(1,6+1):
            print("Error! 正しい設定を選んでください")
        else:
            print("設定%dで遊びます"%settei)
            break
    model = juggler.ImJugglerEX(settei)

    print("--------------------")
    print("[スペック]")
    model.show_spec()
    print("--------------------")

    while(True):
        
        model.show_status()
        print("Enter:抽選, h+Enter:スペック表示, j+Enter:グラフ表示, k+Enter:小役カウンタ表示, l+Enter:終了")
        finger = raw_input()
        
        if(finger=="h"):
            model.show_spec()
        elif(finger=="j"):
            model.show_graph()
        elif(finger=="k"):
            model.show_counter()
        elif(finger=="l"):
            break
        else:
            result = model.draw()
            print(result)
        print("--------------------")


    print("おわり")


if __name__ == '__main__':
    main()