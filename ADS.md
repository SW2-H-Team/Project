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
생성자에 전달되는 status는 MainWindow의 인스턴스를 의미한다.

|클래스| 메서드| 입력인자| 출력인자| 기능|
|----|----|----|----|----|
|LoginWindow|\_\_init\_\_생성자| | |
|--|setUI| | |로그인창의 UI를 보여준다|
|--|buttonClicked| | |'로그인'버튼의 콜백함수. 창을 닫고입력된 이름을 MainWindow에 넘겨준다.|
|DefeatWindow|\_\_init\_\_생성자|status| |status로부터 사용자 이름, 기록, 최대보유금액을 받는다. |
|--|setUI| | |패배화면의 UI를 보여준다.|
|--|buttonClicked| | |'다시하기'버튼의 콜백함수. 창을 닫고 로그인화면으로 넘어간다.|
|AchievementWindow|\_\_init\_\_생성자|achievement, record, totalrecord| |업적종류, 사용자기록, 저장된 기록을 받는다.|
|--|setUI| | |업적창의 UI를 보여준다.|
|--|showRank|totalrecord| |totalrecord의 기록들을 업적창의 textedit에 출력한다.|
|--|buttonClicked| | |'계속하기'버튼의 콜백함수. 창을 닫고 게임을 계속 진행할 수 있게 한다.|
|MainWindow|\_\_init\_\_생성자|name| |name에 해당하는 데이터들을 불러오거나 초기화 한다.|
|--|setUI| | |게임화면의 UI를 보여준다.|
|--|dataLoad|name| |name에 해당하는 데이터를 불러와 변수에 저장한다. |
|--|dataSave| | |지금까지의 데이터를 파일에 저장한다.|
|--|recordLoad| |totalrecord|업적달성시 기록저장을 위해 데이터를 불러온다.|
|--|recordSort|totalrecord, achievement|totalrecord|전달받은 totalrecord를 정렬하여 반환한다.|
|--|recordSaveNReturn|achievement, record|totalrecord[achievement]|기록파일에 자신의 데이터를 추가하고, 반환한다.|
|--|moneyUpdate|money,text| |현재 보유금액을 변경한다.|
|--|historyUpdate|text| |가계부를 갱신한다.|
|--|peakofmoneyUpdate| | |최대 보유금액을 갱신한다.|
|--|timeUpdate| | |게임상 시간을 흐르게 한다.|
|--|payBack| | |빚을 갚는다. 일정 금액을 내지 못하면 압류당한다.|
|--|foreclosure| |color|채무상환기간에 일정금액을 지불하지 못하면 보유한 물감을 압류하고, 물감의 색상을 반환한다.|
|--|defeat| | |진행중인 게임을 중지하고 패배창을 띄운다.|
|--|bankrupt| |True/False|돈이 없으며 더이상 돈을 벌 수가 없으면 파산.|
|--|showAchievement| | |업적 달성시 업적달성창을 띄운다.|
|--|achievement| |#달성한 업적/0|업적을 달성했다면, 해당한 업적 종류를 반환|
|--|buttonClicked| | |'데이터 저장'버튼의 콜백함수. 지금까지의 데이터를 파일에 저장한다.|
|Painter|\_\_init\_\_생성자|status| |Canvas와 PainterTool에 넘겨줄 status를 정의한다.|
|--|setUI| | |그림판을 구성하는 UI를 보여준다.|
|Canvas|\_\_init\_\_생성자|status| |그림그리는데 필요한 설정들을 초기화한다.|
|--|setUI| | |윈도우를 설정하고 보인다. |
|--|paintEvent|e| |그림을 그리고 그 그린 모습을 화면에 띄워준다. |
|--|mousePressEvent|e| |마우스 왼쪽 버튼을 누르면 대게 그 좌표 값을 저장한다. |
|--|mouseMoveEvent|e| |마우스 왼쪽 버튼을 누른 채 마우스를 움직이면 대게 마우스 포인트를 따라 그림을 그린다. |
|--|mouseReleaseEvent|e| |마우스 왼쪽 버튼을 떼면 self.save_drawingType에 따라 그린 결과를 보여준다. |
|PainterTool|\_\_init\_\_생성자|canvas, status| |Canvas에서 사용해야 하는 도구 기능에 필요한 변수 값을 저장한다. |
|--|setUI| | |도구에 대한 UI를 보여준다.|
|--|comboBoxFunction| | |ComboBox를 통해 상점에서 구매한 색으로 변경을 시도하면 클래스에서 이용가능한 변수에 값을 저장한다. |
|--|save| | |그린 그림을 저장한다.|
|--|clear| | |캔버스에 있는 모든 그림 지우기|
|--|ChangedColor|color| |색깔 변경시 라벨에 해당 색을 보여주고 색을 변경한다. |
|--|ChangedSize|size| |붓크기를 입력된 size로 바꾼다.|
|--|ChangedRGBA|r, g, b, a| |rgb와 투명도값으로 현재 색상을 바꾼다.|
|--|MakeColor| | |현재 rgb와 투명도값으로 색을 배합한다.|
|--|ChangedValue|color, size, mode| |전달된 값으로 그리기 설정을 바꾼다.|
|--|ChangedFont|font, size| |입력될 텍스트의 폰트와 크기를 설정한다.|
|--|buttonClicked| | |그림판에 있는 모든 버튼에 대한 콜백함수. 각 버튼마다 기능을 호출한다.|
|--|setThickness| | |선굵기 조절 창을 띄운다.|
|--|changingMode| |result|선 모드 변경창을 띄워 결과를 반환하여 반환한다.|
|--|ChangedText| | |텍스트 입력 설정창을 띄운다.|
|--|ColorEffect| | |투명도 조절 창을 띄운다.|
|Store|\_\_init\_\_생성자|status| | |
|--|setUI| | |상점UI를 보여준다.|
|--|buttonClicked| | |각 색상버튼에 대한 콜백함수. 버튼 입력시 구매창이 나타난다.|
|--|priceChange| | |물감구입 마다 물감가격을 인상한다.|
|GetMoney|\_\_init\_\_생성자|status| |BitcoinMarket과 OddOrEven에 전달한 status를 정의한다.|
|--|setUI| | | 돈벌기의 UI를 보여준다.|
|Bitcoin|\_\_init\_\_생성자|status,holding,x,y,investmentamount|  |입력된 값으로 비트코인을 생성한다. |
|--|setUI| | |비트코인 낱개에 대한 UI를 보여준다.|
|--|buttonClicked| | |매수/매도 버튼에 대한 콜백함수. 비트코인 거래를 할 수 있다.|
|--|changeEconomy| |True/False|매 분마다 그래프의 기울기 추세를 변경할 지 정한다.|
|--|changeGradient| |True/False|매 분마다 그래프의 기울기를 변경할 지 정한다. |
|--|updateEconomy| | | 기울기 추세를 재설정한다. |
|--|updateGradient| | | 기울기를 재설정한다. |
|--|setAdjustment| | | 비트코인 가격 성장의 폭을 설정한다. |
|--|setSubGradient| | | 현실성있는 그래프를 보여주기 위해 기울기를 조정한다. |
|--|setYLim| | |비트코인 가격의 구간마다 그래프의 Y축을 설정한다.|
|--|updateLine|i|[self.line]|매 분마다 그래프와 비트코인 정보를 갱신하며, 시간의 흐름을 생성한다. |
|BitcoinMarket|\_\_init\_\_생성자|status| | Bitcoin에 넘겨줄 status를 정의한다.|
|--|setUI| | | 여러 비트코인을 보여준다. |
|--|setBitcoinName| |name |무작위의 비트코인 이름을 생성한다. |
|--|bitcoinLoad|status,index| |데이터에 저장돼있는 비트코인 정보를 불러온다.| 
|--|bitcoinGenerate| | |하나의 비트코인을 생성해 화면에 추가한다.|
|OddOrEven|\_\_init\_\_생성자|status| | |
|--|setUI| | |홀짝게임 UI를 보여준다.|
|--|statusUpdate|text| |상태메세지를 변경한다.|
|--|chargeUpdate|amount| |충전금을 amount만큼 변경한다.|
|--|getNumber| | |매 시간마다 홀/짝 결과를 낸다.|
|--|checkResult|number| |사용자의 선택과 결과를 비교한다. |
|--|historyUpdate|number| |화면에 표시되는 결과의 기록을 갱신한다. |
|--|buttonClicked| | | 충전/출금, 홀/짝 버튼의 콜백함수. |
|Button|\_\_init\_\_생성자|text, callback| |전달받는 콜백함수를 가진 버튼을 생성한다. |
|Slide_Thickness|\_\_init\_\_생성자| tool | |현재 선택중인 버튼에 맞는 창제목을 설정한다. |
|--|setUI| | |슬라이드 창을 보여준다. |
|--|setText| | |창에 표시되는 숫자를 슬라이드 변화에 맞춘다. |
|--|buttonClicked| | |ok/cancel 버튼에 대한 콜백함수. |
|Slide_ChangedText|\_\_init\_\_생성자|item, tool, items| | |
|--|setUI| | |슬라이드 창을 보여준다. |
|--|setText| | |창에 표시되는 숫자를 슬라이드 변화에 맞춘다.|
|--|buttonClicked| | |ok/cancel 버튼에 대한 콜백함수. |
|Slide_ColorEffect|\_\_init\_\_생성자|tool| | |
|--|setUI| | |슬라이드 창을 보여준다. |
|--|setText| | |창에 표시되는 숫자를 슬라이드 변화에 맞춘다.|
|--|buttonClicked| | |ok/cancel 버튼에 대한 콜백함수. |
