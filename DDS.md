# DDS (Detailed Design Specification)

## Main.py

#### LoginWindow
| |이름 |역할,설명 | 
|----|---- |---- |
|attributes|mainlayout |아래의 위젯들이 표시되는 메인 레이아웃 |
|-- |gametitle |화면에 표시되는 게임제목 |
|-- |gametitlefont |" 의 폰트 |
|-- |story |게임의 줄거리|
|-- |storylabel |게임의 줄거리를 화면에 표시 |
|-- |storyfont |"의 폰트 |
|-- |self.nameinput |이름 입력칸 |
|-- |inputbutton |입력된 이름으로 로그인하기 |
|method|\_\_init\_\_생성자|로그인창을 생성한다. |
|-- |setUI |로그인창 UI를 보여준다. |
|-- | buttonClicked |로그인창을 닫고,self.nameinput에 입력된 이름을 MainWindow의 인자로 넘겨준다.  |
#### DefeatWindow
| |이름 |역할,설명 | 
|----|---- |---- |
|attributes |self.name|화면에 표시될 플레이어 이름 |
|-- |self.time |화면에 표시될 게임상 시간 |
|-- |self.peakofmoney |화면에 표시될 최대 보유금액 |
|-- |mainlayout  |다른 레이어들의 메인레이아웃 |
|-- |recordlayout |기록관련 위젯이 위치할 레이아웃 |
|-- |retrylayout |다시하기관련 위젯이 위치할 레이아웃 |
|-- |recordfont |기록관련 위젯의 폰트 |
|-- |namelabel |화면에 표시되는 플레이어 이름 |
|-- |timelabel |화면에 표시되는 게임상 시간 |
|-- |peakofmoneylabel |화면에 표시되는 최대 보유금액 |
|-- |bankruptlabel |화면에 표시되는 파산 알림 메세지 |
|-- |bankruptfont | " 의 폰트 |
|-- |retrylabel |플레이어에게 다시할 지 물어보는 메세지 |
|-- |retrybutton |다시하기 버튼 |
|method|\_\_init\_\_생성자|패배창을 생성한다. |
|-- |setUI |패배창 UI를 보여준다. |
|-- |buttonClicked |패배창을 닫고 로그인화면을 띄운다. |
#### AchievementWindow
| |이름 |역할,설명 | 
|----|---- |---- |
|attributes |self.achievement|달성한 업적의 종류 |
|-- |self.record |플레이어의 업적 달성 기록 |
|-- |self.totalrecord |다른 플레이어들의 업적 달성 기록 |
|-- |mainlayout |메인 레이아웃 |
|-- |labellayout |기타 라벨들의 레이아웃 |
|-- |recordlayout |기록관련 위젯들의 레이아웃 |
|-- |buttonlayout |계속하기 버튼의 레이아웃 |
|-- |achievementlabel |달성한 업적이 무엇인지 표시 |
|-- |achievementfont | " 의 폰트 |
|-- |myrecord|현재 플레이어의 기록 표시 |
|-- |font0|" 의 폰트 |
|-- |recordlabel1| 순위표의 제목 표시 |
|-- |font1 |" 의 폰트 |
|-- |recordlabel2 |순위표의 범주 표시 |
|-- |self.records| 업적 달성 순위표 |
|-- |continuebutton|계속하기 버튼 |
|method|\_\_init\_\_생성자|업적창을 생성한다. |
|-- |setUI |업적창 UI를 보여준다. |
|-- |showRank|인자로 전달 받은 기록을 순위표에 한줄 씩 보여준다. |
|-- |buttonClicked |업적창을 닫는다. |
#### MainWindow
| |이름 |역할,설명 | 
|----|---- |---- |
|attributes |self.totaldata|파일에 저장된 이 게임에 모든 사용자 정보 |
|--|self.data|데이터 파일에 저장될 데이터의 모음. 플레이어 이름,게임상 시간, 최대보유금액, 현재보유금액, 남은 빚, 가계부기록, 비트코인정보, 홀짝게임정보, 구매한 물감,업적달성현황이 사전형식으로 저장된다.|
|--|self.playername|플레이어 이름|
|--|self.debt|남은 빚|
|--|self.money|현재 보유 금액|
|--|self.time|게임 상 시간. [주,일,시간,분]으로 돼있다.|
|--|self.peakofmoney|최대 보유금액|
|--|self.current_brush_color|현재 보유 물감(색상)|
|--|self.already108|1억(10**8)원 달성 여부|
|--|self.already1010|100억(10**10)원 달성 여부|
|--|self.already1012|1조(10**12)원 달성 여부|
|--|self.already1016|1경(10**16)원 달성 여부|
|--|self.already1020|1해(10**20)원 달성 여부|
|--|self.alreadyac|모든 물감 구입 여부|
|--|mainlayout|메인레이아웃|
|--|statuslayout|상태창의 레이아웃|
|--|tablayout|그림판/상점/돈벌기 창을 전환할 수 있는 탭의 레이아웃.|
|--|historylayout|가계부의 레이아웃|
|--|self.paintertab|그림판 탭|
|--|self.storetab|상점 탭|
|--|self.getmoneytab|비트코인/홀짝게임 탭|
|--|self.namelabel|상태창에 표시되는 플레이어 이름|
|--|self.moneylabel|상태창에 표시되는 현재 보유금액|
|--|self.timelabel|상태창에 표시되는 게임상시간|
|--|self.historylabel|가계부 제목과 현재 남은 빚을 표시|
|--|self.history|가계부 |
|method|\_\_init\_\_생성자|메인 화면을 생성한다. |
|-- |setUI |메인화면 UI를 보여준다. |
|--|dataLoad|MainWindow가 생성되면, LoginWindow에서 입력된 이름으로 저장된 데이터가 있는지 확인하고, 이를 불러와 self.data에 덮어쓴다. |
|--|dataSave|self.data를 현재정보로 업데이트하고, 파일에 저장한다. 그리고 그리던 그림은 그림파일로 저장한다. |
|--|recordLoad|저장된 기록 파일에서 파일을 불러와 반환한다.|
|--|recordSort|전달받은 기록에 현재 기록을 추가하고 등수로 정렬한뒤, 10개 넘어가면 자른다.|
|--|recordSaveNReturn|기록을 불러오고, 정렬한뒤, 기록파일에 저장한다.|
|--|moneyUpdate|입력받은 금액만큼 현재보유금액을 갱신하고, 입력받은 텍스트를 가계부에 추가한다. 그리고 변한 보유금액이 플레이어의 최대보유금액을 초과했는지 확인한다.|
|--|historyUpdate|입력받은 텍스트를 가계부에 추가한다.|
|--|peakofmoneyUpdate|현재보유금액이 최대보유금액을 초과했는지 판별하여 최대보유금액을 갱신한다.|
|--|timeUpdate|비트코인 그래프 애니메이션으로 부터 호출된다. self.time에 1씩더해 시계처럼 작동하며, 1시간이 지나면, 홀짝게임의 결과를 발표하고, 일주일이 지나면, 빚을 갚는 것을 반복한다. |
|--|payBack|게임상시간이 1주이링 지날 때마다 남은 빚이 있으면, 일정 금액을 상환한다. 만약 현재 보유금액이 상환액보다 적으면, 구매한 물감을 압류한다. 압류당할 물감도 없으면, 파산한다.|
|--|foreclosure|보유한 물감을 랜덤으로 삭제하고, 콤보박스에서 이를 지우며, 해당 색을 상점에서 다시 활성화하고 어떤 물감을 압류당했는지 반환한다.|
|--|defeat|시간의 흐름을 중지하고, 메인 창을 닫고, 패배화면창을 띄운다.|
|--|bankrupt|현재보유금액이 없거나, 비트코인의 보유량이 0이거나, 홀짝게임의 충전금이 0이어서 더이상 돈을 벌 방법이 없다면 파산처리한다.|
|--|showAchievement|업적 달성했는지 판별하고, 업적달성을 했으면, 현재 데이터를 저장하고 달성한 업적, 현재플레이어의 기록, 다른 플레이어의 해당 업적 기록 정보를 갖는 업적창을 띄운다.|
|--|achievement|업적 달성했는지 판별하는 함수. 달성한 업적의 종류를 반환한다. 만약 업적 달성이 아니면 0을 반환한다.|
|--|buttonClicked|데이터를 저장할 지 물어보고 yes면 데이터를 저장한다. |

## Painter.py

#### Painter
| |이름 |역할,설명 | 
|----|---- |---- |
|attributes|self.status|전달받은 MainWindow의 인스턴스를 정의한다.|
|--|mainlayout|메인 레이아웃|
|--|toollayout|도구의 레이아웃|
|--|canvaslayout|캔버스의 레이아웃|
|--|self.canvas|캔버스의 인스턴스|
|--|self.tool|도구의 인스턴스|
|method|\_\_init\_\_생성자||
|--|setUI|그림판 UI를 보여준다.|

## PainterTool.py

#### PainterTool
| |이름 |역할,설명 | 
|----|---- |---- |
|attributes|self.status||
|--|self.canvas||
|--|self.save_eraser_size||
|--|self.save_brush_size||
|--|self.save_line_size||
|--|self.save_brush_mode||
|--|self.save_point||
|--|self.save_red||
|--|self.save_blue||
|--|self.save_green||
|--|self.save_alpha||
|--|self.save_brush_color||
|--|self.tools||
|--|self.cb||
|--|self.label||
|method|\_\_init\_\_생성자||
|--|setUI|도 UI를 보여준다.|
|--|comboBoxFunction||
|--|save||
|--|clear||
|--|ChangedColor||
|--|ChangedSize||
|--|ChangedRGBA||
|--|MakeColor||
|--|ChangedValue||
|--|ChangedFont||
|--|buttonClicked||
|--|setThickness||
|--|changingMode||
|--|ChangedText||
|--|ColorEffect||

## Canvas.py

#### Canvas
| |이름 |역할,설명 | 
|----|---- |---- |
|attributes|self.status||
|--|self.drawingPath||
|--|self.image||
|--|self.drawing||
|--|self.color_r||
|--|self.color_g||
|--|self.color_a||
|--|self.brush_color||
|--|self.brush_size||
|--|self.brush_mode||
|--|string||
|--|stringFont||
|--|stringFontSize||
|--|save_drawingType||
|--|past_point||
|--|present_point||
|method|\_\_init\_\_생성자||
|--|setUI||
|--|paintEvent||
|--|mousePressEvent||
|--|mouseMoveEvent||
|--|mouseReleaseEvent||

## Store.py

#### Store
| |이름 |역할,설명 | 
|----|---- |---- |
|attributes|self.status||
|--|||
|--|||
|--|||
|--|||
|--|||
|--|||
|method|\_\_init\_\_생성자||
|--|||
|--|||
|--|||






