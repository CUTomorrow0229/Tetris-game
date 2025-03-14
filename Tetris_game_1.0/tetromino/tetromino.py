from constant import brick_dict

class BrickManager:
    # 初始化
    def __init__(self):
        self.bricks = []
        for i in range(4):
            self.bricks.append([0]*4)
        
        self.bricks_next = []
        for i in range(4):
            self.bricks_next.append([0]*4)
        
        self.bricks_next_object = []
        for i in range(4):
            self.bricks_next_object.append([0]*4)

    # 取得方塊索引
    def getBrickIndex(self, brickId, state):
        brickKey = str(brickId)+str(state)
        return brick_dict[brickKey]

    # 將索引轉換成方塊
    def transformToBricks(self, brickId, state):
        for x in range(4):
            for y in range(4):
                self.bricks[x][y] = 0
     
        p_brick = self.getBrickIndex(brickId, state)
    
        # 轉換
        for i in range(4):        
            bx = int(p_brick[i] % 4)
            by = int(p_brick[i] / 4)
            self.bricks[bx][by] = brickId

    # 判斷方塊可不可以複製到容器中
    def ifCopyToBricksArray(self, container_x, container_y, bricks_array):
        for x in range(4):
            for y in range(4):
               if (self.bricks[x][y] != 0):
                    posX = container_x + x
                    posY = container_y + y
                    if (posX >= 0 and posY >= 0):
                        try:
                            if (bricks_array[posX][posY] != 0):
                                return False
                        except:
                            return False
        return True

    # 複製方塊
    def copyToBricksArray(self, container_x, container_y, bricks_array):
        for x in range(4):
            for y in range(4):
                if (self.bricks[x][y] != 0):
                    posX = container_x + x
                    posY = container_y + y
                    if (posX >= 0 and posY >= 0):
                        bricks_array[posX][posY] = self.bricks[x][y]

    # 下一個方塊
    def updateNextBricks(self, brickId, background_bricks_next):
        for y in range(4):
            for x in range(4):
                self.bricks_next[x][y] = 0

        # 取得方塊索引
        pBrick = self.getBrickIndex(brickId, 0)

        # 將索引轉換成方塊
        for i in range(4):
            bx = int(pBrick[i] % 4)
            by = int(pBrick[i] / 4)
            self.bricks_next[bx][by] = brickId

        # 更新背景
        background_bricks_next.update()

        # 更新方塊
        pos_y = 52
        for y in range(4):
            pos_x = 592
            for x in range(4):
                if(self.bricks_next[x][y] != 0):
                    self.bricks_next_object[x][y].rect[0] = pos_x
                    self.bricks_next_object[x][y].rect[1] = pos_y
                    self.bricks_next_object[x][y].update()
                pos_x = pos_x + 28        
            pos_y = pos_y + 28