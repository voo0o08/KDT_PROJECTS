'''
카드 짝 찾기 게임!!
1. 게임 시작"
2. 불러오기"
3. 저장 후 게임 종료"
4. 그냥 게임 종료"
v4 - 딕셔너리 파일화
주석 추가
'''
import random
cardShape = ("🐳", "🐥", "🦊", "🐻", "🃏") # 카드 모양
userMap = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] # 현재 게임현황 및 사용자가 볼 수 있는 부분
cardMap = () # 답지
userDict = {}
# userDict = {"Lee" : {"ans" : ('🦊', '🐳', '🐻', '🦊', '🐻', '🐥', '🐳', '🐳', '🐥', '🐻', '🦊', '🐥'),
#                      "cur" : ('🃏', '🃏', 3, '🃏', 5, '🃏', '🃏', '🃏', '🃏', '🃏', '🃏', '🃏'),
#                      "finCard" : (1, 2, 4, 6, 7, 8, 9, 10, 11, 12)}}
finishCard = [] # 짝맞추기에 성공한 카드 번호들이 저장됨 -> [1, 5, 12, 7...]
# {이름 : {ans : cardMap, cur : userMap, finCard : finishCard}}
memory = False # 현재 저장할 게임이 존재하는지
end = False # 게임이 종료되었는지
filename = "userGameLog.txt"
# filename = "test.txt"

def LogUser():
    '''
    사용자 로그를 불러오기 위한 함수
    :return:
    '''
    try:
        with open(filename, mode="r", encoding="utf8") as f:
            userList = f.readlines()
            # print(userList)
            for i in range(0, len(userList), 4):
                tempDict = {"ans": tuple(userList[i + 1][:-1].split()),
                            "cur": tuple(int(e) if e.isdecimal() else e for e in userList[i + 2][:-1].split(" ")),
                            "finCard": tuple(int(e) if e.isdecimal() else e for e in userList[i + 3][:-1].split(" "))}
                userDict[userList[i][:-1]] = tempDict
    except FileNotFoundError:
        # print("예외처리 완료")
        # 파일이 존재하지 않는다면 그냥 return
        return

def saveUser():
    '''
    로그 일부 삭제 -> 딕셔너리 삭제하고 걍 새로 쓰는게 나을 듯하다!!!
    이름 받고 지우고 mode="w"로 새로 작성하기
    :return:
    '''
    with open(filename, mode="w", encoding="utf8") as f:
        for userNameSave, userDictSave in userDict.items():
            f.writelines(userNameSave+"\n")
            f.writelines(" ".join(userDictSave["ans"])+"\n")
            f.writelines(" ".join(map(str, userDictSave["cur"]))+"\n")
            f.writelines(" ".join(map(str, userDictSave["finCard"]))+"\n")


def continueCheck():
    '''
    유저가 게임을 계속해서 진행할 것인지를 확인하고,
    올바르게 입력되었다면 해당 값을 return해준다.
    '''
    while True:
        continueInput = input("게임 종료 = 1 / 계속 진행 =  엔터 : ")
        if continueInput in ("1", ""):
            return continueInput
        else:
            print("입력이 잘못되었습니다.")

def cardCheck():
    '''
    사용자가 확인하고자 하는 카드 값을 입력받고, 
    올바른 입력이라면 카드 값을 리턴한다.
    '''
    while True:
        cardInput = input("원하는 카드 2개를 선택하세요(예시:1 4) : ").split()
        if len(cardInput) != 2: # 입력을 1개만 한 경우 불가능
            print("입력이 잘못되었습니다.(예시:1 4)")
        else:
            c1, c2 = map(int, cardInput)
            if c1 in range(1, 13) and c2 in range(1, 13):
                if c1 in finishCard or c2 in finishCard: # 이미 짝을 찾은 카드라면 입력 불가능
                    print("이미 짝을 찾은 카드입니다.")
                else:
                    return c1, c2
            else: # 범위를 벗어난 카드 번호라면 입력 불가능
                print("1~12 사이의 숫자 2개를 선택해주세요.")

def mapPrint(map):
    '''
    보고 싶은 리스트를 3개씩 끊어서 출력해줌
    map : userMap, cardMap(답지) 등 현재 사용자에게 보여주어야 하는 리스트
    '''
    print()
    for idx, c in enumerate(map, 1):
        if idx % 3 == 0:
            if c in cardShape:
                print(f"{c:}")
            else:
                print(f"{c:0>2}")
        else:
            if c in cardShape:
                print(f"{c:}", end=" ")
            else:
                print(f"{c:0>2}", end=" ")
    return

def start(Map):
    '''
    게임이 실행되는 함수
    :param Map:
    :return:
    '''
    global memory
    memory = True # 게임이 시작되면 저장가능한 데이터가 생기게 된다.
    while True:

        mapPrint(userMap)
        card1, card2 = cardCheck()
        # print(userMap)
        # 본인이 선택한 카드를 출력해줌

        copyMap = userMap.copy()
        copyMap[card1-1] = cardMap[card1-1]
        copyMap[card2-1] = cardMap[card2-1]

        mapPrint(copyMap) # 사용자가 선택한 카드의 문양을 보여줌
        copyMap.clear()

        if cardMap[card1-1] == cardMap[card2-1]:
            userMap[card1-1], userMap[card2-1] = "🃏", "🃏"
            finishCard.append(card1)
            finishCard.append(card2)
            print("짝맞추기 성공")

            if len(finishCard) == 12: # 종료조건 : 짝맞춤이 완료된 카드 리스트의 개수가 12개일 때
                mapPrint(cardMap)
                print("게임이 종료되었습니다!! 축하합니다!!\n")
                global end
                end = True
                return
            userInput = continueCheck()
        else:
            userInput = continueCheck()

        if userInput == "1":
            return
        print()


# ----------------------------- main문 -----------------------------
LogUser() # 사용자 로그 불러오기
while True:
    if end: # game함수 내에서 end 플래그가 on으로 바뀌면 게임 종료
        break
    print("[🃏카드 짝 찾기 게임🃏]")
    print("1. 게임 시작")
    print("2. 불러오기")

    if memory: # 게임을 진행하면 momory 플래그가 True가 되어 3, 4번 보기가 생김
        print("3. 저장 후 게임 종료")
        print("4. 그냥 게임 종료")
    choice = input("기능 선택 : ")
    if choice == "1":

        while True:
            wantLevel = int(input("카드 종류를 선택하세요(2개~4개) : "))  # 사용자가 원하는 레벨 선택
            if wantLevel in range(2, 5):
                break
            else:
                print("잘못된 입력입니다.")

        userCard = cardShape[:wantLevel]
        # print(userCard)
        eachCardNum = 12//wantLevel # 각 카드가 몇개 필요한지 계산해주는 변수

        tempList = []
        for i in userCard:
            for j in range(eachCardNum):
                tempList.append(i)
        # print(tempList)
        random.shuffle(tempList)

        cardMap = tuple(tempList)
        print(cardMap)
        start(cardMap)
    elif choice == "2": # 2. 불러오기
        # {이름 : {ans : cardMap, cur : userMap}}
        nameInput = input("이름을 입력해주세요 : ")
        if nameInput in userDict.keys():
            nowUserDict = userDict[nameInput]
            cardMap = nowUserDict["ans"]
            userMap = list(nowUserDict["cur"])
            finishCard = list(nowUserDict["finCard"])
            start(cardMap) # 저장된 정보를 불러 온 후 게임 시작

        else:
            print("찾을 수 없는 사용자입니다.")

    elif choice == "3" and memory:  # 3. 저장 후 게임 종료
        nameInput = input("이름을 입력해주세요 : ")
        nowUserDict = {"ans" : cardMap, "cur" : tuple(userMap), "finCard" : tuple(finishCard)}
        userDict[nameInput] = nowUserDict
        print("저장이 완료되었습니다.")
        for k, v in userDict.items():
            print(k, v)
        saveUser()

        break

    elif choice == "4" and memory: # 4. 그냥 게임 종료"
        print("게임을 종료합니다")
        break

    else: # 선택지에 없는 숫자를 선택하면 넣어줄 문구
        print("지원하지 않는 기능입니다.\n")