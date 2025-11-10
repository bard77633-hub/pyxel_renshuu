import pyxel
import math

WIDTH , HEIGHT = 160, 90 #幅と高さのピクセル数
pyxel.init(WIDTH,HEIGHT,title ="Squash")

TITLE,PLAY,OVER = 0,1,2 #画面遷移用の定数
scene = TITLE #現在のシーン
timer = 0 # 時間の管理
pyxel.sounds[0].set("c1e1g1b1","P","7756","V",5)#効果音
#BAR_COL = [7,11,3]#バーの色

score = 0 #　スコア
hisco = 100 #ハイスコア

#バーを動かすための変数と関数
#bar_x = 5
#bar_y = HEIGHT /2
#bar_width = 20 #バーの幅

#def move_bar(): #キー操作で動かす
#    global bar_y
#    if pyxel.btn(pyxel.KEY_UP): #↑キー
#        bar_y = bar_y - 3
#        if bar_y < bar_width / 2 :
#            bar_y = bar_width / 2
#    if pyxel.btn(pyxel.KEY_DOWN): #↓キー
#        bar_y = bar_y + 3
#        if bar_y > HEIGHT - bar_width / 2 :
#            bar_y = HEIGHT - bar_width / 2

#　ボールを動かすための変数と関数
ball_x = 60
ball_y = 40
ball_vx = 2
ball_vy = 1
ball_r = 3 #ボールの半径
BODY_MAX = 50
body = [0][0] * BODY_MAX
hit_count = 0

def move_ball(): #ボールを動かす
    global ball_x, ball_y, ball_vx ,ball_vy
    ball_x = ball_x + ball_vx
    ball_y = ball_y + ball_vy
    if pyxel.btn(pyxel.KEY_UP) and ball_vy > -2 : #↑キー　上加速
        ball_vy -= pyxel.rndf(0.1,0.3)
    if pyxel.btn(pyxel.KEY_DOWN) and ball_vy < 2 : #↓キー 下加速
        ball_vy += pyxel.rndf(0.1,0.3)
    if pyxel.btn(pyxel.KEY_LEFT) and ball_vx > - 2: #←キー　←加速
        ball_vx -= pyxel.rndf(0.1,0.3)
    if pyxel.btn(pyxel.KEY_RIGHT) and ball_vx < 2: #➡キー ➡加速
        ball_vx += pyxel.rndf(0.1,0.3)
        
    if ball_x <= ball_r: #左端
        ball_vx = -ball_vx
        ball_x = ball_r
    if ball_x >= WIDTH - ball_r: #右端
        ball_vx = -ball_vx
        ball_x = WIDTH-ball_r
    if ball_y <= ball_r: #上端
        ball_vy = -ball_vy
        ball_y = ball_r
    if ball_y >= HEIGHT - ball_r: #下端
        ball_vy = -ball_vy
        ball_y = HEIGHT - ball_r

    
point_target_x = 60
point_target_y = 50
point_target_col = 9
point_target_r = 2

#def move_point_target(): #得点ターゲットを出す
#    global point_target_x, point_target_y

def draw_point_target():
        pyxel.circ(point_target_x, point_target_y , point_target_r , point_target_col) #ターゲット
        pyxel.circ(point_target_x- point_target_r / 3 , point_target_y - point_target_r / 3 , point_target_r / 2 -1 , 14)
        pyxel.rect(point_target_x- point_target_r / 3 , point_target_y - point_target_r / 3 ,1,1,7)

#敵ターゲットの変数
ENEMY_MAX = 50
enemy_flag = [False] * ENEMY_MAX

enemy_target_x = [60] * ENEMY_MAX #60
enemy_target_y = [50] * ENEMY_MAX #50
enemy_target_vx = [1] * ENEMY_MAX #-1
enemy_target_vy = [1] * ENEMY_MAX #1
enemy_target_r = 2 #ボールの半径
enemy_target_col = 1
enemy_dist = [10000] * ENEMY_MAX #
def move_enemy_target(): #敵ターゲットを出す
#    global enemy_target_x, enemy_target_y, enemy_target_vx ,enemy_target_vy
    for i in range( ENEMY_MAX ):
        if enemy_flag[i] == False: continue
        enemy_target_x[i] = enemy_target_x[i] + enemy_target_vx[i]
        enemy_target_y[i] = enemy_target_y[i] + enemy_target_vy[i]

        if enemy_target_x[i] <= enemy_target_r: #左端
            enemy_target_vx[i] = -enemy_target_vx[i]
        if enemy_target_x[i] >= WIDTH - enemy_target_r: #右端
            enemy_target_vx[i] = -enemy_target_vx[i]
        if enemy_target_y[i] <= enemy_target_r: #上端
            enemy_target_vy[i] = -enemy_target_vy[i]
        if enemy_target_y[i] >= HEIGHT - enemy_target_r: #下端
            enemy_target_vy[i] = -enemy_target_vy[i]

def draw_enemy_target():  #ターゲットの描画
    for i in range( ENEMY_MAX ):
        if enemy_flag[i] == False: continue
        pyxel.circ(enemy_target_x[i],  enemy_target_y[i] , enemy_target_r +1, 13) 
        pyxel.circ(enemy_target_x[i],  enemy_target_y[i] , enemy_target_r , enemy_target_col) #ターゲット
        pyxel.circ(enemy_target_x[i] - enemy_target_r / 3 , enemy_target_y[i] - enemy_target_r / 3 , enemy_target_r / 2 -1 , 14)
        pyxel.rect(enemy_target_x[i] - enemy_target_r / 3 , enemy_target_y[i] - enemy_target_r / 3 ,1,1,7)



def hit_check(): #ヒットチェック
    #global enemy_target_x, enemy_target_y, enemy_target_vx, enemy_target_vy ,
    global ball_x, ball_y, ball_vx, ball_vy,enemy_target_col
    global point_target_x, point_target_y, point_target_col
    global score,hisco,hit_count,scene
    point_dist = math.sqrt((ball_x - point_target_x) ** 2 + ( ball_y - point_target_y ) **2 )

    for i in range( ENEMY_MAX ):
        if enemy_flag[i] == False: continue
        enemy_dist[i] = math.sqrt((ball_x - enemy_target_x[i]) ** 2 + ( ball_y - enemy_target_y[i] ) **2 )
        if enemy_dist[i] <= ball_r + enemy_target_r:
            hit_count += 1
            pyxel.play(0,0)#効果音出力
            scene = OVER  #ゲームオーバーにすぐします
            timer = 350

        
    if point_dist <= ball_r + point_target_r:
        score = score +10
        hit_count += 1
        pyxel.play(0,0)#効果音出力
        if score > hisco:
            hisco = score
        point_target_x = pyxel.rndi(10,110)
        point_target_y = pyxel.rndi(10,70)

        if hit_count % 5 == 0 :
            enemy_flag[hit_count // 5] = True

        
#        point_target_vx = -point_target_vx
#        point_target_vy = -point_target_vy
#        point_target_col = pyxel.rndi(9,12)

                
#        enemy_target_x = pyxel.rndi(10,110)
#        enemy_target_y = pyxel.rndi(10,70)

        
#        enemy_target_vx = -enemy_target_vx
#        enemy_target_vy = -enemy_target_vy

    

def update(): #メイン処理（計算、判定を行う）
    global scene,timer,score,hisco,hit_count
#    global enemy_target_x, enemy_target_y,
    global ball_x, ball_y, ball_vx, ball_vy

    if scene == TITLE : #タイトル
        if pyxel.btnp(pyxel.KEY_SPACE): #スペースキーで開始
            scene = PLAY
            score = 0
            ball_x = WIDTH // 2
            ball_y = HEIGHT // 5
            ball_vx = 2
            ball_vy = 1
            hit_count = 0
            for i in range(ENEMY_MAX):
                enemy_flag[i] = False
            
    if scene == PLAY: #ゲームプレイ
        move_ball()
        move_enemy_target()
        
        hit_check()
#        move_bar()

        #ヒットチェック

            
                           
 #           if -2 <= dy <= 2:
 #               ball_vx = -ball_vx
 #               if score > 1000:
  #                  if  ball_vy > 0:
   #                     ball_vy = ball_vy + pyxel.rndf(0.1,0.2)
    #                else:
     #                   ball_vy = ball_vy - pyxel.rndf(0.1,0.2)
      #      elif -6 <= dy <= 6:
       #        if  ball_vy > 0:
        #            ball_vy = ball_vy + pyxel.rndf(0.1,0.3)
         #       else:
          #          ball_vy = ball_vy - pyxel.rndf(0.1,0.3)
          #  else:
         #       ball_vx = -ball_vx + pyxel.rndf(0.3,0.45)
         #       if  ball_vy > 0:
         #           ball_vy = ball_vy + pyxel.rndf(0.3,0.45)
         #       else:
        #            ball_vy = ball_vy - pyxel.rndf(0.3,0.45)      
#
 #           if score > hisco:
  #              hisco = score
        
        #if -(bar_width / 2 + ball_r) <= dx <= bar_width / 2 + ball_r and -ball_r <= dy <=0:
         #   ball_vy = pyxel.rndi(-3,-1)
          #  score = score +10
         #   pyxel.play(0,0)#効果音出力




    if scene == OVER: #ゲームオーバー
        timer = timer -1
        if timer == 0 or pyxel.btnp(pyxel.KEY_SPACE):
            scene = TITLE

def draw(): #描画処理
    pyxel.cls(1) #画面のクリア

    if scene == TITLE: #タイトル
        pyxel.text(WIDTH /2 -12 , HEIGHT * 0.3 , "SQUASH",6)
        pyxel.text(WIDTH /2 -26, HEIGHT *0.7, "[SPACE] Start",pyxel.rndi(0,15))

    if scene == PLAY: #ゲームプレイ
        for x in range(0,WIDTH,4):
            pyxel.line(x,0,x,HEIGHT,0)#背景の縦線
        for y in range(0, HEIGHT,4):
            pyxel.line(0,y,WIDTH,y,0)#背景の横線
#        for i in range(3): #バー
#            pyxel.line(bar_x - 1 + i , bar_y - bar_width / 2 ,bar_x - 1 + i  , bar_y + bar_width / 2 , BAR_COL[i])

        #pyxel.rect(bar_x - bar_width / 2 , bar_y , bar_width , 2, 11) #バー 
        pyxel.circ(ball_x, ball_y , ball_r , 8) #ボール
        pyxel.circ(ball_x- ball_r / 3 , ball_y - ball_r / 3 , ball_r / 2 -1 , 14)
        pyxel.rect(ball_x- ball_r / 3 , ball_y - ball_r / 3 ,1,1,7)

        draw_point_target()
        draw_enemy_target()
        
    if scene == OVER: #ゲームオーバー
        pyxel.text(WIDTH /2 -18, HEIGHT *0.3 ,"GAME OVER",8)
        
    pyxel.text(1,1,"SCORE "  + str(score),7)#スコア
    pyxel.text(WIDTH / 2 , 1, "HI-SC " + str(hisco),10) #ハイスコア

pyxel.run(update,draw)
 
