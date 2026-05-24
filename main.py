import pygame
import time
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 128, 0)
red = (255, 0, 0)
dis_w = 800
dis_h = 600
dis = pygame.display.set_mode((dis_w, dis_h))

pygame.display.update()
pygame.display.set_caption('змейка')

snake_block = 20
snake_speed = 10
x1 = dis_w/2
y1 = dis_h/2
x1_change = 0
y1_change = 0
clock = pygame.time.Clock()

# Загрузка изображений
apple_img = pygame.image.load('apple.png').convert_alpha()
apple_img = pygame.transform.scale(apple_img, (snake_block, snake_block))

# Загрузка изображений змейки
snake_head_img = pygame.image.load('photo_5231253347896073583_y.png').convert_alpha()
snake_head_img = pygame.transform.scale(snake_head_img, (snake_block, snake_block))

# Загрузка тела змейки
try:
    snake_body_img = pygame.image.load('photo_5210687528359369539_y.png').convert_alpha()
    snake_body_img = pygame.transform.scale(snake_body_img, (snake_block, snake_block))
except:
    snake_body_img = pygame.Surface((snake_block, snake_block), pygame.SRCALPHA)
    pygame.draw.rect(snake_body_img, green, (2, 2, snake_block-4, snake_block-4), border_radius=5)
    print("Файл body.png не найден, используется стандартный прямоугольник")

# ========== СОЗДАНИЕ ФОНА С ЗЕЛЕНОЙ СЕТКОЙ ==========
def create_grid_background(width, height, cell_size):
    """Создает фон с зеленой сеткой"""
    bg = pygame.Surface((width, height))
    bg.fill((0, 30, 0))  # Темно-зеленый фон
    
    # Рисуем зеленую сетку
    grid_color = (0, 100, 0)  # Темно-зеленый для сетки
    for x in range(0, width, cell_size):
        pygame.draw.line(bg, grid_color, (x, 0), (x, height), 1)
    for y in range(0, height, cell_size):
        pygame.draw.line(bg, grid_color, (0, y), (width, y), 1)
    
    return bg

def create_bright_grid_background(width, height, cell_size):
    """Создает фон с яркой зеленой сеткой"""
    bg = pygame.Surface((width, height))
    bg.fill((20, 50, 20))  # Темно-зеленый фон
    
    # Рисуем яркую зеленую сетку
    grid_color = (0, 200, 0)  # Ярко-зеленый
    for x in range(0, width, cell_size):
        pygame.draw.line(bg, grid_color, (x, 0), (x, height), 2)
    for y in range(0, height, cell_size):
        pygame.draw.line(bg, grid_color, (0, y), (width, y), 2)
    
    return bg

def create_neon_grid_background(width, height, cell_size):
    """Создает фон с неоновой зеленой сеткой"""
    bg = pygame.Surface((width, height))
    bg.fill((0, 20, 0))  # Очень темный фон
    
    # Рисуем неоновую сетку с эффектом свечения
    grid_color = (50, 255, 50)  # Неоново-зеленый
    for x in range(0, width, cell_size):
        pygame.draw.line(bg, grid_color, (x, 0), (x, height), 1)
        # Эффект свечения (более толстая, но полупрозрачная линия)
        pygame.draw.line(bg, (0, 255, 0, 50), (x-1, 0), (x-1, height), 1)
        pygame.draw.line(bg, (0, 255, 0, 50), (x+1, 0), (x+1, height), 1)
    
    for y in range(0, height, cell_size):
        pygame.draw.line(bg, grid_color, (0, y), (width, y), 1)
        pygame.draw.line(bg, (0, 255, 0, 50), (0, y-1), (width, y-1), 1)
        pygame.draw.line(bg, (0, 255, 0, 50), (0, y+1), (width, y+1), 1)
    
    return bg

def create_cell_background(width, height, cell_size):
    """Создает фон с закрашенными клетками (шахматная доска)"""
    bg = pygame.Surface((width, height))
    
    # Чередующиеся зеленые клетки
    colors = [(30, 80, 30), (20, 60, 20)]  # Темно-зеленые цвета
    
    for row in range(height // cell_size + 1):
        for col in range(width // cell_size + 1):
            color = colors[(row + col) % 2]
            pygame.draw.rect(bg, color, (col * cell_size, row * cell_size, cell_size, cell_size))
    
    # Добавляем границы клеток
    border_color = (0, 150, 0)
    for x in range(0, width, cell_size):
        pygame.draw.line(bg, border_color, (x, 0), (x, height), 1)
    for y in range(0, height, cell_size):
        pygame.draw.line(bg, border_color, (0, y), (width, y), 1)
    
    return bg

# ВЫБЕРИТЕ ОДИН ИЗ ВАРИАНТОВ (раскомментируйте нужный):
background = create_grid_background(dis_w, dis_h, snake_block)  # Обычная зеленая сетка
# background = create_bright_grid_background(dis_w, dis_h, snake_block)  # Яркая зеленая сетка
# background = create_neon_grid_background(dis_w, dis_h, snake_block)  # Неоновая зеленая сетка
# background = create_cell_background(dis_w, dis_h, snake_block)  # Закрашенные клетки

foodx = round(random.randrange(0, dis_w - snake_block) / snake_block) * snake_block
foody = round(random.randrange(0, dis_h - snake_block) / snake_block) * snake_block

snake_L = []
len_of_snake = 1

font_style = pygame.font.SysFont(None, 50)
victory_font = pygame.font.SysFont(None, 80)  # Шрифт для победы

# Функция для поворота головы с сохранением качества
def rotate_head(image, direction_x, direction_y):
    """Поворачивает голову в зависимости от направления движения"""
    if direction_x > 0:  # вправо
        return pygame.transform.rotate(image, -180)
    elif direction_x < 0:  # влево
        return pygame.transform.rotate(image, 0)
    elif direction_y > 0:  # вниз
        return pygame.transform.rotate(image, 90)
    elif direction_y < 0:  # вверх
        return pygame.transform.rotate(image, -90)
    return image  # если не движется

def our_snake(snake_block, snake_list):
    for i, segment in enumerate(snake_list):
        if i == len(snake_list) - 1:  # Голова
            # Поворачиваем голову в зависимости от глобального направления
            rotated_head = rotate_head(snake_head_img, x1_change, y1_change)
            dis.blit(rotated_head, (segment[0], segment[1]))
        else:  # Тело
            dis.blit(snake_body_img, (segment[0], segment[1]))

def messages(msg, color, font=None, y_offset=0):
    if font is None:
        mesg = font_style.render(msg, True, color)
    else:
        mesg = font.render(msg, True, color)
    
    # Полупрозрачный фон для сообщения
    text_rect = mesg.get_rect(center=(dis_w/2, dis_h/2 + y_offset))
    pygame.draw.rect(dis, (0, 0, 0, 180), text_rect.inflate(30, 20))
    dis.blit(mesg, text_rect)

def show_score():
    """Отображает текущий счет на экране"""
    score_font = pygame.font.SysFont(None, 35)
    score_text = score_font.render(f"Счёт: {len_of_snake - 1} / 5", True, white)
    # Добавляем полупрозрачный фон для счета
    text_rect = score_text.get_rect(topleft=(10, 10))
    pygame.draw.rect(dis, (0, 0, 0, 100), text_rect.inflate(10, 5))
    dis.blit(score_text, (10, 10))

game_over = False
victory = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and x1_change == 0:
                x1_change = -snake_block
                y1_change = 0
            elif event.key == pygame.K_RIGHT and x1_change == 0:
                x1_change = snake_block
                y1_change = 0
            elif event.key == pygame.K_UP and y1_change == 0:
                x1_change = 0
                y1_change = -snake_block
            elif event.key == pygame.K_DOWN and y1_change == 0:
                x1_change = 0
                y1_change = snake_block
                
    # Проверка столкновения со стенами
    if x1 >= dis_w or x1 < 0 or y1 >= dis_h or y1 < 0:
        game_over = True
        
    x1 += x1_change
    y1 += y1_change
    
    # ОТРИСОВКА ФОНА С ЗЕЛЕНОЙ СЕТКОЙ
    dis.blit(background, (0, 0))
    
    # Рисуем еду
    dis.blit(apple_img, (foodx, foody))
    
    snake_Head = [x1, y1]
    snake_L.append(snake_Head)
    
    if len(snake_L) > len_of_snake:
        del snake_L[0]
    
    # Проверка столкновения с хвостом
    for segment in snake_L[:-1]:
        if segment == snake_Head:
            game_over = True
    
    our_snake(snake_block, snake_L)
    show_score()  # Показываем счет
    
    # Проверка поедания еды
    if x1 == foodx and y1 == foody:
        foodx = round(random.randrange(0, dis_w - snake_block) / snake_block) * snake_block
        foody = round(random.randrange(0, dis_h - snake_block) / snake_block) * snake_block
        len_of_snake += 1
        
        # ПРОВЕРКА НА ПОБЕДУ (5 яблок)
        if len_of_snake - 1 >= 5:  # -1 потому что начальная длина 1
            victory = True
            game_over = True
        
        # Визуальный эффект при съедании
        dis.blit(apple_img, (foodx, foody))
        pygame.display.update()
        time.sleep(0.05)
    
    pygame.display.update()
    clock.tick(snake_speed)

# ПОКАЗЫВАЕМ СООБЩЕНИЕ О РЕЗУЛЬТАТЕ
if victory:
    # Анимация победы (мигающий фон)
    for _ in range(3):
        dis.fill((0, 255, 0, 100))  # Зеленый фон
        pygame.display.update()
        time.sleep(0.2)
        dis.blit(background, (0, 0))
        our_snake(snake_block, snake_L)
        show_score()
        pygame.display.update()
        time.sleep(0.2)
    
    # Показываем сообщение о победе
    messages("ПОБЕДА!", (0, 255, 0), victory_font, -30)
    messages(f"Вы съели {len_of_snake - 1} яблок!", white, font_style, 30)
    pygame.display.update()
    time.sleep(3)
else:
    # Сообщение о проигрыше
    messages("Вы проиграли", red)
    pygame.display.update()
    time.sleep(2)

pygame.quit()
quit()
