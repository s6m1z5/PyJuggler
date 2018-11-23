# coding: utf-8
# python 2.7
# juggler.py

import sys, os
import numpy as np
import matplotlib.pyplot as plt

class Juggler(object):
    def __init__(self, name="ダミー", setting=6, big=268., reg=268., grape=6., cherry=33., replay=7., pierrot=1092., bell=1092.):
        self.name = name #機種名
        self.setting = setting #設定(1-6)
        self.rotation = 0 #ハマり回転数
        self.rotation_total = 0
        self.medal = 0 #差枚数
        self.log = [] #当たり履歴
        self.slump = [] #スランプグラフ
        self.counter = np.zeros(7) #役カウンタ[BIG, REG, ブドウ, チェリー, リプレイ, ベル, ピエロ]

        self.big = big #BIG確率(分母)
        self.reg = reg #REG確率(分母)
        self.grape = grape #ブドウ確率(分母)
        self.cherry = cherry #チェリー確率(分母)
        self.replay = replay #リプレイ確率(分母)
        self.pierrot = pierrot #ピエロ確率(分母)
        self.bell = bell #ベル確率(分母)
        
        self.weight_big = np.array([1.0-1./self.big, 1./self.big])
        self.weight_reg = np.array([1.0-1./self.reg, 1./self.reg])
        self.weight_grape = np.array([1.0-1./self.grape, 1./self.grape])
        self.weight_cherry = np.array([1.0-1./self.cherry, 1./self.cherry])
        self.weight_replay = np.array([1.0-1./self.replay, 1./self.replay])
        self.weight_pierrot = np.array([1.0-1./self.pierrot, 1./self.pierrot])
        self.weight_bell = np.array([1.0-1./self.bell, 1./self.bell])

        self.flag_big = False #当たりフラグ
        self.flag_reg = False

    #スペック表示
    def show_spec(self):
        print(self.name)
        print("設定:%d"%self.setting)
        print("BIG確率:1/%g"%self.big)
        print("REG確率:1/%g"%self.reg)
        print("ボーナス合算:1/%g"%((self.reg*self.big)/(self.reg+self.big-1.)))
        print("ブドウ確率:1/%g"%self.grape)
        print("チェリー確率:1/%g"%self.cherry)

    #現在の回転数, 当たり回数などを表示
    def show_status(self):
        print("現在の回転数:%d, 差枚数:%d, 総回転数:%d, BIG:%d回, REG:%d回"%(self.rotation, self.medal, self.rotation_total, self.counter[0], self.counter[1]))
        n_big = float(self.rotation_total)/(self.counter[0]+1e-07)
        n_reg = float(self.rotation_total)/(self.counter[1]+1e-07)
        n_both = float(self.rotation_total)/(self.counter[0]+self.counter[1]+1e-07)
        print("BIG確率:1/%g, REG確率:1/%g, ボーナス合算:1/%g"%(n_big, n_reg, n_both))

    #小役カウンタを表示
    def show_counter(self):
        #print("ブドウ:%d, チェリー:%d, リプレイ:%d, ベル:%d, ピエロ:%d"%(self.counter[2], self.counter[3], self.counter[4], self.counter[5], self.counter[6]))
        n_koyaku = float(self.rotation_total)/(self.counter[2:]+1e-07)
        print("ブドウ確率:1/%g, チェリー確率:1/%g, リプレイ確率:1/%g, ベル確率:1/%g, ピエロ確率:1/%g"%(n_koyaku[0], n_koyaku[1], n_koyaku[2], n_koyaku[3], n_koyaku[4]))


    #スランプグラフを表示
    def show_graph(self, name="slump_graph", save=False):
        fig = plt.figure(name)
        ax = fig.add_subplot(111)
        ax.plot(self.slump, color="r", label="slump")
        ax.set_title("Slump Graph")
        ax.set_xlabel("# of draw")
        ax.set_ylabel("medals")
        ax.grid(color='gray')
        ax.legend()
        plt.show(fig)
        if save==True:
            fig.savefig(name+".png")
        plt.close(fig)

    #抽選
    def draw(self):
        #MAXBET
        self.medal -= 3
        self.rotation += 1
        self.rotation_total += 1
        #フラグが成立している場合は払い出し優先(生入りは考慮しない)
        #それ以外はBIG>REG>ベル>ピエロ>チェリー>リプレイ>ブドウの順に当たり判定を行う
        if ((self.flag_big==True) or (self.flag_reg==True)):
            self.rotation = 0
            if self.flag_big==True:
                result = "BIG"
                self.medal += 325
                self.flag_big = False
                self.counter[0] += 1
            if self.flag_reg==True:
                result = "REG"
                self.medal += 104
                self.flag_reg = False
                self.counter[1] += 1
        else:
            if np.random.choice([False, True], p=self.weight_big)==True:
                self.flag_big = True
            elif np.random.choice([False, True], p=self.weight_reg)==True:
                self.flag_reg = True

            if np.random.choice([False, True], p=self.weight_bell)==True:
                result = "ベル"
                self.medal += 14
                self.counter[6] += 1
            elif np.random.choice([False, True], p=self.weight_pierrot)==True:
                result = "ピエロ"
                self.medal += 10
                self.counter[5] += 1
            elif np.random.choice([False, True], p=self.weight_cherry)==True:
                result = "チェリー"
                self.medal += 2
                self.counter[3] += 1
            elif np.random.choice([False, True], p=self.weight_replay)==True:
                result = "リプレイ"
                self.medal += 3
                self.counter[4] += 1
            elif np.random.choice([False, True], p=self.weight_grape)==True:
                result = "ブドウ"
                self.medal += 7
                self.counter[2] += 1
            else:
                result = "ハズレ"

        if ((self.flag_big==True) or (self.flag_reg==True)):
            result = result + "(ペカッ)"
        self.log.append(result)
        self.slump.append(self.medal)
        
        return result

    


class ImJugglerEX(Juggler):

    def __init__(self, settei=1):

        self.big_prob = np.array([287.4, 282.5, 282.5, 273.1, 273.1, 268.6])#スペック表示しやすいように分母で入力
        self.reg_prob = np.array([455.1, 442.8, 348.6, 321.3, 268.6, 268.6])
        self.grape_prob = np.array([6.49, 6.49, 6.49, 6.49, 6.49, 6.18])
        self.cherry_prob = np.array([33.6, 33.6, 33.4, 33.2, 33.0, 33.0])
        self.big = self.big_prob[settei-1]
        self.reg = self.reg_prob[settei-1]
        self.grape = self.grape_prob[settei-1]
        self.cherry = self.cherry_prob[settei-1]
        self.replay = 7.3
        self.pierrot = 1092.3
        self.bell = 1092.3
        self.setting = settei
        super(ImJugglerEX, self).__init__("アイムジャグラーEXAE", self.setting, self.big, self.reg, self.grape, self.cherry, self.replay, self.pierrot, self.bell)


# 使用例
if __name__ == '__main__':
    
    myjag = ImJugglerEX(6)
    print("--------------------")
    myjag.show_spec()
    print("--------------------")

    """
    #普通に遊ぶ
    while(True):
        
        #print("現在の回転数:%d, 差枚数:%d, 総回転数:%d, BIG:%d回, REG:%d回"%(myjag.rotation, myjag.medal, myjag.rotation_total, myjag.counter[0], myjag.counter[1]))
        myjag.show_status()
        print("Enter:抽選, h+Enter:スペック表示, j+Enter:履歴表示, k+Enter:カウンタ表示, l+Enter:終了")
        finger = raw_input()
        
        if(finger=="h"):
            myjag.show_spec()
        elif(finger=="j"):
            print(myjag.log)
        elif(finger=="k"):
            myjag.show_counter()
        elif(finger=="l"):
            break
        else:
            result = myjag.draw()
            print(result)
        print("--------------------")

    print("おわり")
    """

    #シミュレーションする
    for i in range(10000):
        myjag.draw()
    myjag.show_status()
    myjag.show_counter()
    myjag.show_graph(name="slump_graph", save=True)
