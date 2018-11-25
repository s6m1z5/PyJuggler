# coding: utf-8
# python 2.7
# juggler.py

import sys, os
import numpy as np
import matplotlib.pyplot as plt

class Juggler(object):
    def __init__(self, name="ダミー", setting=6, big_single=172, big_cherry=72, reg_single=172, reg_cherry=72, grape=10600, cherry_single=1840, replay=8978, bell=60, pierrot=60):

        self.name = name            #機種名
        self.setting = setting      #設定(1-6)
        self.rotation = 0           #ハマり回転数
        self.rotation_total = 0     #総回転数
        self.medal = 0              #差枚数
        self.log = []               #当たり履歴
        self.slump = []             #スランプグラフ
        self.counter = np.zeros(7)  #役カウンタ[BIG, REG, ブドウ, チェリー, リプレイ, ベル, ピエロ]
        self.flag_big = False #BIGフラグ
        self.flag_reg = False #REGフラグ

        self.big_single = big_single        #単独BIG確率(x/65536)
        self.big_cherry = big_cherry        #チェリーBIG確率
        self.reg_single = reg_single        #単独REG確率
        self.reg_cherry = reg_cherry        #チェリーREG確率
        self.grape = grape                  #ブドウ確率
        self.cherry_single = cherry_single  #チェリーのみ確率
        self.replay = replay                #リプレイ確率
        self.pierrot = pierrot              #ピエロ確率
        self.bell = bell                    #ベル確率

        self.big_total = big_single+big_cherry                  #BIG確率
        self.reg_total = reg_single+reg_cherry                  #REG確率
        self.bonus_total = self.big_total+self.reg_total        #ボーナス合算
        self.cherry_total = big_cherry+reg_cherry+cherry_single #チェリー合算

        # 抽選テーブルを作成
        self.th_big_single = big_single
        self.th_big_cherry = self.th_big_single + big_cherry
        self.th_reg_single = self.th_big_cherry + reg_single
        self.th_reg_cherry = self.th_reg_single + reg_cherry
        self.th_grape = self.th_reg_cherry + grape
        self.th_cherry_single = self.th_grape + cherry_single
        self.th_replay = self.th_cherry_single + replay
        self.th_bell = self.th_replay + bell
        self.th_pierrot = self.th_bell + pierrot

    #スペック表示
    def show_spec(self):
        print(self.name)
        print("設定:%d"%self.setting)
        print("BIG確率:1/%g"%(65536./self.big_total))
        print("REG確率:1/%g"%(65536./self.reg_total))
        print("ボーナス合算:1/%g"%(65536./self.bonus_total))
        print("ブドウ確率:1/%g"%(65536./self.grape))
        print("チェリー確率:1/%g"%(65536./self.cherry_total))
        print("リプレイ確率:1/%g"%(65536./self.replay))
        print("ピエロ確率:1/%g"%(65536./self.pierrot))
        print("ベル確率:1/%g"%(65536./self.bell))

    #現在の回転数, 当たり回数などを表示
    def show_status(self):
        
        if self.counter[0]==0:
            p_big = "BIG確率:0/%d, "%self.rotation_total
        else:
            p_big = "BIG確率:1/%g, "%(float(self.rotation_total)/self.counter[0])
        if self.counter[1]==0:
            p_reg = "REG確率:0/%d, "%self.rotation_total
        else:
            p_reg = "REG確率:1/%g, "%(float(self.rotation_total)/self.counter[1])
        if (self.counter[0]+self.counter[1])==0:
            p_total = "ボーナス合算確率:0/%d"%self.rotation_total
        else:
            p_total = "ボーナス合算確率:1/%g"%(float(self.rotation_total)/(self.counter[0]+self.counter[1]))
        print("現在の回転数:%d, 差枚数:%d, 総回転数:%d, BIG:%d回, REG:%d回"%(self.rotation, self.medal, self.rotation_total, self.counter[0], self.counter[1]))
        print(p_big+p_reg+p_total)
        #n_big = float(self.rotation_total)/(self.counter[0]+1e-07)
        #n_reg = float(self.rotation_total)/(self.counter[1]+1e-07)
        #n_both = float(self.rotation_total)/(self.counter[0]+self.counter[1]+1e-07)
        #print("BIG確率:1/%g, REG確率:1/%g, ボーナス合算:1/%g"%(n_big, n_reg, n_both))

    #小役カウンタを表示(要修正)
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
        #MAXBET時の処理
        self.medal -= 3
        self.rotation += 1
        self.rotation_total += 1
        #フラグが成立している場合は払い出し優先(生入りは考慮しない)
        #それ以外は[単独BIG|チェリーBIG|単独REG|チェリーREG|ブドウ|チェリー(ボナなし)|リプレイ|ピエロ|ベル|ハズレ]のテーブルで抽選を行う
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
            table = np.random.randint(65536)
            if 0<=table<self.th_big_single:
                # 単独BIG
                self.flag_big = True
                result = "ハズレ(ペカッ)"
            elif self.th_big_single<=table<self.th_big_cherry:
                # チェリーBIG
                self.flag_big = True
                self.medal += 2
                self.counter[3] += 1
                result = "チェリー(ペカッ)"
            elif self.th_big_cherry<=table<self.th_reg_single:
                # 単独REG
                self.flag_reg = True
                result = "ハズレ(ペカッ)"
            elif self.th_reg_single<=table<self.th_reg_cherry:
                # チェリーREG
                self.flag_reg = True
                self.medal += 2
                self.counter[3] += 1
                result = "チェリー(ペカッ)"
            elif self.th_reg_cherry<=table<self.th_grape:
                # ブドウ
                self.medal += 7
                self.counter[2] += 1
                result = "ブドウ"
            elif self.th_grape<=table<self.th_cherry_single:
                # チェリー(ボーナスなし)
                self.medal += 2
                self.counter[3] += 1
                result = "チェリー"
            elif self.th_cherry_single<=table<self.th_replay:
                # リプレイ
                self.medal += 3
                self.counter[4] += 1
                result = "リプレイ"
            elif self.th_replay<=table<self.th_bell:
                # ベル
                self.medal += 14
                self.counter[6] += 1
                result = "ベル"
            elif self.th_bell<=table<self.th_pierrot:
                # ピエロ
                self.medal += 10
                self.counter[5] += 1
                result = "ピエロ"
            elif self.th_pierrot<=table:
                # ハズレ
                result = "ハズレ"

        self.log.append(result)
        self.slump.append(self.medal)
        
        return result

class ImJugglerEX(Juggler):

    def __init__(self, settei=1):

        #self.big_prob = np.array([287.4, 282.5, 282.5, 273.1, 273.1, 268.6])#スペック表示しやすいように分母で入力
        #self.reg_prob = np.array([455.1, 442.8, 348.6, 321.3, 268.6, 268.6])
        #self.grape_prob = np.array([6.49, 6.49, 6.49, 6.49, 6.49, 6.18])
        #self.cherry_prob = np.array([33.6, 33.6, 33.4, 33.2, 33.0, 33.0])
        #self.big = self.big_prob[settei-1]
        #self.reg = self.reg_prob[settei-1]
        #self.grape = self.grape_prob[settei-1]
        #self.cherry = self.cherry_prob[settei-1]
        #self.replay = 7.3
        #self.pierrot = 1092.3
        #self.bell = 1092.3
        
        #設定差のある確率
        self.big_single_prob = np.array([160, 164, 164, 168, 168, 172])           #単独BIG確率,x/65536のxで表現
        self.big_cherry_prob = np.array([68, 68, 68, 72, 72, 72])                 #チェリーBIG確率
        self.reg_single_prob = np.array([100, 104, 132, 144, 172, 172])           #単独REG確率
        self.reg_cherry_prob = np.array([44, 44, 56, 60, 72, 72])                 #チェリーREG確率
        self.grape_prob = np.array([10100, 10100, 10100, 10100, 10100, 10600])    #ブドウ確率

        self.big_single = self.big_single_prob[settei-1]
        self.big_cherry = self.big_cherry_prob[settei-1]
        self.reg_single = self.reg_single_prob[settei-1]
        self.reg_cherry = self.reg_cherry_prob[settei-1]
        self.grape = self.grape_prob[settei-1]

        #設定差がない確率
        self.cherry_single = 1840   #ボーナスなしチェリー
        self.replay = 8978          #リプレイ
        self.bell = 60              #ベル
        self.pierrot = 60           #ピエロ

        self.setting = settei

        super(ImJugglerEX, self).__init__("アイムジャグラーEXAE", self.setting, self.big_single, self.big_cherry, self.reg_single, self.reg_cherry, self.grape, self.cherry_single, self.replay, self.bell, self.pierrot)


# 使用例
if __name__ == '__main__':
    
    myjag = ImJugglerEX(1)
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
    for i in range(5000):
        myjag.draw()
    myjag.show_status()
    myjag.show_counter()
    myjag.show_graph(name="slump_graph", save=True)
