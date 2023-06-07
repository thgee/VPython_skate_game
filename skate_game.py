Web VPython 3.2

import random as rand

# ------------ 변수 ----------------
speed = 5 # 이동속도
jump = 1.2 # 점프력

is_gameover = False
mode = 1 # 0:정지 1:달리기 2:점프
t = 0
dt = 0.01
g = 9.8 # 중력가속도
mu = 0.5 # 마찰계수
e  = 1.0 # 반발계수

camera_type = 1 # 1: 카메라가 y좌표계로 움직이지않음 2: 점프시 카메라가 플레이어를 따라 움직임




# ------------ 환경설정 ------------ 
scene = canvas(title = '스케이트 게임', width=1000, height=500, background=vec(0.8, 0.7, 0.6))
scene.camera.pos = vec(0.56, 2.44, -1)
scene.camera.axis = vector(-0.56, -1.44, -1.43)
scene.camera.forward = vector(0, 0, -100)
scene.camera.v = vec(0, 0, -speed)
scene.camera.a = vec(0, 0, 0)
distant_light(direction=vector( 0,  1,  0), color=vec(0.9, 0.7, 0.8))


# ------------ Player ------------ 
# player의 몸체
body = sphere(pos=vector(0, 0, 0), radius=0.1)

# player의 귀
left_ear = cone(pos=vector(-0.08, 0.08, 0), axis=vector(0.04, 0, 0), radius=0.03)
right_ear = cone(pos=vector(0.08, 0.08, 0), axis=vector(-0.04, 0, 0), radius=0.03)

# player의 팔과 다리
left_arm = cylinder(pos=vector(-0.1, 0, 0), axis=vector(-0.02, 0, 0), radius=0.02)
right_arm = cylinder(pos=vector(0.1, 0, 0), axis=vector(0.02, 0, 0), radius=0.02)
left_leg = cylinder(pos=vector(-0.05, -0.08, 0), axis=vector(-0.04, -0.08, 0), radius=0.02, make_trail = True)
right_leg = cylinder(pos=vector(0.05, -0.08, 0), axis=vector(0.04, -0.08, 0), radius=0.02)

# player의 눈
left_eye = sphere(pos=vector(-0.03, 0.03, -0.08), radius=0.03, color=color.black)
right_eye = sphere(pos=vector(0.03, 0.03, -0.08), radius=0.03, color=color.black)

# player의 입
mouth = pyramid(pos=vector(0, -0.03, -0.08), size=vector(0.06, 0.02, 0.02), axis = vec(0, 0, -1),color=color.red)

# player를 하나의 객체로 묶음
player = compound([body, left_ear, right_ear, left_arm, right_arm, left_leg, right_leg, left_eye, right_eye, mouth],
                   color=color.yellow, size = vec(0.3, 0.3, 0.3), pos=vector(0, 0.05, -2.5), v=vector(0, 0, -speed), 
                   make_trail = False, trail_radius = 0.05, trail_color = vec(0.2, 0.4, 1),
                   mass = 3, a = vec(0, 0, 0))


# ------------- 아이템 -----------------
items = []
for i in range(1, 100):
    items.append(sphere(pos = vec(rand.uniform(-4, 2) ,0.9 ,-i * 20 - 4), radius = 0.2, color = vec(0.45, 0.49,1), type = 1))
    items.append(sphere(pos = vec(rand.uniform(-4, 2) ,0.9 ,-i * 20 + 3), radius = 0.2, color = vec(0.47, 1,0.37), type = 2))
    items.append(sphere(pos = vec(rand.uniform(-4, 2) ,0.9 ,-i * 20 + 10), radius = 0.2, texture = textures.stucco, type = 3))

item = 0 # 1: 브레이크 강화 아이템 2: 점프력 강화 아이템 3: 위성 아이템
item_time = 0 # 아이템 지속시간
             


# ------------ 위성 ------------ 
balls = []
for i in range(4):
    balls.append(sphere(pos = vec(10, 0, 0), radius = 0.1 , texture = textures.stucco, mass = 5, a = vec(0, 0, 0), v = vec(0, 0, 0)))
ball_mode = 0 # 아이템 3을 먹는순간 위성의 위치를 초기화한 후 ball_mode = 1로 바뀜


# ------------ 장애물 and 벽 ------------ 

obstacle = []  
for i in range(200):
    
    # 장애물
    obstacle.append(box(pos = vec(round(rand.uniform(-5, 2.5)), 0, -i * 1 - 10), size = vec(0.3 * (round(rand.uniform(1, 10)) % 3+ 1),0.3 * (round(rand.uniform(1, 100)) % 2 + 1),0.3), v = vec(0, 0, 0), mass = 1))
    obstacle.append(box(pos = vec(round(rand.uniform(-5, 2.5)), 0, -i * 2 - 10), size = vec(0.3 * (round(rand.uniform(1, 10)) % 3+ 1),0.3 * (round(rand.uniform(1, 100)) % 2 + 1),0.3), v = vec(0, 0, 0), mass = 1))
    obstacle.append(box(pos = vec(round(rand.uniform(-5, 2.5)), 0, -i * 3 - 10), size = vec(0.3 * (round(rand.uniform(1, 10)) % 3+ 1),0.3 * (round(rand.uniform(1, 100)) % 2 + 1),0.3), v = vec(0, 0, 0), mass = 1))

    # 벽
    wall_left = box(pos = vec(-10, 0, -i*10), size = vec(10.1,1,10), color = color.gray(0.2))
    wall_right = box(pos = vec(7.5, 0, -i*10), size = vec(10.1,1,10), color = color.gray(0.2))
    
    

# ----------------  빙판 ---------------------
floor = box(pos = vec(0, -0.15, -300), size = vec(10, -0.1, 1000), color = vec(0.53, 0.72, 0.86))




# ------------ 힘-----------------
F_gravity = vec(0, 0, 0) # 중력
F_normal = vec(0, 0, 0) # 수직항력
F_jump = vec(0, 0, 0) # 점프할때 바닥에 가하는 힘에 의한 반작용
F_break = vec(0, 0, 0) # 브레이크에 의한 마찰력




# ------------  위성과 장애물 충돌함수 ------------ 
def ball_obstacle_collision (ball, obstacle, e):
    _v = ball.v + player.v
    c = obstacle.pos - ball.pos
     
    v1_c = dot(_v, norm(c)) * norm(c)
    v1_p = _v - v1_c
    v2_c = dot(obstacle.v, norm(c)) * norm(c)
    v2_p = obstacle.v - v2_c
    
    if dot(_v - obstacle.v, norm(c)) < 0: 
        return False
    
    ball_top = ball.pos.y + ball.radius
    ball_bottom = ball.pos.y - ball.radius
    ball_left = ball.pos.x - ball.radius
    ball_right = ball.pos.x + ball.radius
    ball_front = ball.pos.z - ball.radius
    ball_rear = ball.pos.z + ball.radius

    obstacle_top = obstacle.pos.y + obstacle.size.y / 2
    obstacle_bottom = obstacle.pos.y - obstacle.size.y / 2
    obstacle_left = obstacle.pos.x - obstacle.size.x / 2
    obstacle_right = obstacle.pos.x + obstacle.size.x / 2
    obstacle_front = obstacle.pos.z - obstacle.size.z / 2
    obstacle_rear = obstacle.pos.z + obstacle.size.z / 2
    
    if  ball_left < obstacle_right and ball_right > obstacle_left and ball_top > obstacle_bottom and ball_bottom < obstacle_top and ball_front < obstacle_rear and ball_rear > obstacle_front:
        v1 = ((ball.mass - e * obstacle.mass) * v1_c + (1 + e) * obstacle.mass * v2_c) / (ball.mass + obstacle.mass)
        v2 = ((obstacle.mass - e * ball.mass) * v2_c + (1 + e) * ball.mass * v1_c) / (ball.mass + obstacle.mass)
        obstacle.v = v2 + v2_p
        return True
        
    else:
        return False
    
    
# ------------  플레이어와 장애물 충돌함수 ------------ 
def player_obstacle_collision(obstacle):
    global is_gameover

    player_top = player.pos.y + player.size.y / 2
    player_bottom = player.pos.y - player.size.y / 2
    player_left = player.pos.x - player.size.x / 2
    player_right = player.pos.x + player.size.x / 2
    player_front = player.pos.z - player.size.z / 2
    player_rear = player.pos.z + player.size.z / 2

    obstacle_top = obstacle.pos.y + obstacle.size.y / 2
    obstacle_bottom = obstacle.pos.y - obstacle.size.y / 2
    obstacle_left = obstacle.pos.x - obstacle.size.x / 2
    obstacle_right = obstacle.pos.x + obstacle.size.x / 2
    obstacle_front = obstacle.pos.z - obstacle.size.z / 2
    obstacle_rear = obstacle.pos.z + obstacle.size.z / 2
    
    if  player_left < obstacle_right and player_right > obstacle_left and player_top > obstacle_bottom and player_bottom < obstacle_top and player_front < obstacle_rear and player_rear > obstacle_front:
        text(pos = vec(-0.2,0.5, player.pos.z), text='Game Over', align='center', color=color.red, billboard = True, height = 0.5)
        is_gameover = True


# ------------ 아이템 획득 함수 -----------------
def get_item(item):
    
    if mag(player.pos - item.pos) <= item.radius + player.size.x: # 아이템과 충돌시
        item.radius = 0
        return item.type
    else:
        return 0
        
        



keysdown = set()

def handle_key(event):
    key = event.key
    keysdown.add(key)

def handle_keyup(event):
    key = event.key
    keysdown.remove(key)

def handle_keys():
    
    if is_gameover: 
        return

    # 벽을 넘어가지 못하게 함
    if player.pos.x >= 2.3 - player.size.x / 2 :
        player.pos.x -= 0.2
        for ball in balls:
            ball.pos.x -= 0.2
    else if player.pos.x <= -4.7 + player.size.x / 2 :
        player.pos.x += 0.2
        for ball in balls:
            ball.pos.x += 0.2
    
   
      
    
    if 'up' in keysdown:
        if player.v.y == 0 and mode == 1:
            global F_jump
            global mode
            mode = 2
            
            # 운동량을 이용하여 점프직후의 속도를 구함
            #  점프는 0.1초동안 한다고 가정
            F_jump = vec(0, jump, 0)
            player.v += F_jump / 0.1 / player.mass # f = pt, p = mv -> f = mvt
            
            if item == 2: # 점프력 강화시 카메라 위치도 함께 올라감
                camera_type = 2
                scene.camera.v += F_jump / 0.1 / player.mass        


    if 'left' in keysdown:
        player.pos -= vec(0.05, 0, 0)
        for ball in balls:
            ball.pos -= vec(0.05, 0, 0)

    if 'right' in keysdown:
        player.pos += vec(0.05, 0, 0)
        for ball in balls:
            ball.pos += vec(0.05, 0, 0)

    if ' ' in keysdown:
        if player.v.z >= 0.01 : 
            return
        
        if mode == 2: # 점프중에는 브레이크를 할 수 없도록 함
            return
        
        # 스키드마크
        player.make_trail=True
        
        # 플레이어의 모드 변경
        global mode
        player.axis = vec(0, 0, 1)
        mode = 0 # 정지모드로 변경

def handle_keyup_space(event):
    if event.key == ' ' and mode == 0:
        
        # 마찰력을 없애주고 기존속도로 돌아감
        global F_break
        F_break = vec(0, 0,0)
        player.v = vec(0, 0, -speed)
        scene.camera.v = vec(0, 0, -speed)
            
        # 달리기모드로 변경
        global mode
        if mode == 0:
            player.axis = vec(1, 0, 0)
            mode = 1 # 달리기모드로 변경
    
        # 스키드마크 해제
        player.make_trail=False

scene.bind('keydown', handle_key)
scene.bind('keyup', handle_keyup)
scene.bind('keyup', handle_keyup_space)




# ------------- 게임시작 ---------------
while True:
    
    # FPS
    rate(1 / dt)

    handle_keys()

    
    # 달리기 모션
    if mode == 1:
        if player.pos.z % 0.8 <= -0.4:
            player.rotate(angle=radians(-10), axis=vec(0, 1, 0))
        else:
            player.rotate(angle=radians(10), axis=vec(0, 1, 0))
    

        
    #  힘 상호작용 계산 
    
    # 중력
    F_gravity = vec(0, -player.mass * g, 0)
    
    # 빙판에서 달리고있는 경우 수직항력 작용
    F_normal = vec(0, 0, 0)
    if player.pos.y <= 0.05:
        F_normal = -F_gravity
    
    
    # 점프 후 바닥에 착지할때
    if mode == 2 and player.pos.y <= 0.049:
        player.v.y = 0 # 착지하면서 속도는 0이되고 운동에너지는 소멸됨
        player.pos.y = 0.05
        scene.camera.v.y = 0
        player.axis=vec(1, 0, 0) # 플레이어가 정면을 보게함
        mode = 1
        
        if item == -1:
            camera_type = 1
            item = 0
            scene.camera.v.y = 0
            
        if camera_type == 1 and item == 2:
            camera_type = 2
            
        
    # 마찰력으로 브레이크 처리
    if mode == 0:
        F_break = vec(0, 0, mu * player.mass * g) # Fk = mu * N
        if player.v.z >= 0:
            player.v.z = 0
            scene.camera.v.z = 0
            F_break = vec(0, 0, 0)
            
        
    # 힘의 합
    F_sum = F_gravity + F_normal + F_break
    
    
    
    
    
#     플레이어 위치 업데이트
    player.a = F_sum / player.mass
    player.v += player.a * dt
    player.pos += player.v * dt
    
    # 카메라 위치 업데이트
    if camera_type == 2:
        scene.camera.a = F_sum / player.mass
    else:
        scene.camera.a = F_break / player.mass
    scene.camera.v += scene.camera.a * dt
    scene.camera.pos += scene.camera.v * dt
    
    
    
    # 위성과 장애물의 충돌검사 and 장애물 위치 업데이트
    for ball in balls:
        for ob in obstacle:
            ball_obstacle_collision(ball, ob, e)    
            ob.pos +=  ob.v * dt

        # 위성의 위치 업데이트
        # 아이템 지속시간 동안위성이 플레이어 주변을 등속 원운동 하도록 구현
        ball.pos += player.v * dt
        if ball_mode == 1:
            ball.a = mag(ball.v) ** 2 / mag(player.pos - ball.pos) * norm(player.pos -ball.pos)
        ball.v += ball.a * dt
        ball.pos += ball.v * dt 
    
    
    # 아이템획득
    for i in items:
        if item == 0:
            item = get_item(i)
    
    if item > 0: # 아이템을 획득했다면
    
        for i in items: # 아이템 하나를 먹으면 다른 아이템들은 보이지 않도록 처리
            i.radius = 0
    
        item_time += dt # 지속시간이 흐르기 시작
    
        if item == 1: 
            mu = 1.8 # 마찰계수 증가
            player.color = vec(0.45, 0.49,1)
            
        else if item == 2:
            player.color = vec(0.47, 1,0.37)
            jump = 3
            
            
        else if item == 3:
            
            
            #  위성아이템 획득 순간 위성의 위치와 속도 초기화
                
                
            if ball_mode == 0:
                balls[0].pos = vec(0.5, -0.05, 0) + player.pos
                balls[1].pos = vec(0, -0.05, -0.5) + player.pos
                balls[2].pos = vec(-0.5, -0.05, 0) + player.pos
                balls[3].pos = vec(0, -0.05, 0.5) + player.pos
                
                balls[0].v = vec(0, 0, -6)
                balls[1].v = vec(-6, 0, 0)
                balls[2].v = vec(0, 0, 6)
                balls[3].v = vec(6, 0, 0)
                
                
                ball_mode = 1
                
        
        
    if item_time >= 3: # 아이템 지속시간이 끝나면
        
        for i in items: # 아이템들이 원래 크기로 돌아옴
            i.radius = 0.2
        player.color = color.yellow
        
        item_time = 0
        
        if item == 1:
            mu = 0.5 # 마찰계수가 원래대로 돌아옴
            item = 0
            
        else if item == 2:
            jump = 1.2 # 점프력이 원래대로 돌아옴
            item = -1
            
            if mode != 2: # 점프력 강화 지속시간이 끝났을 시점에 달리고 있었다면
                camera_type = 1
                item = 0
            
            
        else if item == 3:
            item = 0
            ball_mode = 2
            
            
    # 위성아이템의 지속시간이 끝난 직후
    if ball_mode == 2:
        for ball in balls:
            ball.pos *= 1.001
        ball_mode = 0
            

    
    
    # 충돌처리
    for i in obstacle:    
        player_obstacle_collision(i)
        
    # 게임종료
    if is_gameover == True:
        player.rotate(angle=radians(90), axis=vec(1, 0, 0))
        player.color = vec(1, 0.2, 0.2)
        return
    
