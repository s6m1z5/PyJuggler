# coding: utf-8
# python 2.7
# main.py

import numpy as np # __version__ = 1.12.1
import sys, os

import juggler


def main():
    # 遊ぶ機種を選択
    dic_models = {"ImEXAE":"アイムジャグラーEXAE"}
    print("PyJuggler by s6m1z5")
    print("--------------------")
    print("[機種選択]")
    for key, value in dic_models.iteritems():
        print "%s\t:%s" %(key, value)

    while(True):
        key_in = raw_input("選択してください:")
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
    print("--------------------")
    model = juggler.ImJugglerEX(settei)
    print("設定:%g"%model.setting)
    print("BIG確率:%g"%model.big)
    print("REG確率:%g"%model.reg)
    print("ここから先はできてないので終了")

if __name__ == '__main__':
    main()