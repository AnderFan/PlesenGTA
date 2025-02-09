import numpy as np
import sys
import pygame
import random

global cells_len
fieldSize = 30 # высота\широта игр.поля
cells_len = fieldSize ** 2 #  длинна массива с клетками и других связаных (генома, мертвых)

def add_cell(id_of_cell):  # """ добавить клетку перед текущей клеткой """ # УДАРЬ МЕНЯ Я НЕ РАБОТАЮ, та всё тише, уже работаешь
    ##  у нас всё храниться так [---,[*клетка*,пред клетка индекс, след клетка индекс],---]
    global dead_current
    global dead_next

    prev = cells[id_of_cell][1]  # это мы находим пред елемент
    new_id = get_dead()
    cells[prev][2] = new_id
    cells[id_of_cell][1] = new_id  # эт мы поменяли индексы в текущей и пред клетке
    # а теперь надо довавить индексы в новой клетке
    cells[new_id][0] = True # Я ПОЛТОРА ЧАСА НЕ МОГ ПОНЯТЬ ПОЧЕМУ НИЧЁ НЕ РАБОТАЕТ, ПОКА НЕ НАШЁЛ ЭТУ ПАДЛУ.
    cells[new_id][1] = prev  # добавляем пред клетку в новую клетку
    cells[new_id][2] = id_of_cell  # добавляем текущию клетку как след клетку для новой клетки


def remove_cell(cell_id): # убрать клетку с линкед листа
    global dead_current
    global dead_next

    prev = cells[cell_id][1]
    next = cells[cell_id][2]
    cells[prev][2] = next
    add_dead(cell_id)



def gen_empty_cell(): # creates empty cell// создает пустую клетку
    cell = {"int type": 0, "type": "none", "heading": 0, "energy": 0, "xy": (0, 0), "genome": 0, "links": 0, "active gene": 0 , "mutation rate": 0, "energy consumption": 0}
    # type - char[4] - leaf,root, bnch(branch), stem, sead
    # heading - 1 to 4 (0 = up, 3 = left), 0 = NaN
    # energy - -10 to ??? (255)
    # xy
    # genome coord, 0 = NaN
    # links 2 - forward, 4 - right, 8 - back, 16 - left
    # active gene - current active gene
    # mutatation rate - 0-1 - chance of mutation
    # energy consumption - потребление енергии за ход
    return cell



def generate_cells(cellsLen): # чёт мутное с очередью мертвых тут происходит
    '''
    Эта хуйня генерит первые скокото живых штук
    '''
    #num_of_cells = np.random.randint(int(cellsLen/2)) # колво скок будет живо - рандомно по приколу)))
    global dead_current
    global dead_next

    num_of_cells = 5 #колво скок живо сам задаеш
    for i in range(1, num_of_cells+1):
        cells[i][0]["type"] = "DEBUG"
        cells[i][1] = i - 1
        cells[i][2] = i + 1
        cells[i][0]["xy"] = (random.randrange(0, fieldSize * block_size, block_size) + block_size/2,
                             random.randrange(0, fieldSize * block_size, block_size) + block_size/2) # рандомно заполняем координаты клетки "xy" с шагом в величину
        print(cells[i][0]["xy"])
        print("\n")

    cells[1][1] = num_of_cells
    cells[num_of_cells][2] = 0
    # поменяли индексы крайних чтобы норм работало # замкнули

    dead_current = num_of_cells + 1  # не помню зачем но надо

    dead_next = dead_current + 1
    print(dead_current, dead_next)



def simplified_cells_print(): # debug
    toPrint = []
    cellsBuffer = np.copy(cells)
    for i in cellsBuffer:

        if i[1] + i[2] > 0:
            i[0] = "Real"
        else:
            i[0] = "XXX"
        toPrint.append(i)

    print("\n", toPrint, "\n len", len(toPrint))

def get_genome(cell): # NO VALIDATION - can be performed on any cell
    return genomes(cell["genome"]) # ааа, ну это точно недоделано

def create_cell(xy): # лол что
    pass

def genome_traverse(cell): # NO VALIDATION  # проходка по геному
    genome = get_genome(cell)

    for i in range(3):
        if genome[i]//32 <= 2:
            create_cell()
        elif genome[i]//32 == 4:
            create_cell()
        elif genome[i]// 32 == 5:
            create_cell()


def kill_cell(cell_ind): # убить клетку
    """
    :param cell_ind: - индекс клетки
    надо занести клетку в очередь мертвых клеток -add_to_queue(cell_index)
    и удалить её из связоного списка живых - kill_cell(cell_index)
    и удалить её из поля - в тупую поменять тип клетки напрямую через поле
    Разбросать енергию на клетки рядом (НАДО СДЕЛАТЬ)
    И ПОМЕНЯТЬ ЛИНКИ ПРИЛЕГАЮШИХ КЛЕТОК
    тут используем links клетки (массив из 4 булиан елементов где нулвеой - вверх, третий - лево, первый право)

    :return: - нихуя
    """

def consume_energy(cell_ind): # потребляем енергию
    cell = cells[cell_ind][0]
    cells[cell_ind][0]["energy"] = cell["energy"] - cell["energy consumption"] # кушоем енергию
    if cells[cell_ind][0]["energy"] < 0:
        return 1 # если енергии меньше 0, то посылаем сигнал шоб сдохнуть
    return 0


def produce_energy(cell_ind): # производим энергию ок да
    cell = cells[cell_ind][0]
    if cell["type"] == "leaf":
        cells[cell_ind][0]["energy"] += 15 # УДАРЬ МЕНЯ, я имею ввиду 15 потом перенести в переменную leaf_energy_prod
    elif cell["type"] == "root":
        cells[cell_ind][0]["energy"] += яша # ТУТ НАДО ОТДЕЛЬНАЯ ФУННКЕЦИЯ ДЛЯ ВЫКАЧИВАНИЯ ЕНЕРГИИ ИЗ ПОЧВЫ


def organics_check(cell): # чек органики на текущей клетке
    xy = cell["xy"]
    if field[xy[0]][xy[1]][1] > 64: # если органики больше 128, то подых # УДАРЬ МЕНЯ, тут 64 потом в переменную перенести
        return 1
    return 0

def upd_cell(cell_ind):  # связная функция, которая трогает каждую клетку, вызывает все остальные функции и переформатриуерт (нет) выходы входы функций шоб всё стыковалось
    death = 0 # не умираем
    cell = cells[cell_ind][0]
    death += consume_energy(cell_ind) # потрбляем енергию
    produce_energy(cell_ind) # производим энерегию (если мы листок иль корешок)
    death += organics_check(cell)



def get_abs_heading(abs_rot, nada_rot): # сделано кирикой, берет относительное напрваление клетки (типо справо от клетки, спереди, слева), и выдаёт абсолютное направление (1 - вверх, 4 - лево)
    """
    Надо функцию которая берет на вход абсолютное направлние клетки, желаемое относительное направление и выдаёт абсолютное направление для относительного напрваление
    :param abs_rot: Направление 0 - никуда, 1 - вверх, 4 - влево  (2 вправо, 3 вниз)
    :param nada_rot: Желаемое направление - 1 - влево, 2 - впероед, 3- вправо 4 - зад
    :return: абсолютное направление для относительного напрваление
    """
    if abs_rot == 0:
        return nada_rot
    adekvat_cord = {1: -1, 2: 0, 3: 1, 4: 2} # переназначаю ваші ебанутіе координаті ібо нехуй
    res = (abs_rot + adekvat_cord[nada_rot]) % 4
    if res == 0:
        res = 4
    return res

def move_energy(arr, now_energy, want_energy=1000, min_energy=0, prioryty=None): # ИСПОЛЬЗОВАТЬ ЧРЕЗ БУФЕРНУЮ ФУНКЦИЮ # ебаный пиздец (сделано киркой), при помощи неких темных манипуляций (не ебу) равномерно распределяет свободную енергию в соседей
    """
    крч типо передает енерегию из целевой клекти в соседей и ахуеть
    :param arr: значит двумерный массив по структре [[*тип клетку сверху*,*кол-во енергии в этой клетке*],[*тип клетку справа*,*кол-во енергии в этой клетке*],[...,...],[...,...]]
    :param now_energy: кол-во свободной енергии, это енергия которую клетка должна отдать (забейте как мы откуда её знаем, просто эту енергию надо распередлить)
    :param want_energy: мы ж хотели ещё параметр желаемого кол-ва енергии (опционален), по дефолту дохуя ставим чтобі не на что не влияло
    :param min_energy: минимально желаемое колво енергии которое хотим иметь (опционально, закидка на гены)
    :param prioryty: список в каком порядке делать обход соседей (опционально, закидка потом для генов)
    :return: новое колво енергии у текущей клетки после передачи
    """
    if prioryty is None:
        prioryty = {1: 0, 2: 1, 3: 2, 4: 3}  # ключи єто расположение (1 - вверрх и далье по часовой), а значения ето порядок обхода (по дефолту совпадают)

    if min_energy >= now_energy:
        return now_energy  # если у нас уже енергии меньше чем мы хотим иметь в минимуме, то нихуя не отдаем и все

    averange = now_energy - min_energy # почитаем суму енергии у всех соседей, ну и сразу нас закидіваем

    x = 0
    for i in range(1, len(arr)+1):

        if (arr[prioryty[int(i)]][0] not in [False]):
            if arr[prioryty[i]][1] < now_energy and arr[prioryty[i]][1] < want_energy:
                # сюда вместо фолс список с типами клеток в которіе не засовіваем енергию
                averange += arr[prioryty[i]][1]
                x += 1
    if x == 0:
        return now_energy # если какогото хуя никому не можем передать то всьо

    averange2 = int(averange/x) # вот крч считаем по скок отдаем

    for i in range(1, len(arr)+1): # вот отдаем типо
        if arr[prioryty[i]][0] not in [False] and arr[prioryty[i]][1] < now_energy and arr[prioryty[i]][1] < want_energy:
            arr[prioryty[i]][1] = averange2
    return min_energy + averange - averange2 * x # посчитали скок у нас осталось когда все отдали

def next_cell(cell_id): # это для получения след елмента линкед листа с клетками
    return cells[cell_id][2]



def add_dead(cell_id): # добавить мертвяка в конец очереди # не проверено
    global dead_next
    global cells_len
    dead_next += 1;
    dead_next = dead_next % cells_len
    dead_cells_coords[dead_next] = cell_id
    # в целом тут немного шурли мурли и добавляем клетку в конец очереди

def get_dead(): # достать мертвяка из начала очереди # не проверено
    global dead_current
    global cells_len
    cell_id = dead_cells_coords[dead_current]
    dead_current += 1;
    dead_current = dead_current % cells_len
    return cell_id
    # тут возвращаем айди мертвяка



field = [[[0,0] for j in range(fieldSize)] for i in range(fieldSize)] # создаем матрицу с двух-мерным массивом, в пизду нумпи

# Проверяем


cells = [[gen_empty_cell(),0,0] for _ in range(cells_len)]  # linked list, with all of the cells // связный список со всеми клетками
first_cell = 1
dead_cells_coords = list(range(cells_len)) ## ааа, ээээ, ну это помоему очередб с пустыми индексами в cells


global dead_current
global dead_next
dead_current = 0
dead_next = -1
dead_next = cells_len - 1
# это были указатели начала и конца очереди

genomes = [[0 for __ in range(12)] for _ in range(cells_len)] # array with all of the active genomes (len?)


##### render
block_size = 30
global SCREEN, CLOCK

BLACK = (29, 51, 74)
WHITE = (255, 255, 255)
NEW_CELL = (52, 201, 36)

WINDOW_WIDTH = fieldSize * block_size
WINDOW_HEIGHT = fieldSize * block_size
pygame.init()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()
SCREEN.fill(WHITE)
arg = block_size, WINDOW_WIDTH, WINDOW_HEIGHT, BLACK

radius = float(block_size/30)

def render(arg): # Рендерит поле, и клетки на нём
    draw_grid(arg)

    for event in pygame.event.get(): # Выход при нажатии на крестик
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for cell in cells: # Тут идёт проверка на то словарь ли ли в cell[0]
        if isinstance(cell[0], dict): #и если нет, то читаю координаты и рисую
            if cell[0]["xy"] != (0,0):
                x, y = cell[0]["xy"]
                pygame.draw.circle(SCREEN, NEW_CELL, (x, y), 13)
        else: #а если да, то ругаюсь. Это сделано потому, что в add_cell последние из cells являются bool-ами
            print(cell)
            print(f"Invalid data type: {type(cell[0])}")

    pygame.display.update()



def draw_grid(arg):
    # Set the size of the grid block
    block_size, WINDOW_WIDTH, WINDOW_HEIGHT, BLACK = arg
    for x in range(0, WINDOW_WIDTH, block_size):
        for y in range(0, WINDOW_HEIGHT, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)


#### end render

def setup():
    generate_cells(cells_len)  # тута создаеём # хуйня, чёто мутное
    яша = False;
    #нонаме - перец с костью

    #simplified_cells_print()
    #add_cell(3) # ахах ты лох, переделуй) нихуя не працює))))) 
    #print(cells)
    #simplified_cells_print()
    # print(genome)



def update():
    traverse = True
    current_cell_id = first_cell
    current_cell = cells[current_cell_id][0]
    while(current_cell_id != 0):
        #upd_cell(current_cell_id)

        current_cell_id = next_cell(current_cell_id)


def loop():
    n = 0

    while(n<10000000):
        render(arg)
        update()
        n += 1

setup()
loop()



# credits: ТриГнома (ПодСмешок, Беззыммянникк, Кирка) )