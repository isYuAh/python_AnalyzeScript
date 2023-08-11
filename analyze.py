import time


class Script:
    def __init__(self, scriptName):
        self.filename = f"./scripts/{scriptName}.txt"
        self.thisChoice = []

    def close(self):
        self.f.close()

    def readLines(self):
        self.f = open(self.filename, "r", encoding="utf-8")
        self.lines = self.f.read().splitlines()
        self.nowline = 0
        self.nowPart = 0
        self.nowTab = "    " * self.nowPart

    def pushPart(self, pushNumber=1):
        self.nowPart += pushNumber
        self.nowTab = "    " * self.nowPart
        self.ProceedNowPartDescription()

    def ProceedLine(self):
        self.lineToBeProceed = self.lines[self.nowline].removeprefix(self.nowTab)
        # print(f">>>>>DEBUG::{self.lineToBeProceed}")

    def printBasicInfo(self):
        self.ProceedLine()
        if self.CheckHasMeaning():  # 如果不是注释或者空行
            # print(self.nowline)
            # print(self.lineToBeProceed)
            if self.lineToBeProceed[:10] == "##TITLE## ":
                print(f"剧本：{self.lineToBeProceed.removeprefix('##TITLE## ')}")
            elif self.lineToBeProceed[:11] == "##AUTHOR## ":
                print(f"作者：{self.lineToBeProceed.removeprefix('##AUTHOR## ')}")
            elif self.lineToBeProceed[:9] == "##TIME## ":
                print(f"时间：{self.lineToBeProceed.removeprefix('##TIME## ')}")
            elif self.lineToBeProceed[:16] == "##DESCRIPTION## ":
                print(f"描述：{self.lineToBeProceed.removeprefix('##DESCRIPTION## ')}")
            elif self.lineToBeProceed[:9] == "##START##":
                self.nowline += 1
                self.ProceedLine()
                self.MODE = "DESCRIPTION"
                return
        self.nowline += 1
        # print("><<><><><><><>" + self.lineToBeProceed[:9])
        self.ProceedLine()
        self.printBasicInfo()

    def CheckHasMeaning(self):
        return self.lineToBeProceed.strip() != "" and self.lineToBeProceed[:2] != "//"

    def ProceedPartEnd(self):
        print("\n\n----------------------------------")
        for c in self.thisChoice:
            print(f"| {c}")
        print("----------------------------------\n\n")
        choice = self.thisChoice[int(input("请输入选择第几个选项：")) - 1]
        self.MODE = "DESCRIPTION"

        while self.lineToBeProceed[: len(choice) + 1] != f"#{choice}":
            if self.nowline == len(self.lines) - 1:
                print("\n\nERROR: 没有此选项对应的剧情\n\n")
                self.quit()
            self.nowline += 1
            self.ProceedLine()
        self.nowline += 1
        self.ProceedLine()
        self.thisChoice = []
        self.pushPart()

    def ProceedNowPartDescription(self):
        if self.CheckHasMeaning():
            if self.MODE == "DESCRIPTION":
                if (
                    self.lineToBeProceed[:9] != "#CHOICE# "
                    and self.lineToBeProceed[0] != " "
                ):  # 未开始下一部分
                    if self.lineToBeProceed[:10] == "##SLEEP## ":
                        time.sleep(
                            float(self.lineToBeProceed.removeprefix("##SLEEP## "))
                        )
                    elif self.lineToBeProceed[:10] == "##ENDING##":
                        self.MODE = "ENDING"
                    else:
                        print(self.lineToBeProceed)
                elif (
                    self.lineToBeProceed[:9] == "#CHOICE# "
                    and self.lines[self.nowline][: 4 * self.nowPart] == self.nowTab
                ):
                    self.MODE = "CHOICE"
                    self.thisChoice.append(
                        self.lineToBeProceed.removeprefix("#CHOICE# ")
                    )
                else:
                    if self.MODE == "ENDING":
                        self.quit()
            elif self.MODE == "CHOICE":
                if self.lineToBeProceed[:9] == "#CHOICE# ":
                    self.thisChoice.append(
                        self.lineToBeProceed.removeprefix("#CHOICE# ")
                    )
                else:
                    self.ProceedPartEnd()
            elif self.MODE == "ENDING":
                if self.nowline == len(self.lines) - 1:
                    time.sleep(2)
                    print("\n\n----------------------------------")
                    print("游戏结束")
                    print("----------------------------------\n\n")
                    self.quit()
                elif (
                    len(self.lines[self.nowline])
                    - len(self.lines[self.nowline].lstrip())
                    != self.nowPart * 4
                ):
                    time.sleep(2)
                    print("\n\n----------------------------------")
                    print("游戏结束")
                    print("----------------------------------\n\n")
                    self.quit()
                else:
                    print(self.lineToBeProceed)

        self.nowline += 1
        self.ProceedLine()
        self.ProceedNowPartDescription()

    def quit(self):
        self.close()
        quit()


print("----------------------------------")
print("------------ 文字游戏 ------------")
print("------------  BY 芋  ------------")
print("----------------------------------")
print("默认剧本:default")

script = input("输入剧本名称(只需要输入scripts目录下的文件名即可，无需扩展名)：")

S = Script(script)
S.readLines()

print("\n\n----------------------------------")
S.printBasicInfo()
print("----------------------------------\n\n")
S.ProceedNowPartDescription()


S.close()
