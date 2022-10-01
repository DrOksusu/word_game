from PyQt5.QtCore import QPointF, QRect
from PyQt5.QtGui import QFont
from threading import Thread, Lock
from random import randint
from time import sleep
from gs import *

#gs.py 에서 읽은 데이타 가져오기
print(list_data)
a = list_data
kor = []
eng = []

i=1
while i < len(a):
    kor.append(a[i][0])
    eng.append(a[i][1])
    i += 1

print(kor)
print(eng)

# 튜플 단어장
# kor = ('문자열', '정수', '리스트', '튜플', '딕셔너리',
#        '타입', '출력', '반복문', '변수', '파이썬')
# eng = ('input', 'int', 'string', 'type', 'list', 'class',
#        'print', 'python', 'tuple', 'for', 'if', 'while',
#        'thread', 'random', 'with', '__init__', '__del__')




# text 파일에서 항목 넣기!
# f = open('word.txt', encoding='UTF-8')
# while True:
#     line = f.readline()
#     line = line.strip()
#     if not line : break
#     word1 = line.split(':')[0].strip()
#     kor.append(word1)
#     word2 = line.split(':')[1].strip()
#     eng.append(word2)
# f.close()
# 만약에 CSV로 읽어 올려면 line.split(',')
# import csv
#
# f = open('data.csv', 'r', encoding='utf-8')
# rdr = csv.reader(f)
# for line in rdr:
#     print(line)
# f.close()
# CSV ... END



class CWord:
    def __init__(self, pt, word, word_kor, word_eng):
        # 단어 좌표
        self.pt = pt
        # 단어 문자
        self.word = word
        self.word_kor = word_kor
        self.word_eng = word_eng

class CMap:
    def __init__(self, parent):
        self.parent = parent
        self.rect = parent.rect()
        self.word = []
        self.word_kor = []
        self.word_eng = []
        self.thread = Thread(target=self.play)
        self.bthread = False
        self.lock = Lock()
        #스코어 만들기
        self.score = 50


    def __del__(self):
        self.gameOver()

    def gameStart(self, lang, level):
        self.lang = lang
        self.level = level

        self.bthread = True
        if self.thread.is_alive() == False:
            self.score = 50
            self.parent.label1.setText("Yejinu score: " + str(self.score))

            self.thread = Thread(target=self.play)
            self.thread.start()

    def gameOver(self):
        self.bthread = False
        self.word.clear()
        self.parent.update()

    def draw(self, qp):
        qp.setFont(QFont('맑은 고딕', 12))
        self.lock.acquire()
        for w in self.word:
            qp.drawText(w.pt, w.word)
        self.lock.release()

    def createWord(self):

        self.rect = QRect(self.parent.rect())

        # 무작위 단어 선정
        _str = ''
        num = 0
        if self.lang == 0: # 한글
            n = randint(0, len(kor) - 1) # 랜덤
            num = 0
            _str = kor[n]
            self.word_eng.append(eng[n]) # Game Map에다가 영어 단어 넣기!
        else:
            n = randint(0, len(eng) - 1) # 랜덤
            num = 0
            _str = eng[n]
            self.word_kor.append(kor[n]) # Game Map에다가 한글 단어 넣기!

        # 무작위 좌표 선정
        x = randint(0, self.rect.width() - 50)
        y = 0

        cword = CWord(QPointF(x, y), _str, kor[num], eng[num])
        self.word.append(cword)

    def downWord(self, speed):
        i = 0
        for w in self.word[:]:
            if w.pt.y() < self.rect.bottom():
                w.pt.setY(w.pt.y() + speed)
                i += 1
            else:
                del (self.word[i])

                if self.lang == 0:
                    del (self.word_eng[i])
                else:
                    del (self.word_kor[i])

                self.score = self.score - 1
                self.parent.label1.setText("Yejinu score: " + str(self.score))
                if self.score < 48:
                    self.gameOver()




    def delword(self, _str):
        self.lock.acquire()

        i = 0
        find = False

        if self.lang == 0:
            for w in self.word_eng[:]:
                if _str == w:
                    del (self.word[i])
                    del (self.word_eng[i])
                    find = True

                    #스코어 매기기
                    self.score = self.score + 1
                    self.parent.label1.setText("Yejinu score: " + str(self.score))

                    break
                else:
                    i += 1
        else:
            for w in self.word_kor[:]:
                if _str == w:
                    del (self.word[i])
                    del (self.word_kor[i])
                    find = True

                    #스코어 매기
                    self.score = self.score + 1
                    self.parent.label1.setText("Yejinu score: " + str(self.score))
                    break
                else:
                    i += 1
            # if self.lang == 0:
            #     if _str == w.word_eng:
            #         del (self.word_kor[i])
            #         del (self.word_eng[i])
            #         del (self.word[i])
            #         find = True
            #         break
            #     else:
            #         i += 1
            # else:
            #     if _str == w.word_kor:
            #         del (self.word_kor[i])
            #         del (self.word_eng[i])
            #         del (self.word[i])
            #         find = True
            #         break
            #     else:
            #         i += 1

        self.lock.release()

        if find:
            self.parent.update()

    def play(self):
        while self.bthread:
            if randint(1, 200) == 1:
                self.lock.acquire()
                self.createWord()
                self.lock.release()

            self.lock.acquire()
            if self.level == 0:
                self.downWord(0.3)
            elif self.level == 1:
                self.downWord(0.5)
            else:
                self.downWord(0.7)
            self.lock.release()

            self.parent.update()
            sleep(0.01)