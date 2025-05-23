import random
from constant import brick_down_speed_max

class Game:
    # 初始化
    def __init__(self, brick_manager):
        self.brick_manager = brick_manager
        self.debug_message = False
        self.lines_number_max = 0
        self.score = 0
        self.instructions_mode = True
        self.instruction_page = 1
        self.game_over_screen = False

        # 方塊陣列(10x20)
        self.bricks_array = []
        for i in range(10):
            self.bricks_array.append([0]*20)

        # 方塊陣列(4x4)
        self.bricks = []
        for i in range(4):
            self.bricks.append([0]*4)
    
        self.resetGame()

        self.brick_next_id = random.randint(1, 7)

        self.hold_id = 0
        self.can_hold = True

    # 重製遊戲狀態
    def resetGame(self):
        self.container_x = 3
        self.container_y = -4
        
        self.brick_id = 1
        self.brick_state = 0
        
        self.lines_number = 0
        self.game_mode = 0
        self.game_level = 1
        self.game_over = False
        self.game_over_screen = False
        self.score = 0

        self.brick_down_speed = brick_down_speed_max * (0.9 ** self.game_level)

        self.hold_id = 0
        self.can_hold = True

        self.instructions_mode = True
        self.instruction_page = 1

        # 清除方塊陣列(10x20)
        for x in range(10):
            for y in range(20):
                self.bricks_array[x][y] = 0
            
        # 清除方塊陣列(4x4)
        for x in range(4):
            for y in range(4):
                self.bricks[x][y] = 0

        # 最大連線數
        if(self.lines_number > self.lines_number_max):
            self.lines_number_max = self.lines_number

    # 判斷方塊可不可以消除
    def ifClearBrick(self):
        pointNum = 0
        lineNum = 0
        for y in range(20):
            for x in range(10):
                if (self.bricks_array[x][y] > 0):
                    pointNum = pointNum + 1
                if (pointNum == 10):
                    for i in range(10):
                        lineNum = lineNum + 1
                        self.bricks_array[i][y] = 9
            pointNum = 0
        return lineNum

    # 消除方塊
    def clearBrick(self):
        temp = 0    
        for x in range(10):
            for i in range(19):
                for y in range(20):
                    if (self.bricks_array[x][y] == 9):
                        if (y > 0):
                            temp = self.bricks_array[x][y - 1]
                            self.bricks_array[x][y - 1] = self.bricks_array[x][y]
                            self.bricks_array[x][y] = temp
                            y = y - 1
                self.bricks_array[x][0] = 0

    # 計分
    def calculateScore(self, lines):
        if lines == 1:
            return 1000
        elif lines == 2:
            return 3000
        elif lines == 3:
            return 5000
        elif lines == 4:
            return 8000
        else:
            return 0

    # 生成新方塊
    def brickNew(self):
        # 判斷GameOver
        self.game_over = False
        if not self.instructions_mode and self.container_y < 0:
            self.game_over = True

        # 複製方塊到容器內
        self.container_y = self.container_y - 1
        self.brick_manager.copyToBricksArray(self.container_x, self.container_y, self.bricks_array)  
    
        # 消除方塊和相關參數計算
        lines = self.ifClearBrick() // 10;        
        if (lines > 0):
            if lines > self.lines_number_max:
                self.lines_number_max = lines
            
            self.lines_number = self.lines_number + lines

            self.score += self.calculateScore(lines)

            # 每消10行等級+1
            if self.score >= self.game_level * 10000:
                self.game_level += 1
                self.brick_down_speed = brick_down_speed_max * (0.9 ** self.game_level)
                

            self.game_mode = 1

        # 設定當前、下一個方塊的狀態
        self.container_x = 3
        self.container_y = -4

        self.brick_id = self.brick_next_id

        self.brick_next_id = random.randint(1, 7)
        self.brick_state = 0

        self.can_hold = True

        if (self.game_over and not self.instructions_mode):
            if self.lines_number > self.lines_number_max:
                self.lines_number_max = self.lines_number
            
            self.game_over_screen = True
            self.game_mode = 2

    # 重新開始遊戲
    def restartGame(self):
        old_max = self.lines_number_max
        self.resetGame()
        self.lines_number_max = old_max
        self.instructions_mode = False
        self.game_over_screen = False

    # Hold功能處理
    def holdBrick(self):
        if not self.can_hold:
            return
        
        # 第一次用
        if self.hold_id == 0:
            self.hold_id = self.brick_id
            self.brick_id = self.brick_next_id
            self.brick_next_id = random.randint(1, 7)
        # 第二次以上
        else:
            temp = self.brick_id
            self.brick_id = self.hold_id
            self.hold_id = temp

        # 重製方塊
        self.container_x = 3
        self.container_y = -4
        self.brick_state = 0

        self.brick_manager.transformToBricks(self.brick_id, self.brick_state)

        self.can_hold = False
