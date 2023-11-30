import os
import time
import pygame
import sys
import random
import asyncio

# Khởi tạo Pygame
pygame.init()

# Các hằng số
WIDTH, HEIGHT = 600, 800
OBJECT_WIDTH = 100
OBJECT_HEIGHT = 110
BASKET_SIZE = 150
BASKET_HEIGHT = 150
FPS = 60
MAX_TIME = 15

# Load hình ảnh trái cây
fruit_images = [
    pygame.image.load(os.path.join("TP", "TP1.png")),
    pygame.image.load(os.path.join("TP", "TP2.png")),
    pygame.image.load(os.path.join("TP", "TP3.png")),
    pygame.image.load(os.path.join("TP", "TP4.png")),
    pygame.image.load(os.path.join("TP", "TP5.png")),
]

# Load hình ảnh cụm đá
tool_images = [
    pygame.image.load(os.path.join("VPP", "VVP1.png")),
    pygame.image.load(os.path.join("VPP", "VVP2.png")),
    pygame.image.load(os.path.join("VPP", "VVP3.png")),
    pygame.image.load(os.path.join("VPP", "VVP4.png")),
    pygame.image.load(os.path.join("VPP", "VVP5.png")),
]

# load font
font = pygame.font.Font("LeagueSpartan_regular.ttf", 36)

# Màu sắc
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Tạo cửa sổ game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Catcher")

# Tải âm thanh
pygame.mixer.init()
catch_fruits_sound = pygame.mixer.Sound("catch_fruits.ogg")
catch_tools_sound = pygame.mixer.Sound("catch_tools.ogg")


# Khởi tạo âm thanh nền
pygame.mixer.music.load("gamemusic.ogg")
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)

# Load hình nền
background = pygame.image.load(os.path.join("", "smaller_background.jpg"))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load hình ảnh rổ
basket_image = pygame.image.load(os.path.join("", "MASCOT.png"))
basket_image = pygame.transform.scale(basket_image, (BASKET_SIZE, BASKET_HEIGHT))

# Hàm vẽ rổ
def draw_basket(x):
    screen.blit(basket_image, (x, HEIGHT - 170))


# vẽ vật thể rơi
def draw_object(obj):
    x, y, object_type, img = obj
    if object_type == "fruit":
        image = fruit_images[img]
        image = pygame.transform.scale(image, (OBJECT_WIDTH, OBJECT_HEIGHT))
    elif object_type == "tool":
        image = tool_images[img]
        image = pygame.transform.scale(image, (OBJECT_WIDTH, OBJECT_HEIGHT))
    screen.blit(image, (x, y))


# Hàm vẽ điểm số và thời gian
def draw_info(score, time):
    # Format the score to always display in two digits
    formatted_score = str(score).zfill(2)
    score_text = font.render("Score", True, "#FF5A35")

    # Format the time to always display in two digits
    formatted_time = str(int(time)).zfill(2)
    time_text = font.render("Time", True, "#FF5A35")

    # Calculate positions to center and justify
    total_width = (
        max(
            score_text.get_width(),
            font.size(formatted_score)[0],
            time_text.get_width(),
            font.size(formatted_time)[0],
        )
        + 100
    )
    start_x = (WIDTH / 2) // 2

    score_x = WIDTH // 5
    score_y = 20

    time_x = score_x + total_width
    time_y = 20

    screen.blit(
        score_text, (score_x + (total_width - score_text.get_width()) // 2, score_y)
    )
    screen.blit(
        font.render(formatted_score, True, "#231F20"),
        (score_x + (total_width - font.size(formatted_score)[0]) // 2, score_y + 40),
    )  # Added 40 for vertical spacing
    screen.blit(
        time_text, (time_x + (total_width - time_text.get_width()) // 2, time_y)
    )
    screen.blit(
        font.render(formatted_time, True, "#231F20"), (time_x + 70, time_y + 40)
    )  # Added 40 for vertical spacing

# Start screen
def start_screen():
    # pygame.mouse.set_visible(100)
    play_button = pygame.image.load(os.path.join("", "play_button.png"))
    play_button = pygame.transform.scale(play_button, (250, 78))
    play_button_rect = play_button.get_rect(center=(WIDTH // 2, HEIGHT // 2))

     # draw background start screen
    screen.blit(background, (0, 0))

        # Draw the play button
    screen.blit(play_button, play_button_rect.topleft)
    pygame.display.update()
    
    start_screen_running = True
    while start_screen_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button_rect.collidepoint(event.pos):
                    start_screen_running = False
                    return True
                    



# Hàm vẽ bảng kết thúc
def draw_end_screen(score):
    # Mouse visible
    # pygame.mouse.set_visible(100)
   
    # set board
    # x, y, widht, height
    score_board = pygame.Rect(WIDTH // 4, HEIGHT // 3, 300, 200)
    pygame.draw.rect(screen, "#37383B", score_board)
    
    # Score text
    score_text_font = pygame.font.Font("LeagueSpartan_regular.ttf", 96)
    final_score = score_text_font.render(f"{score}", True, WHITE)
    if (score < 10):
        final_score = score_text_font.render(f"0{score}", True, WHITE)  
    screen.blit(final_score, (WIDTH // 3 + 45, HEIGHT // 3 + 65))
    
     # Set score board top img
    score_top_img = pygame.image.load(os.path.join("", "Score_top.png"))
    score_top_img = pygame.transform.scale(score_top_img, (200, 66))
    score_top_img = pygame.transform.rotate(score_top_img, (3))
    screen.blit(score_top_img, (WIDTH // 5, HEIGHT // 2 - 180))
    
    # Draw Replay button
    replay_button = pygame.image.load(os.path.join("", "GAME_OVER.png")) # Hot fix to game over instead of replaying
    replay_button = pygame.transform.scale(replay_button, (200, 125))
    replay_button_rect = replay_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    screen.blit(replay_button, (WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50))
    
    pygame.display.update()
    
    # Wait for user input
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()
    #         elif event.type == pygame.MOUSEBUTTONDOWN:
    #             if replay_button_rect.collidepoint(event.pos):
    #                 return True  # Replay button clicked


# Hàm chơi lại
def replay():
    clock = pygame.time.Clock()
    # pygame.mouse.set_visible(0)
    return main()

# Hàm chính
async def main():
    clock = pygame.time.Clock()

    basket_x = WIDTH // 2 - BASKET_SIZE // 2
    score = 0
    time_left = MAX_TIME

    # Danh sách đối tượng (trái cây và cục đá)
    max_objects = 3
    objects = []

    game_over = False

    running = True
    while running:
        screen.blit(background, (0, 0))
        # pygame.mouse.set_visible(0)
        # Tạo trái cây hoặc tool ngẫu nhiên
        if random.randint(0, 100) < 5 and len(objects) < max_objects:
            object_type = random.choice(["fruit", "tool"])
            img = random.randint(0, 4)
            obj = [random.randint(0, WIDTH - OBJECT_WIDTH), 0, object_type, img]
            objects.append(obj)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            # Xử lý sự kiện chuột
            if event.type == pygame.MOUSEMOTION or event.type == pygame.FINGERMOTION:
                basket_x = event.pos[0] - BASKET_SIZE // 2
            # touch screen
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
                basket_x = event.pos[0] - BASKET_SIZE // 2
        # Vẽ và di chuyển trái cây hoặc tool
        for obj in objects:
            obj[1] += 5
            draw_object(obj)
            if (
                HEIGHT - 180 < obj[1] < HEIGHT - 90
                and basket_x < obj[0] < basket_x + BASKET_SIZE - 20
            ):
                objects.remove(obj)
                if obj[2] == "fruit":
                    score += 1
                    catch_fruits_sound.play()
                elif obj[2] == "tool":
                    catch_tools_sound.play()
                    if score > 0:
                        score -= 1
                        
            if obj[1] > HEIGHT:
                objects.remove(obj)
        # Vẽ và di chuyển rổ
        draw_basket(basket_x)
        # Vẽ thông tin
        draw_info(score, time_left)
        # Giảm thời gian
        time_left -= 1 / FPS
        if time_left <= 0:
            draw_end_screen(score)
            time.sleep(15)
            running = False
        pygame.display.update()
        clock.tick(FPS)
        await asyncio.sleep(0)
    
    # Kết thúc game
    # if game_over:
    #     if (draw_end_screen(score)):
    #         replay()


asyncio.run(main())

