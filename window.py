from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import map

#질문 : 파이참 프로그램 코드를 쓰다가 메모할 수 있는 기능이 # 말고 따로 있는지
#창을 키울 수 있는지(단어 입력창)
#배치파일로 만들어서 파이썬이 없는 사람도 실행하도록 만들 수 있는지
#로그인 기능을 만들어서 새로 로그인한 사람들이 자신만의 파일로 사용할 수 있도록 할 수 있을까?
#맞추면 점수가 올라가고 용돈이 쌓이는 그런 기능
#소리가 나면서 실감나게
#연속 5번 맞추면 그 문제는 잘 안 나오도록
#구글스프레드의 이름을 따서 조절할 수 있도록 level1 level2 예지한국사 이런식으로

class CWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # 컨트롤 레이아웃 박스
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()

        # 한글 영어 선택
        self.lang = QComboBox()
        self.lang.addItem('한글')
        self.lang.addItem('영어')
        self.lang.addItem('중국어')
        self.lang.setCurrentIndex(0)

        # 난이도
        self.level = QComboBox()
        self.level.addItem('초보자')
        self.level.addItem('중급자')
        self.level.addItem('전문가')
        self.level.setCurrentIndex(0)

        # 단어 입력창
        self.edit = QLineEdit()
        self.edit2 = QLineEdit()

        # 게임 시작버튼
        self.btn = QPushButton('게임시작')
        self.btn.setCheckable(True)
        self.btn.toggled.connect(self.toggleButton)

        # 점수라벨 달기
        self.label1 = QLabel('Yejinu score', self)
        self.label1.setAlignment(Qt.AlignCenter)
        self.font1 = self.label1.font()
        self.font1.setPointSize(10)
        self.label1.setFont(self.font1)

        # 수평 레이아웃 위젯 추가
        self.hbox.addWidget(self.lang)
        self.hbox.addWidget(self.level)
        self.hbox.addWidget(self.edit)
        self.hbox.addWidget(self.btn)

        self.vbox.addStretch(1)
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle('OKdictionary')

        self.map = map.CMap(self)

    def closeEvent(self, e):
        self.map.gameOver()

    def paintEvent(self, e):
        qp = QPainter();
        qp.begin(self)
        self.map.draw(qp)
        qp.end()

    def toggleButton(self, state):
        if state:
            self.map.gameStart(self.lang.currentIndex(),
                               self.level.currentIndex())
            self.btn.setText('게임종료')
            self.lang.setEnabled(False)
            self.level.setEnabled(False)
        else:
            self.map.gameOver()
            self.btn.setText('게임시작')
            self.lang.setEnabled(True)
            self.level.setEnabled(True)

    def keyPressEvent(self, e):
        # 계속 포커스를 가지도록
        self.edit.setFocus()

        # 엔터키 입력시 단어 확인
        if e.key() == Qt.Key_Return:
            self.map.delword(self.edit.text())
            self.edit.setText('')