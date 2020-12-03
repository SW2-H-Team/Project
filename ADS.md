ADS(Architecture Design Specification)
=======================================

## 1. 소프트웨어 구조 설계
| 모듈 | 클래스 | 역할 |
|----|----|----|
|Main.py|LoginWindow |데이터를 불러올 수 있도록 사용자의 입력을 받는 창.|
|--     |DefeatWindow|패배조건 충족시 게임을 중지시키고 패배를 알리는 창|
|--     |AchievementWindow|특정조건 충족시 업적 달성을 알리는 창|
|--     |MainWindow|LoginWindow에서 입력받은 이름으로 게임을 플레이할 수 있는 메인윈도우|
|Painter.py|Painter|Canvas와 PainterTool을 묶어 화면에 표시한다.|
|Canvas.py|Canvas|사용자가 직접 원하는 그림을 그릴 수 있는 공간|
|PainterTool.py|PainterTool|각 종 그리기 설정을 할 수 있는 도구 |
|Store.py|Store|물감들을 구매하여 그림판에 추가할 수 있게 한다.|
|GetMoney.py|GetMoney|돈을 벌 수 있는 클래스(BitcoinMarket,OddAndEven)들을 묶어 화면에 표시한다.|
|Bitcoin.py|Bitcoin|각 비트코인의 정보를 담고있다. |
|--         |BitcoinMarket|5개의 비트코인을 묶어 화면에 표시한다.|
|OddAndEven.py|OddAndEven|홀짝게임을 할 수 있는 화면이다.|
|Button.py|Button|버튼을 생성하는 클래스|
|Slide.py|Slide_Thickness|선굵기를 조절할 수 있도록 창을 띄운다.|
|--|Slide_ChangedText|Canvas에 표시할 텍스트의 크기를 조절할 수 있는 창을 띄운다.|
|--|Slide_ColorEffect|그리는 선의 투명도를 조절할 수 있는 창을 띄운다.|

## 2. 클래스 인터페이스 설계
각 클래스마다 UI를 설정하는 setUI 메소드는 생략.

|클래스| 메서드| 입력인자| 출력인자| 기능|
|----|----|----|----|----|
|LoginWindow|||||