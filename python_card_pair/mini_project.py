'''
카드 뒤집기 게임!!
'''
import random
cardShape = ("A", "B", "C", "D")
userMap = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] # 현재 게임현황 및 사용자가 볼 수 있는 부분
cardMap = () # 답지
userDict = {"Lee" : {"ans" : ('B', 'C', 'B', 'A', 'C', 'B', 'A', 'A', 'C', 'A', 'B', 'C'), "cur" : (1, '@', 3, '@', '@', '@', '@', '@', '@', '@', '@', '@')}}
# #{이름 : {ans : cardMap, cur : userMap}}
memory = False
end = False

def mapPrint(map):
    print()
    for idx, c in enumerate(map, 1):
        if idx % 3 == 0:
            print(f"{c:^4}")
        else:
            print(f"{c:^4}", end="")
    return

def start(Map): #game 진행
    global memory
    memory = True
    while True:
        # for idx, c in enumerate(userMap, 1):
        #     if idx%3 == 0:
        #         print(f"{c:^4}")
        #     else:
        #         print(f"{c:^4}", end=" ")
        mapPrint(userMap)
        card1, card2 = map(int, input("원하는 카드 2개를 선택하세요(예시:1 4) : ").split())

        # print(userMap)
        # 본인이 선택한 카드를 출력해줌
        copyMap = userMap.copy()
        copyMap[card1-1] = cardMap[card1-1]
        copyMap[card2-1] = cardMap[card2-1]
        # for idx, c in enumerate(copyMap, 1):
        #     if idx%3 == 0:
        #         print(f"{c:^4}")
        #     else:
        #         print(f"{c:^4}", end="")
        mapPrint(copyMap)
        copyMap.clear()

        if cardMap[card1-1] == cardMap[card2-1]:
            userMap[card1-1], userMap[card2-1] = "@", "@"
            print("짝맞추기 성공")
            if userMap.count("@") == 12:
                print("게임이 종료되었습니다!! 축하합니다!!\n")
                global end
                end = True
                return
            userInput = input("\n게임 종료 = 1 / 계속 진행 =  엔터 : ")
        else:
            userInput = input("\n게임 종료 = 1 / 계속 진행 =  엔터 : ")

        if userInput == "1":
            return


        print()

while True:
    if end:
        break
    print("[카드 뒤집기 게임]")
    print("1. 게임 시작")
    print("2. 불러오기")

    if memory:
        print("3. 저장 후 게임 종료")
        print("4. 그냥 게임 종료")
    choice = input("기능 선택 : ")
    if choice == "1":
        wantLevel = int(input("3*4 카드에 나타날 모양의 개수를 입력하세요(2~4) : ")) # 사용자가 원하는 레벨 선택
        userCard = cardShape[:wantLevel]
        # print(userCard)
        eachCardNum = 12//wantLevel

        tempList = []
        for i in userCard:
            for j in range(eachCardNum):
                tempList.append(i)
        # print(tempList)
        random.shuffle(tempList)

        cardMap = tuple(tempList)
        print(cardMap)
        start(cardMap)
    elif choice == "2":
        # {이름 : {ans : cardMap, cur : userMap}}
        nameInput = input("이름을 입력해주세요 : ")
        if nameInput in userDict.keys():
            nowUserDict = userDict[nameInput]
            cardMap = nowUserDict["ans"]
            userMap = list(nowUserDict["cur"])
            start(cardMap)
        else:
            print("찾을 수 없는 사용자입니다.")
    elif choice == "3" and memory:
        nameInput = input("이름을 입력해주세요 : ")
        nowUserDict = {"ans" : cardMap, "cur" : tuple(userMap)}
        userDict[nameInput] = nowUserDict
        print("저장이 완료되었습니다.")
        print(f"사용자 리스트 {userDict.keys()}")
        break
    elif choice == "4" and memory:
        print("게임을 종료합니다")
        break
    else:
        print("지원하지 않는 기능입니다.\n")