import numpy as np
import sys
import pygame
import random
#import pygame_widgets as pg_w
#from pygame_widgets.button import Button




def create_debug_genome(): # Я НЕ ТОРЧ, это временно для дебага роста по геному пока что
    genomes[0][0][0] = 2
    genomes[0][0][1] = 2
    genomes[0][0][2] = 2

def create_first_cell(): # УБЕЙСЯ # вот через этот костыль создаем первую клетку, шоб не рыгать потом эрорами
    global dead_current
    global dead_last
    dead_current += 1
    cells[1][0]["type"] = "root"

def turn_branch(cell_id): # стать веткой
    cells[cell_id][0]["type"] = "bnch"

def genome_duplicate(old_genome_id): # ВОТ ЭТО ВАЖНАЯ ХУЙНЯ\ тут мы копируем геном для семечка,
    # ДОКУМЕНТЫ
    new_genome_id = get_free_genome()
    global total_genome_len
    global gene_len
    for i in range(total_genome_len):
        for j in range(gene_len):
            genomes[new_genome_id][i][j] = genomes[old_genome_id][i][j] # тут копируем значения старого генома в новый
    return new_genome_id


def genome_mutate(cell_id): # Смутировать геном данной клетки с определенным шансом
     # ДОКУМЕНТЫ
     # УДАРЬ МЕНЯ, недописанная функция
     # ХЕЗЕШКА
    genome_id = cells[cell_id][0]["genome"]
    global adult_genome_len
    global total_genome_len
    global gene_len
    mutation_location  = random.randint(0,100) # ген для мутации
    allele_to_mutate = random.randint(0,gene_len-1) # шо смутирует в гене
    mutation_significance = random.randint(-60,60) # насколько

    if mutation_location < total_genome_len:
         #print("mutating, was", genomes[genome_id][mutation_location][allele_to_mutate], "; became:",  genomes[genome_id][mutation_location][allele_to_mutate] + mutation_significance)
         genomes[genome_id][mutation_location][allele_to_mutate] = (genomes[genome_id][mutation_location][allele_to_mutate] + mutation_significance)%256

def kill_cell(cell_id): # убивает клеть
    cell = cells[cell_id][0]

    # check integrity # СЛАВА БОГУ ЦЕЛОСТНОСТИ
    # не забудь поменть линкед лист и поле, органика, линки и ГЕНЫ И ГЕНЫ ГЕНЫ

    for i in range(0,4): # меняем линки у присоединнёных клеток # вычеркиваем мертвую клеть из соседей, шоб в неё не пихали энерджи
        linked_cell_id = cell["linksB"][i]
        #linked_cell = cells[linked_cell_id][0]
        linked_cell_link = (i + 2 ) % 4
        cells[linked_cell_id][0]["linksB"][linked_cell_link] = 0

    for i in range(0, 4): # обнуляем линки трупу, шоб когда на этом индексе выростет шото новое его не распидорасило от старых линков
        cells[cell_id][0]["linksB"][i] = 0

    # тут манипулируем геном
    genome_id = cell["genome"] # достаем айди генома
    genomes_usage[genome_id] -= 1 # и декрементируем кол-во пользователей этого генома
    if genomes_usage[genome_id] == 0: # если никто не использует данный геном, то освобождаем его
        add_free_genome(genome_id) # добавляем геном в очередь свободных геномов

    # тут трогаем поле
    x, y = cells[cell_id][0]["xy"]
    field[x][y][0] = 0 # в массиве поля на коордах мертвой клети меняем коорды
    remove_cell_lnkl(cell_id) # убираем из линкед листа


def grow_independent_cell_ID( heading, new_type, xy, genome_id, new_energy=0): # Создать новую независимую клеть - без родителя
    # ID - потому что возваращет индекс созданной клетки
    # СЛАВА БОГУ ЦЕЛОСТНОСТИ - тут и индексы могут разорваться, и коорды могут полететь
    # СУРОГГАТ ЛЮБВИ И НОРМАЛЬНОЙ ФУНКЦИИ
    global fieldSize
    child_x = xy[0]
    child_y = xy[1]
    # НЕ ЗАБУДЬ ПРО КРАЯ ПОЛЯ
    # heading - 1 up, ... , 4 - left

    if (child_x < 1 or child_x >= fieldSize -1 ) or (child_y < 1 or child_y >= fieldSize-1): #  Ну тут понятно
        print("при создании новой клетки вышли за границы")
        return 0

    if field[child_x][child_y][0] == 0: # Если ячейка поля пуста, то ростём (пуста = указывает на фантома (целс[0]))

        #child_cell_id = get_dead()
        child_cell_id = add_cell_lnkl_past(0) # тут добавляем клетку ПОСЛЕ текущей клетки\ СЛАВА БОГУ ЦЕЛОСТНОСТИ
        heading = heading -1 # Загадка: без окон, без дверей, посредине дырка

        #cells[parent_cell_id][0]["linksB"][heading] = child_cell_id # добавляем линк в родителя
        #child_link_heading = (heading +  2 ) % 4 # это куда линк в родителя от ребенка (точнее напрвление, типо если родитель создал ребенка справа, то у ребенка линк должен быть влево)
        #cells[child_cell_id][0]["linksB"][child_link_heading] = parent_cell_id  # добавляем линк в чадо

        # ВОТ ТУТ СОЗДАЕМ САМО ЧАДО
        cells[child_cell_id][0]["type"] = new_type # даём тип
        cells[child_cell_id][0]["energy"] = new_energy # даём стартовую энергию нергии
        field[child_x][child_y][0] = child_cell_id # ложим чадо в поле на соответсвущие координаты
        cells[child_cell_id][0]["xy"] = (child_x, child_y) # ну кабы коорды в клеть записываем
        cells[child_cell_id][0]["genome"] =   genome_id # даем геном
        cells[child_cell_id][0]["heading"] = heading + 1  # тут всё нормально, ничего необычного, просто даём направление, что вы воопше смотрите сюда

        genomes_usage[genome_id] += 1 # тут шоб мы понимали что эта клетка использует этот геном (увеличили кол-во геном енжоеров)
        return child_cell_id
    else:
        ###print("попытка создать клетку в клетку, неудача")
        return 0

def split_from_parent(cell_id): # ХЕЗЕШКА\ Эт штука которая уничтожает задний линк, тоесть отделяет клетку от родителя
    #print(cells[cell_id][0]["heading"])
    heading = cells[cell_id][0]["heading"] - 1
    parent_link_heading = (heading +  2 ) % 4 # это куда линк в родителя от ребенка (точнее напрвление, типо если родитель создал ребенка справа, то у ребенка линк должен быть влево)
    cells[cells[cell_id][0]["linksB"][parent_link_heading]][0]["linksB"][heading] = 0 # ну тут всё очевидно (обнуляем линк родителя, шоб он больше сюда не передавал энергию)
    cells[cell_id][0]["linksB"][parent_link_heading] = 0 # в текущей клетке (не родитель) меням линк сзади, шоб мы туда даже не смотрелли


def grow_cell(parent_cell_id, heading, new_type, new_energy=0): # Вот это штука которая выращиевт новые клетки
    # СЛАВА БОГУ ЦЕЛОСТНОСТИ - тут и индексы могут разорваться, и коорды могут полететь
    global fieldSize
    global genomes_usage
    child_x = cells[parent_cell_id][0]["xy"][0]
    child_y = cells[parent_cell_id][0]["xy"][1]
    # НЕ ЗАБУДЬ ПРО КРАЯ ПОЛЯ
    # heading - 1 up, ... , 4 - left
    if heading == 2:
        child_x += 1
    elif heading == 4:
        child_x -= 1
    elif heading == 1:
        child_y -= 1
    elif heading == 3:
        child_y += 1
    else:
        child_y = 0
        child_x = 0

    if (child_x < 1 or child_x >= fieldSize-1) or (child_y < 1 or child_y >= fieldSize-1):
        ###print("при создании новой клетки вышли за границы")
        return 0

    if field[child_x][child_y][0] == 0:


        #child_cell_id = get_dead()
        child_cell_id = add_cell_lnkl(parent_cell_id) # БОЖЕ ПОЖАЛЙСУТА РАБОТАЙ ГНИДА\ СЛАВА БОГУ ЦЕЛОСТНОСТИ
        heading = heading -1 # ибо масисы та с 0 начинатеься
        cells[parent_cell_id][0]["linksB"][heading] = child_cell_id # добавляем линк в родителя
        child_link_heading = (heading +  2 ) % 4 # это куда линк в родителя от ребенка (точнее напрвление, типо если родитель создал ребенка справа, то у ребенка линк должен быть влево)
        cells[child_cell_id][0]["linksB"][child_link_heading] = parent_cell_id  # добавляем линк в чадо

        # ВОТ ТУТ СОЗДАЕМ САМО ЧАДО
        cells[child_cell_id][0]["type"] = new_type # даём новый тип
        cells[child_cell_id][0]["energy"] = new_energy # даём гемгшл нергии
        field[child_x][child_y][0] = child_cell_id # ложим чадо в поле на соответсвущие координаты
        cells[child_cell_id][0]["xy"] = (child_x, child_y) # ну кабы коорды в клеть записываем
        cells[child_cell_id][0]["genome"] =   cells[parent_cell_id][0]["genome"] # у дитя гены такие же
        cells[child_cell_id][0]["heading"] = heading + 1 # тут поварачиваем клетку от родителя # тут вовзаврщаем хеадинг в формат где 0 зарезервирован под меня

        genome_id = cells[parent_cell_id][0]["genome"] # получили айди генома
        genomes_usage[genome_id] += 1 # увеличли кол-во энжоеров этого генома

        return 1
    else:
        ###print("попытка создать клетку в клетку, неудача")
        return 0

def change_to_leaf_LEGACY(cell_id): # УБЕЙСЯ
    cells[cell_id][0]["type"] = "leaf"
    enrg_cons = 15

    cells[cell_id][0]["energy"] = 234634623547425734574573457  # вот тут не уверен

def create_Бибки_debug():

    пирожки = 40 # ааааа, эээээ ну тама, типо, колво рядков и столбов сколько клеток спавнить, да, вроде, та в пизду
    n= 0
    for i in range(1,пирожки):
        for j in range(1,пирожки):
            x = i * 6
            y = j * 6
            cell_id_tmp = grow_independent_cell_ID(1,"stem",(x,y),n,150)
            #grow_cell(cell_id_tmp,3,"leaf",50)

            #cells[n][0]["genome"] = n
            n += 1
            #cells[n][0]["xy"] = (x,y)
            #field[x][y][0] = n




def create_Игорь_debug(): # игорь)
    # СЛАВА БОГУ ЦЕЛОСТНОСТИ - индексы изменяются руками, страшно
    global dead_current

    cells[0][2] = 1

    # добавляем в линкед лист
    cells[1][2] = 2

    cells[2][1] = 1
    cells[2][2] = 3

    cells[3][1] = 2 # leaf
    # меняем типы
    cells[1][0]["type"] = "stem"
    cells[2][0]["type"] = "bnch"
    cells[3][0]["type"] = "leaf"
    cells[3][0]["energy"] = 200

    # трогаем очередь мертвых
    dead_current = 4

    # направление
    cells[1][0]["heading"] = 4
    cells[2][0]["heading"] = 4
    cells[3][0]["heading"] = 4

    # линки
    cells[1][0]["links"] = 8  # росток
    cells[2][0]["links"] = 8+ 4 #2 + 8  # 1 2 4 8  # стебель
    cells[3][0]["links"] = 1#8  # листок

    cells[1][0]["linksB"][1] = 2
    cells[2][0]["linksB"][2] = 3
    cells[2][0]["linksB"][3] = 1
    cells[3][0]["linksB"][0] = 2

    # трогем коорлинаты
    startX = 4
    startY = 4

    cells[1][0]["xy"] = (startX, startY)
    field[startX][startY][0] = 1
    cells[2][0]["xy"] = (startX+1, startY)
    field[startX+1][startY][0] = 2
    #cells[3][0]["xy"] = (startX+2, startY)
    #field[startX + 2][startY][0] = 3
    cells[3][0]["xy"] = (startX + 1, startY + 1)
    field[startX + 1][startY + 1][0] = 3



def create_cells_debug_LEGACY(cells_number):
# generate cells тоже самое\\
# только сука женерейт целлс не работает, эта же штука аккуратно обвалакивает cells и dead_cells шоб индексы не сломались, вот прям вкусно и НЕ ТРОГАТЬ


    #блять просто иди нахуй
    # тут вроде фулл вручную создаются первые две клетки
    global dead_current
    cells[1][2] = 2
    change_cell_root_debug(1)
    change_cell_root_debug(2)
    cells[2][1] = 1
    dead_current = 3
    """эт я токошо создал вручную первые две клетки ибо так бог сказал """
    simplified_cells_print(cells)
    ###print()
    # принтим клетки ибо шоб ловить уродов

    #cells_number = 4

    for i in range(2,cells_number):
        cell_id = add_cell_lnkl(2)
        change_cell_root_debug(cell_id)
    #cell_id = add_cell_lnkl(2)
    #change_cell_root_debug(cell_id)
    # тут я черещ уже нормальную функцию создал клетки перед второй клеткой, ибо ну ну ну ну, свзяь плохая, потом перезвонишь

    simplified_cells_print(cells)
    # принтим клетки ибо шоб ловить уродов





def add_cell_lnkl(id_of_cell):  # """ добавить клетку перед текущей клеткой """ # УДАРЬ МЕНЯ Я НЕ РАБОТАЮ, та всё тише, уже работаешь
    ##  у нас всё храниться так [---,[*клетка*,пред клетка индекс, след клетка индекс],---]
    # СЛАВА БОГУ ЦЕЛОСТНОСТИ  - тут много чё может пойти не так
    global dead_current
    global dead_last

    prev = cells[id_of_cell][1]  # это мы находим пред елемент
    new_id = get_dead()
    cells[prev][2] = new_id
    cells[id_of_cell][1] = new_id  # эт мы поменяли индексы в текущей и пред клетке
    # а теперь надо довавить индексы в новой клетке
    #cells[new_id][0] = True
    cells[new_id][1] = prev  # добавляем пред клетку в новую клетку
    cells[new_id][2] = id_of_cell  # добавляем текущию клетку как след клетку для новой клетки
    return new_id # возврат айди созданной клетики

def add_cell_lnkl_past(id_of_cell):  # """ добавить клетку ПОСЛЕ текущей клеткой """ # УДАРЬ МЕНЯ Я НЕ РАБОТАЮ, та всё тише, уже работаешь
    ##  у нас всё храниться так [---,[*клетка*,пред клетка индекс, след клетка индекс],---]
    # СЛАВА БОГУ ЦЕЛОСТНОСТИ  - тут много чё может пойти не так
    global dead_current
    global dead_last

    next = cells[id_of_cell][2]  # это мы находим пред елемент
    new_id = get_dead()
    cells[next][1] = new_id
    cells[id_of_cell][2] = new_id  # эт мы поменяли индексы в текущей и пред клетке
    # а теперь надо довавить индексы в новой клетке
    #cells[new_id][0] = True
    cells[new_id][2] = next  # добавляем пред клетку в новую клетку
    cells[new_id][1] = id_of_cell  # добавляем текущию клетку как след клетку для новой клетки
    return new_id # возврат айди созданной клетики

def create_cell_debug(): # УБЕЙСЯ # хз, не трогай, чёто мутное и страшное, спрашивай беззымянника


    global dead_current
    global dead_last
    cell_id = dead_current
    dead_current += 1
    cells[cell_id][0]["type"] = "DEBUG"
    change_cell_root_debug(cell_id)

def randomize_cells_coords(fieldSize): # рандомайзит коорды клеток, на удивление даже использует нормальную проходку
    print("================================================================")
    print("RANDOMIZING COORDS")
    print()
    global first_cell_LEGACY
    current_cell_id = first_cell_LEGACY
    generated = True

    while(current_cell_id != 0):

        # тут прикол что если мы случайно создали клетку на коордах уже существующей клетки, то надо кабы хуйня переделывать
        # для этого мы чекаем поле, а точнее не существует ли на таких то коордах клетки
        # проверяем мы это через указаный индекс на квадратике поля, если индекс 0, значит тут нет реальной клетки и всё норм
        # а если индекс не 0, значит тут есть клетка (ИЛИ КОГДА ТО БЫЛА, НО ПОСКОЛЬКО МЫ ИСПАОЛЬЗУЕМ ЭТУ ФУНКЦИЮ В САМОМ НАЧАЛЕ ЭТО НЕВАЖНО)
        # генерим ХУ - чекаем не занято ли место по этим ХУ на поле - если занято, переделываем

        generated = False
        while(generated == False):

            cells[current_cell_id][0]["xy"] = (random.randint(0, fieldSize - 1), random.randint(0, fieldSize - 1))
            x, y = cells[current_cell_id][0]["xy"]
            blockCellId = field[x][y][0]  # это индекс клетки на координатах текущей клетки
            generated = True
            print("block cell id", blockCellId)
            if blockCellId != 0: # мы чекаем шо за индекс у клетки на коордах где мы хотим создать новую клетку, если индекс 0, значит там нет клетки, а если не 0, значит перезодаем
                generated = False

        x, y = cells[current_cell_id][0]["xy"]
        field[x][y][0] = current_cell_id # добавляем индекс клетки в поле на свои координаты

        current_cell_id = next_cell(current_cell_id)
    print("RANDOMIZING FINISHED")
    print("========================================")
    print()


def change_cell_root_debug(моль): # блять что это # Я НЕ ТОРЧ
    cells[моль][0]["type"] = "root"
    return "заебись)"

def remove_cell_lnkl(cell_id): # убрать клетку с линкед листа # ХЕЗЕШКА, не провереня функция
    global dead_current
    global dead_last

    prev = cells[cell_id][1] # индекс перпедыдущей клетки
    next = cells[cell_id][2] # индексик след клетки
    cells[prev][2] = next # заменяем индекс предыдущей клетки на индекс клетки следующей от текущей
    cells[next][1] = prev # заменяем индекс следующей клетки на  индекс передущей клетки
    add_dead(cell_id) # добавляем клетку в очередь мертвяков


def gen_empty_cell(): # creates empty cell// создает пустую клетку // использувется только при спавне поля, дальше не юзать
    cell = {"int type": 0, "type": "none", "heading": 0, "energy": 0, "xy": (-1, -1), "genome": 0, "links": 0, "linksB":[0,0,0,0], "active gene": 0 , "mutation rate": 0, "energy consumption": 0}
    # type - char[4] - leaf,root, bnch(branch), stem, sead
    # heading - 1 to 4 (1 = up, 4 = left), 0 = NaN
    # energy - -10 to ??? (255)
    # xy
    # genome coord, 0 = NaN
    # links 1 up , 2 - right, 4 - down, 8 - left, НЕТ НИХУЙЯ, ЛИНКИ АБСОЛЮТНЫ, НЕ ОТНОСИТЕЛЬНЫ # ЛЕГАСИ # А МОЖЕТ ТЫ МНЕ ЕЩЁ ТЕОРИЮ ОТНОСИТЕЛЬНОСТИ РАССКАЖЕШЬ? ЧТО ЭТО БЛЯТЬ ЗНАЧИТ???
    # linksB - спроси чего попроще 
    # active gene - current active gene
    # mutatation rate - 0-1 - chance of mutation
    # energy consumption - потребление енергии за ход # ЭТО СОН СОБАКИ И ЛЕГАСИ, ЭТО В ОТЕДЬНОЙ ГЛОБ ПЕРЕМННОЙ(energy_prod) БУДЕ
    return cell


def generate_cells(cellsLen): # УБЕЙСЯ # чёт мутное с очередью мертвых тут происходит
    '''
    Эта хуйня генерит первые скокото живых штук
    '''
    #num_of_cells = np.random.randint(int(cellsLen/2)) # колво скок будет живо - рандомно по приколу)))
    global dead_current
    global dead_last

    num_of_cells = 5 #колво скок живо сам задаеш
    for i in range(1, num_of_cells+1):
        cells[i][0]["type"] = "DEBUG"
        cells[i][1] = i - 1
        cells[i][2] = i + 1

    cells[1][1] = num_of_cells
    cells[num_of_cells][2] = 0
    # поменяли индексы крайних чтобы норм работало # замкнули

    dead_current = num_of_cells + 1  # не помню зачем но надо

    dead_last = dead_current + 1
    ###print(dead_current, dead_last)


def simplified_cells_print(cells): # debug
    toPrint = ["XXX",0,0]

    for i in cells:

        #if i[0]["type"] == "root":
        toPrint[0] = i[0]["type"]
        toPrint[1] = i[1]
        toPrint[2] = i[2]
        print(toPrint)

def get_genome(cell_id): # ХЕЗЕШКА
    cell = cells[cell_id][0]
    return genomes[cell["genome"]] # ааа, ну это точно недоделано

def create_cell(xy): # лол что
    pass

def genome_randomize(): # Рандомизирует геном, ИСПОРЛЬЗОВТАЬ ТОЛЬКО ПРИ СТАРТЕ
    global total_genome_len
    global gene_len
    global cells_len
    for genome_ind in range(0,cells_len): # проходимся по всем геномам
        for gene_ind in range(0,total_genome_len): # по всем генам в геноме
            for trait in range(0,gene_len): # и по всем ячейкам в гене
                genomes[genome_ind][gene_ind][trait] = random.randint(0,255) # ХЕЗЕШКА, и тут в каждой ячейке делаем рандом

def genome_traverse_для_торчей(cell_id):
    cell = cells[cell_id][0]
    genome = get_genome(cell_id)
    grow = False
    new_cell_type = "none"

    if cell["type"] == "stem":
        turn_branch(cell_id)

def categorise(x, border): # made by kirka # это функция которая форматит Х (0-255) под заданные границы, типо если бродерс
    # это функция которая форматит Х (0-255) под заданные границы, типо если бродерс
    # типо если бродерс 6, то оно выдаст число от 0 до 5, так надо для некоторых условий и комманд
    # Я НЕ ТОРЧ, ТУТ ИЗ-ЗА ОСОБЕННОСТЕЙ, ПОСЛЕДНЯЯ КАТЕГОРИЯ (если юордерс 6, то это 6) ХУЙОМБАЯ,
    # ТОЕСТЬ СТОИТ ВСОПРИНИМАТЬ ЧТО ОНО ВЫДАЕТ ЗАНЧЕНИЕ ОТ 0 ДО БОРДЕРС-1, НО ЕСЛИ ГЕН БЛИЗОК К 255, ТО ОНО МОЖЕТ ВЫДАТЬ И БОРДЕР
   return int((x + 1) / int(256 / border))


def get_fX_trait_LEGACY(X,border): # USE CATEGORISE
    # это функция которая форматит Х (0-255) под заданные границы, типо если бродерс
    # Я НЕ ТОРЧ, ТУТ ИЗ-ЗА ОСОБЕННОСТЕЙ, ПОСЛЕДНЯЯ КАТЕГОРИЯ (если юордерс 6, то это 6) ХУЙОМБАЯ,
    # ТОЕСТЬ СТОИТ ВСОПРИНИМАТЬ ЧТО ОНО ВЫДАЕТ ЗАНЧЕНИЕ ОТ 0 ДО БОРДЕРС-1, НО ЕСЛИ ГЕН БЛИЗОК К 255, ТО ОНО МОЖЕТ ВЫДАТЬ И БОРДЕР
   # типо если бродерс 6, то оно выдаст число от 0 до 5, так надо для некоторых условий и комманд
    MAX = 255
    num = int(MAX / (border + 1)) # тут мы получаем шаг для разделения, типо шаг 42 это если мы хотим разделить 255 на 6 категорий(бордер)
    num2 = X // num # тут собвстенно получаем форматирвоанние занчение
    return num2

def genome_handle(cell_id):
    global adult_genome_len
    cell = cells[cell_id][0]
    if cell["type"] == "stem":
        active_gene = cell["active gene"]
        genome_traverse_M(cell_id, active_gene,0)
    elif cell["type"] == "seed":
        active_gene = cell["active gene"]
        if cell["active gene"] < adult_genome_len: ## АААА Я НЕ ТОРЧ УДАРЬ МЕНЯ
            active_gene = adult_genome_len
        genome_traverse_M(cell_id, active_gene, 0)
    """cell = cells[cell_id][0]
    active_gene = cell["active gene"]
    if cell["type"] == "seed":
        #active_gene, _ = genome_traverse_seed(cell_id, active_gene, active_gene, 0)
        active_gene, _ = genome_traverse_seed_ТОРЧ(cell_id, active_gene, active_gene, 0)
    else:
        active_gene, _ = genome_traverse(cell_id, active_gene, active_gene, 0)
    cells[cell_id][0]["active gene"] = active_gene"""

def turn_stem_from_seed(cell_id, adult_gene): # это функция которая для взросления сынок\ для появления ростка из семечка
    # adult_gene - ген кооторый взрослая клетка будет использовать при создании
    # шо функция должна делать:
    """Менять тип клетки на росток

    Копироватть геном - декрементация клеток изсплующих текущий ген незабудь
    Мутировать

    """

    new_genome_id = genome_duplicate(cells[cell_id][0]["genome"])
    genomes_usage[cells[cell_id][0]["genome"]] -= 1
    cells[cell_id][0]["genome"] = new_genome_id
    genome_mutate(cell_id)
    cells[cell_id][0]["type"] = "stem"
    cells[cell_id][0]["active gene"] = adult_gene
    split_from_parent(cell_id)

def genome_conditions(cell_id, gene_id): # проверка условий генома\ НЕ САМОСТОЯТЕЛЬНАЯ ФУНКЦИЯ - использовать ТОЛЬКО в рамках проходка_генома()
    genome = get_genome(cell_id)
    cell = cells[cell_id][0]
    gene = genome[gene_id]
    global tick
    condition_num = categorise(gene[3], 8) # тут мы разделяем ген (0-255) на 7 равных + 1 кусков, потом эти куски итнерперетируцются как номера условий для проверки

    next = 0 # след комманда для прохоидки генома (см.ретурн и прозоходку генома)
    if cell["type"] == "seed" : #  тут мы прибавляем единичку если семечко, это шоб сменить потом укзатель правильно (см. ретурн внизу)
        next +=1
        if tick %30 != 0:
            return (0,0)

    if condition_num < 5: # УДАРЬ МЕНЯ, тут надо пеереджелать всё в матч-кейс \\ ЕСли 5 и больше, то условия нет и мы растём
        condition_X = gene[4]
        condition_Y = gene[5]
        condition_Success = False

        match (condition_num):

            case 0:  # безусловное выполнение комманды
                condition_Success = True
            case 1:  # Энергии больше(меньше) чем Х
                if cell["energy"] > condition_X:
                    condition_Success = True
            # if condition_num == 2:
            #     if cell["energy"] < condition_X:
            #         condition_Success = True
            case 2:  # Есть чужие(свои) свои клетки рядом
                # if is_nearby_foreign_cells(cell_id) == False:
                #    condition_Success = True
                condition_Success = is_nearby_foreign_cells(cell_id)
            # if condition_num == 3:
            #    condition_Success = is_nearby_any_cells(cell_id)
            case 999999999:  # По направлению х (от 0 до 3)
                condition_X = 0  # УДАРЬ МЕНЯ
                heading = get_abs_heading(cell["heading"], condition_X) - 1
                # if is_cell_near(cell_id,heading):
                #    condition_Success = True
                condition_Success = is_cell_near(cell_id, heading)
            case 3:  # По направлению х (от 0 до 3) есть клетка Y (тип клетки)
                # 0 - лево, 1(3) спереди, 2 спрва
                condition_X = categorise(condition_X, 3)  # ХЕЗЕШКА
                моль = {0: 1, 1: 2, 2: 3, 3: 2}  # тут шоб тройку сулчайно не пихнули в гет_абс_хеадинг
                heading = get_abs_heading(cell["heading"], моль[condition_X]) - 1
                # 0 - росток, 1 - ветка, 2 - листок, 3 - корешок, 4 - семечко, 5-10(11) - любая клеть
                condition_Y = categorise(condition_Y, 11)  # ХЕЗЕШКА
                муха = {0: "stem", 1: "bnch", 2: "leaf", 3: "root", 4: "sead",
                        5: "яша"}  # рельсы, шпалы, кирпичи, в тебя летит струя мочи
                if condition_Y > 4:  # ну если больше 4, то мы проверяем наличие клетки как таковой
                    condition_Success = is_cell_near(cell_id, heading)
                else:
                    condition_Success = is_particular_cell_near(cell_id, heading, муха[condition_Y])
            case 4:  # 6. Клеток в радиусе Х больше чем У # УДАРЬ МЕНЯ, очень нагруженое условие, типо два фор лупа и пару ифов, это треш
                radius = categorise(condition_X, 32)
                cells_nearby = get_cells_in_radius(cell_id, radius)
                cells_count = 0
                for i in cells_nearby:  # считаем клетки
                    if i != 0:
                        cells_count += 1
                if cells_count > condition_Y:  # и если их больше чем У, ну тода тру
                    condition_Success = True

    # тут вохзвращаем указатель на след комманду и успешность условия

        return (next+2, int(condition_Success)) # возвращаем 2 - выполнить коммнаду для взослого, 7 - для семечка
    return (next+6, 0) # - возвращем 6 или 7\\ 6 - вырости, 7 - вырости для семечка

def genome_conditions_LEGACY(cell_id, gene_id): # проверка условий генома\ НЕ САМОСТОЯТЕЛЬНАЯ ФУНКЦИЯ - использовать ТОЛЬКО в рамках проходка_генома()
    genome = get_genome(cell_id)
    cell = cells[cell_id][0]
    gene = genome[gene_id]
    global tick

    condition_num = categorise(gene[3], 8) # тут мы разделяем ген (0-255) на 7 равных + 1 кусков, потом эти куски итнерперетируцются как номера условий для проверки

    next = 0 # след комманда для прохоидки генома (см.ретурн и прозоходку генома)
    if cell["type"] == "seed": #  тут мы прибавляем единичку если семечко, это шоб сменить потом укзатель правильно (см. ретурн внизу)
        next +=1



    if condition_num < 5: # УДАРЬ МЕНЯ, тут надо пеереджелать всё в матч-кейс \\ ЕСли 5 и больше, то условия нет и мы растём
        condition_X = gene[4]
        condition_Y = gene[5]
        condition_Success = False

        if condition_num == 0:  # безусловное выполнение комманды
            condition_Success = True
        if condition_num == 1:  # Энергии больше(меньше) чем Х
            if cell["energy"] > condition_X:
                condition_Success = True
        # if condition_num == 2:
        #     if cell["energy"] < condition_X:
        #         condition_Success = True
        if condition_num == 2:  # Есть чужие(свои) свои клетки рядом
            # if is_nearby_foreign_cells(cell_id) == False:
            #    condition_Success = True
            condition_Success = is_nearby_foreign_cells(cell_id)
        # if condition_num == 3:
        #    condition_Success = is_nearby_any_cells(cell_id)
        if condition_num == 999999999:  # По направлению х (от 0 до 3)
            condition_X = 0  # УДАРЬ МЕНЯ
            heading = get_abs_heading(cell["heading"], condition_X) - 1
            # if is_cell_near(cell_id,heading):
            #    condition_Success = True
            condition_Success = is_cell_near(cell_id, heading)
        if condition_num == 3:  # По направлению х (от 0 до 3) есть клетка Y (тип клетки)
            # 0 - лево, 1(3) спереди, 2 спрва
            condition_X = categorise(condition_X, 3)  # ХЕЗЕШКА
            моль = {0: 1, 1: 2, 2: 3, 3: 2}  # тут шоб тройку сулчайно не пихнули в гет_абс_хеадинг
            heading = get_abs_heading(cell["heading"], моль[condition_X]) - 1
            # 0 - росток, 1 - ветка, 2 - листок, 3 - корешок, 4 - семечко, 5-10(11) - любая клеть
            condition_Y = categorise(condition_Y, 11)  # ХЕЗЕШКА
            муха = {0: "stem", 1: "bnch", 2: "leaf", 3: "root", 4: "sead",
                    5: "яша"}  # рельсы, шпалы, кирпичи, в тебя летит струя мочи
            if condition_Y > 4:  # ну если больше 4, то мы проверяем наличие клетки как таковой
                condition_Success = is_cell_near(cell_id, heading)
            else:
                condition_Success = is_particular_cell_near(cell_id, heading, муха[condition_Y])
        if condition_num == 4:  # 6. Клеток в радиусе Х больше чем У # УДАРЬ МЕНЯ, очень нагруженое условие, типо два фор лупа и пару ифов, это треш
            radius = categorise(condition_X, 32)
            cells_nearby = get_cells_in_radius(cell_id, radius)
            cells_count = 0
            for i in cells_nearby:  # считаем клетки
                if i != 0:
                    cells_count += 1
            if cells_count > condition_Y:  # и если их больше чем У, ну тода тру
                condition_Success = True

    # тут вохзвращаем указатель на след комманду и успешность условия

        return (next+2, int(condition_Success)) # возвращаем 2 - выполнить коммнаду для взослого, 7 - для семечка
    return (next+6, 0) # - возвращем 6 или 7\\ 6 - вырости, 7 - вырости для семечка

def set_new_root_gene(cell_id, new_root_gene):
    cells[cell_id][0]["active gene"] = new_root_gene
    return True

def genome_commands_seed(cell_id, gene_id, command_start_ind): # выполнение комманд из генома\ НЕ САМОСТОЯТЕЛЬНАЯ ФУНКЦИЯ - использовать ТОЛЬКО в рамках проходка_генома()
    # СЕКВЕНЦИЯ КОММАНД
    global adult_genome_len
    global seed_genome_len

    genome = get_genome(cell_id)
    cell = cells[cell_id][0]
    gene = genome[gene_id]

    command_num = categorise(gene[command_start_ind], 16)  # тут мы разделяем ген (0-255) на 15 равных + 1 кусков, потом эти куски итнерперетируцются как номера коммнад
    command_X = gene[command_start_ind + 1]
    command_Y = gene[command_start_ind + 2]
    command_Success = False

    if command_num == 12:  # безусловный успех комманды
        command_Success = True
    if command_num == 13:  # смена активного/рут гена на Х (или на себя)
        command_X = categorise(command_X, seed_genome_len - 1) * 2
        if command_X < seed_genome_len:
            command_X =  adult_genome_len + command_X
            set_new_root_gene(cell_id,command_X) # смениили на Х
        else:
            set_new_root_gene(cell_id,gene_id) # сменили на себя же
        command_Success = True
    if command_num < 8:  # пропуск хода # ВОТ ЭТО ВАЖНО ДЛЯ СЕМЕЧКА
        return (0,1) # next = 0 = quit/ 1 = success = command succeeded
    if command_num == 14:  # повернуться
        command_X = categorise(command_X, 4)
        cells[cell_id][0]["heading"] = ((cells[cell_id][0]["heading"]-1 + command_X) % 4) + 1

        command_Success = True
    if command_num == 15:  # отделиться\ отвалиться от родителя
        split_from_parent(cell_id)
        command_Success = True

    return (5, command_Success) # ретурним 4 =  укзатель след дейтсвия (см. проходку_генома()) и успех коммнады

def genome_commands(cell_id, gene_id, command_start_ind): # выполнение комманд из генома\ НЕ САМОСТОЯТЕЛЬНАЯ ФУНКЦИЯ - использовать ТОЛЬКО в рамках проходка_генома()
    # СЕКВЕНЦИЯ КОММАНД
    genome = get_genome(cell_id)
    cell = cells[cell_id][0]
    gene = genome[gene_id]
    global adult_genome_len

    command_num = categorise(gene[command_start_ind], 8)  # тут мы разделяем ген (0-255) на 7 равных + 1 кусков, потом эти куски итнерперетируцются как номера коммнад
    command_X = gene[command_start_ind + 1]
    command_Y = gene[command_start_ind + 2]
    command_Success = False

    match (command_num):
        case 0:# безусловный успех комманды
            command_Success = True
        case 1:  # смена активного/рут гена на Х (или на себя)
            command_X = categorise(command_X, (adult_genome_len - 1) *2)
            if command_X < adult_genome_len:
                set_new_root_gene(cell_id,command_X) # смениили на Х
            else:
                set_new_root_gene(cell_id,gene_id) # сменили на себя же
            command_Success = True
        case 2:  # пропуск хода
            return (0,1) # next = 0 = quit/ 1 = success = command succeeded
        case 3:  # повернуться
            command_X = categorise(command_X, 4)
            cells[cell_id][0]["heading"] = ((cells[cell_id][0]["heading"]-1 + command_X) % 4) + 1
            command_Success = True
        case 4:  # отделиться\ отвалиться от родителя
            split_from_parent(cell_id)
            command_Success = True
    return (4, command_Success) # ретурним 4 =  укзатель след дейтсвия (см. проходку_генома()) и успех коммнады

def genome_commands_LEGACY(cell_id, gene_id, command_start_ind): # выполнение комманд из генома\ НЕ САМОСТОЯТЕЛЬНАЯ ФУНКЦИЯ - использовать ТОЛЬКО в рамках проходка_генома()
    # СЕКВЕНЦИЯ КОММАНД
    genome = get_genome(cell_id)
    cell = cells[cell_id][0]
    gene = genome[gene_id]
    global adult_genome_len

    command_num = categorise(gene[command_start_ind], 8)  # тут мы разделяем ген (0-255) на 7 равных + 1 кусков, потом эти куски итнерперетируцются как номера коммнад
    command_X = gene[command_start_ind + 1]
    command_Y = gene[command_start_ind + 2]
    command_Success = False

    if command_num == 0:  # безусловный успех комманды
        command_Success = True
    if command_num == 1:  # смена активного/рут гена на Х (или на себя)
        command_X = categorise(command_X, (adult_genome_len - 1) *2)
        if command_X < adult_genome_len:
            set_new_root_gene(cell_id,command_X) # смениили на Х
        else:
            set_new_root_gene(cell_id,gene_id) # сменили на себя же
        command_Success = True
    if command_num == 2:  # пропуск хода
        return (0,1) # next = 0 = quit/ 1 = success = command succeeded
    if command_num == 3:  # повернуться
        command_X = categorise(command_X, 4)
        cells[cell_id][0]["heading"] = ((cells[cell_id][0]["heading"]-1 + command_X) % 4) + 1
        command_Success = True
    if command_num == 4:  # отделиться\ отвалиться от родителя
        split_from_parent(cell_id)
        command_Success = True

    return (4, command_Success) # ретурним 4 =  укзатель след дейтсвия (см. проходку_генома()) и успех коммнады

def genome_get_next_gene(cell_id, condition,command, genome_start, genome_end):
    # g start, end - нужны для семечка
    command = int(command)
    condition = int(condition)
    command = command << 1 # 10 or 00
    sum = command + condition  # 00 - both failed / 01 - condition success / 10 - command success / 11 - both sucedede
    next_gene_dict = {0:10, 1:15, 2:9, 3:14}
    next_gene_bare = next_gene_dict[sum] # bare - 0-255, а это типо хуйня, у нас 20 с чем то генов
    next_gene = genome_start + categorise(next_gene_bare,genome_end)
    return (9,next_gene)

def genome_grow_seed(cell_id):
    # ДОКУМЕНТЫ
    active_gene = 0
    turn_stem_from_seed(cell_id, active_gene)
    return 0

def genome_grow(cell_id,gene_id): # рост по геному
    cell =  cells[cell_id][0]
    gene = get_genome(cell_id)
    gene = gene[gene_id]
    new_cell_type = "я котик ты котик"
    ## СЕКВЕНЦИЯ РОСТА - УДАРЬ МЕНЯ
    if cell["energy"] > 100:  # УДАРЬ МЕНЯ, тут 100 прост по приколу пока стоит, вообще это шоб убедится шо клетка имеет достаточно энергии шоб прорости
        grow_success = 0
        for i in range(0,3):  # i = relative heading # і это отонсительное направление тут, типо влево, вперед, вправо (а не вверх, вправо, вниз, ...)
            grow = False
            abs_heading = get_abs_heading(cell["heading"], i + 1)  #
            if gene[i] // 32 <= 2:
                new_cell_type = "stem"
                grow = True
            elif gene[i] // 32 == 4:
                new_cell_type = "leaf"
                grow = True
            elif gene[i] // 32 == 5:
                new_cell_type = "seed"
                grow = True

            ###print("grow", grow)
            if grow:
                energy_to_give = energy_cons[new_cell_type] * 2
                grow_success += grow_cell(cell_id, abs_heading, new_cell_type, energy_to_give)
        if grow_success > 0:
            turn_branch(cell_id)
    return 0 # ретурним 0 = указатель шоб зкакничвали пузыриться

def  genome_traverse_M(cell_id, active_gene, depth): # M - modified
    global adult_genome_len
    global total_genome_len
    global seed_genome_len
    # тут расписані локации конретніх штук в гене, тіпо где найті условія, коммнаді і т.д.
    """
    condition_loc = 3 # условие
    condition_X_loc = 4 # параметр условия Х - 0-255
    condition_Y_loc = 5 # параметр условия Y - 0-255

    command_1_loc = 6 # команда при НЕ выполнении условия
    command_1_X_loc = 7 #
    command_1_Y_loc = 8 #

    gene_1_loc = 9 #  ген при успех команды
    gene_2_loc = 10 #  ген при неудачи команды (или без комманды)

    command_1_loc = 11 # команда при выполеннии условия
    command_1_X_loc = 12
    command_1_Y_loc = 13

    gene_3_loc = 14 # ген при успех команды
    gene_4_loc = 15# ген при неудачи команды (или без комманды)
    """
    cell = cells[cell_id][0]


    """
    1 - проверить условия 
    2 - выполнить комманды для взрослой клетки 
    3 - выполнить комманды для семечка 
    4 - сменить ген
    5 - сменить ген для семечка
    6 - вырости
    7 - вырости семечко
    8 - разервировано
    9 - смнеить ген на Х
    0 - закончить\выйти
    -1 - смерть по причине [удалено]
    
    """
    condition_success = "не ешь жолтий снег"
    command_id = "та попизди"
    command_success = "ну ахуеть теперь"
    next_gene = 69
    depth += 1


    next = 1

    # указывает какую след комманду выполнить\ команда потом возавращет указатель какую команду след выпонлить.
    next = 2 * (1 + (depth < total_genome_len)) - 3 # ЕБАТЬ ЧТО (делает некст -1 если глубина больше длинны генома = если мы в бесконечном лупе)

    while (next > 0 ):
        match(next): # про цифры снизу смотри сверху в комменте
            case 1:
                next, condition_success = genome_conditions(cell_id,active_gene)
                command_id = 6 + 5*condition_success # 6 если неуспех, 11 если успех
            case 2:
                next, command_success = genome_commands(cell_id,active_gene,command_id)
            case 3:
                next, command_success = genome_commands_seed(cell_id,active_gene,command_id)
            case 4:
                next, next_gene = genome_get_next_gene(cell_id,condition_success,command_success,0,adult_genome_len-1) # используем взрослые гены из генома
            case 5:
                next, next_gene = genome_get_next_gene(cell_id,condition_success,command_success,adult_genome_len,total_genome_len-1) # испольузуем последние\детские гены в генома
            case 6:
                next = genome_grow(cell_id,active_gene)
            case 7:
                 next = genome_grow_seed(cell_id) # ростим семечко
                #next = 0 # скипаем рост семечка для отладки
            case 9:
                next = genome_traverse_M(cell_id, next_gene, depth)
            case -1:
                print("ПИЗДА, БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
                print("ПИЗДА, БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
                print("ПИЗДА, БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
                print("ПИЗДА, БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
                kill_cell(cell_id)
                next = 0
                return 0
            case 0:
                return 0
            case _:
                while True:
                    print("АХАХАХАХАХХАХАХАХАХХА")
    return 0

    #match(cell["type"][1]):
    #    case "e":  # "sEed"
    #        genome_conditions()
    #        genome_commands()
    #        genome_grow()



def genome_traverse(cell_id, active_gene=0, root_gene = -1, depth = 0): # ХЕЗЕШКА  # проходка по геному # ЛЕГАСИ
 # ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ
# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ
    global adult_genome_len
    cell = cells[cell_id][0]
    genome = get_genome(cell_id)
    if active_gene >= adult_genome_len:
        #kill_cell(cell_id)
        active_gene = adult_genome_len-1
        return root_gene, depth

    gene = genome[active_gene]
    grow = False # для секвенции роста ниже
    new_cell_type = "none" # ????????? заглушка наверн

    if depth > 50: # это если гены перенаправляют на друг друга
        print("ПИЗДА, БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
        print("ПИЗДА, БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
        print("ПИЗДА, БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
        print("ПИЗДА, БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
        print("ПИЗДА, БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
        kill_cell(cell_id)
        return root_gene, depth
    depth += 1


    if cell["type"] == "stem":
        #print("current heading", cell["heading"])
        ###print("GENOME SEQUECE")
        ###print("cur cell type", cell["type"], "energy", cell["energy"])
        ###print("genome", genome)

        # ПРОВЕРКА УСЛОВИЯ
        condition_num = categorise(gene[3],8)
        if condition_num < 5:
            condition_X = gene[4]
            condition_Y = gene[5]
            condition_Success = False

            if condition_num == 0: # безусловное выполнение комманды
                condition_Success = True
            if condition_num == 1: # Энергии больше(меньше) чем Х
                if cell["energy"] > condition_X:
                    condition_Success = True
           # if condition_num == 2:
           #     if cell["energy"] < condition_X:
           #         condition_Success = True
            if condition_num == 2: # Есть чужие(свои) свои клетки рядом
                #if is_nearby_foreign_cells(cell_id) == False:
                #    condition_Success = True
                condition_Success = is_nearby_foreign_cells(cell_id)
            #if condition_num == 3:
            #    condition_Success = is_nearby_any_cells(cell_id)
            if condition_num == 999999999: #  По направлению х (от 0 до 3)
                condition_X = 0 # УДАРЬ МЕНЯ
                heading = get_abs_heading(cell["heading"],condition_X)-1
                    #if is_cell_near(cell_id,heading):
                    #    condition_Success = True
                condition_Success = is_cell_near(cell_id,heading)
            if condition_num == 3: #  По направлению х (от 0 до 3) есть клетка Y (тип клетки)
                # 0 - лево, 1(3) спереди, 2 спрва
                condition_X = categorise(condition_X,3)  # ХЕЗЕШКА
                моль = {0:1, 1:2, 2:3, 3:2} # тут шоб тройку сулчайно не пихнули в гет_абс_хеадинг
                heading = get_abs_heading(cell["heading"], моль[condition_X]) - 1
                # 0 - росток, 1 - ветка, 2 - листок, 3 - корешок, 4 - семечко, 5-10(11) - любая клеть
                condition_Y = categorise(condition_Y,11)  # ХЕЗЕШКА
                муха = {0: "stem", 1: "bnch", 2: "leaf", 3: "root", 4:"sead", 5:"яша"} # рельсы, шпалы, кирпичи, в тебя летит струя мочи
                if condition_Y > 4: # ну если больше 4, то мы проверяем наличие клетки как таковой
                    condition_Success = is_cell_near(cell_id,heading)
                else:
                    condition_Success = is_particular_cell_near(cell_id, heading, муха[condition_Y])
            if condition_num == 4: # 6. Клеток в радиусе Х больше чем У
                radius = categorise(condition_X,32)
                cells_nearby = get_cells_in_radius(cell_id,radius)
                cells_count = 0
                for i in cells_nearby: # считаем клетки
                    if i != 0:
                        cells_count += 1
                if cells_count > condition_Y: # и если их больше чем У, ну тода тру
                    condition_Success = True




            # СЕКВЕНЦИЯ КОММАНД
            command_start_ind = 11 # ссылка на комманду при НЕвыполении условия
            if condition_Success:
                command_start_ind = 6 # ссылка на комманду при выполении условия

            command_num = categorise(gene[command_start_ind], 8)
            command_X = gene[command_start_ind+1]
            command_Y = gene[command_start_ind+1]
            command_Success = False

            if command_num == 0: # безусловный успех комманды
                command_Success = True
            if command_num == 1: # смена активного/рут гена на Х (или на себя)
                command_X = categorise(command_X, adult_genome_len-1 )
                if command_X < adult_genome_len:
                    root_gene = command_Y
                else:
                    root_gene = active_gene
                command_Success = True
            if command_num == 2: # пропуск хода
                return root_gene, depth
            if command_num == 3: # повернуться
                command_X = categorise(command_X, 4)
                cells[cell_id][0]["heading"] = (cells[cell_id][0]["heading"]+command_X) % 4 + 1
                command_Success = True
            if command_num == 4: # отделиться\ отвалиться от родителя
                split_from_parent(cell_id)
                command_Success = True


            # СЕКВЕНЦИЯ СМЕНЫ ГЕНА

            next_gene_ind = 0
            if condition_Success:
                next_gene_ind = 9 # если условие выполено, но комманда нет
                if command_Success: # если выполнено и условие и комманда
                    next_gene_ind += 1
            elif not condition_Success:
                next_gene_ind = 9  # если НЕ выполена комманда и условие
                if command_Success:  # если НЕ выполнено условие, но выполенна комманда
                    next_gene_ind += 1
            else:
                print("ЩО ТИ НАКОЇВ, ДІДЬКО")
                input()

            next_gene = gene[next_gene_ind]
            next_gene = categorise(next_gene, adult_genome_len-1)
            if next_gene != active_gene: # если мы пытаемся переключиться на текущий же ген, то хуйня идея
                root_gene, depth = genome_traverse(cell_id, next_gene, root_gene, depth)
            return root_gene, depth

        else:

            ## СЕКВЕНЦИЯ РОСТА - УДАРЬ МЕНЯ
            if cell["energy"] > 100: # УДАРЬ МЕНЯ, тут 100 прост по приколу пока стоит, вообще это шоб убедится шо клетка имеет достаточно энергии шоб прорости
                grow_success = 0
                for i in range(0,3): # i = relative heading # і это отонсительное направление тут, типо влево, вперед, вправо (а не вверх, вправо, вниз, ...)
                    grow = False
                    abs_heading = get_abs_heading(cell["heading"], i+1)  #
                    if gene[i]//32 <= 2:
                        new_cell_type = "stem"
                        grow = True
                    elif gene[i]//32 == 4:
                        new_cell_type = "leaf"
                        grow = True
                    elif gene[i]// 32 == 5:
                        new_cell_type = "seed"
                        grow = True

                    ###print("grow", grow)
                    if grow:
                        energy_to_give = energy_cons[new_cell_type]  *  2
                        grow_success += grow_cell(cell_id, abs_heading, new_cell_type, energy_to_give )
                if grow_success > 0:
                    turn_branch(cell_id)

        return root_gene, depth
    return root_gene, depth

def genome_traverse_seed_ТОРЧ(cell_id, active_gene=0, root_gene = -1, depth = 0): # ХЕЗЕШКА  # проходка по геному #
    turn_stem_from_seed(cell_id, active_gene)
    #print("im EVOLVING")
    global adult_genome_len
    if active_gene >= adult_genome_len:
        return 0, "lol"
    return active_gene, "lol"

def genome_traverse_seed(cell_id, active_gene=0, root_gene = -1, depth = 0): # ХЕЗЕШКА  # проходка по геному # ЛЕГАСИ
# ЛЕГАСИ # ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ
# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ# ЛЕГАСИ

    global adult_genome_len
    global seed_genome_len

    if active_gene < adult_genome_len or root_gene < adult_genome_len: # УДАРЬ МЕНЯ, Я НЕ ТОРЧ, это трэш, очень временное решение
        active_gene = adult_genome_len
        root_gene = adult_genome_len

    cell = cells[cell_id][0]
    genome = get_genome(cell_id)
    gene = genome[active_gene]
    grow = False # для секвенции роста ниже
    new_cell_type = "none" # ????????? заглушка наверн

    if depth > 20: # это если гены перенаправляют на друг друга
        print("ПИЗДА, БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
        print("ПИЗДА, БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
        print("ПИЗДА, БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
        print("ПИЗДА, БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
        print("ПИЗДА, БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
        kill_cell(cell_id)
        return root_gene, depth
    depth += 1


    if cell["type"] == "seed":
        ###print("GENOME SEQUECE")
        ###print("cur cell type", cell["type"], "energy", cell["energy"])
        ###print("genome", genome)

        # ПРОВЕРКА УСЛОВИЯ
        condition_num = categorise(gene[3],8)
        if condition_num < 5:
            condition_X = gene[4]
            condition_Y = gene[5]
            condition_Success = False

            if condition_num == 0: # безусловное выполнение комманды
                condition_Success = True
            if condition_num == 1: # Энергии больше(меньше) чем Х
                if cell["energy"] > condition_X:
                    condition_Success = True
           # if condition_num == 2:
           #     if cell["energy"] < condition_X:
           #         condition_Success = True
            if condition_num == 2: # Есть чужие(свои) свои клетки рядом
                #if is_nearby_foreign_cells(cell_id) == False:
                #    condition_Success = True
                condition_Success = is_nearby_foreign_cells(cell_id)
            #if condition_num == 3:
            #    condition_Success = is_nearby_any_cells(cell_id)
            if condition_num == 999999999: #  По направлению х (от 0 до 3)
                condition_X = 0 # УДАРЬ МЕНЯ
                heading = get_abs_heading(cell["heading"],condition_X)-1
                    #if is_cell_near(cell_id,heading):
                    #    condition_Success = True
                condition_Success = is_cell_near(cell_id,heading)
            if condition_num == 3: #  По направлению х (от 0 до 3) есть клетка Y (тип клетки)
                # 0 - лево, 1(3) спереди, 2 спрва
                condition_X = categorise(condition_X,3)  # ХЕЗЕШКА
                моль = {0:1, 1:2, 2:3, 3:2} # тут шоб тройку сулчайно не пихнули в гет_абс_хеадинг
                heading = get_abs_heading(cell["heading"], моль[condition_X]) - 1
                # 0 - росток, 1 - ветка, 2 - листок, 3 - корешок, 4 - семечко, 5-10(11) - любая клеть
                condition_Y = categorise(condition_Y,11)  # ХЕЗЕШКА
                муха = {0: "stem", 1: "bnch", 2: "leaf", 3: "root", 4:"sead", 5:"яша"} # рельсы, шпалы, кирпичи, в тебя летит струя мочи
                if condition_Y > 4: # ну если больше 4, то мы проверяем наличие клетки как таковой
                    condition_Success = is_cell_near(cell_id,heading)
                else:
                    condition_Success = is_particular_cell_near(cell_id, heading, муха[condition_Y])
            if condition_num == 4: # 6. Клеток в радиусе Х больше чем У
                radius = categorise(condition_X,32)
                cells_nearby = get_cells_in_radius(cell_id,radius)
                cells_count = 0
                for i in cells_nearby:
                    if i != 0:
                        cells_count += 1
                if cells_count > condition_Y:
                    condition_Success = True




            # СЕКВЕНЦИЯ КОММАНД
            command_start_ind = 11 # ссылка на комманду при НЕвыполении условия
            if condition_Success:
                command_start_ind = 6 # ссылка на комманду при выполении условия

            command_num = categorise(gene[command_start_ind], 8)
            command_X = gene[command_start_ind+1]
            command_Y = gene[command_start_ind+1]
            command_Success = False

            if command_num == 0: # безусловный успех комманды
                command_Success = True
            if command_num == 1: # смена активного гена на Х (или на себя)
                command_X = categorise(command_X, adult_genome_len*2 )
                if command_X < adult_genome_len:
                    root_gene = command_Y
                else:
                    root_gene = active_gene
            if command_num == 2: # пропуск хода
                return root_gene, depth
            if command_num == 3333333333: # повернуться # УДАПЬ МЕНЯ, УБЕЙСЯ
                command_X = categorise(command_X, 4)
                cells[cell_id][0]["heading"] = (cells[cell_id][0]["heading"]+command_X) % 4 + 1


            # СЕКВЕНЦИЯ СМЕНЫ ГЕНА

            next_gene_ind = 0
            if condition_Success:
                next_gene_ind = 9 # если условие выполено, но комманда нет
                if command_Success: # если выполнено и условие и комманда
                    next_gene_ind += 1
            elif not condition_Success:
                next_gene_ind = 9  # если НЕ выполена комманда и условие
                if command_Success:  # если НЕ выполнено условие, но выполенна комманда
                    next_gene_ind += 1
            else:
                print("ЩО ТИ НАКОЇВ, ДІДЬКО")
                input()

            next_gene = gene[next_gene_ind]
            next_gene = adult_genome_len + categorise(next_gene, seed_genome_len-1)
            if next_gene != active_gene: # если мы пытаемся переключиться на текущий же ген, то хуйня идея
                root_gene, depth = genome_traverse(cell_id, next_gene, root_gene, depth)
            return root_gene, depth

        else:

            turn_stem_from_seed(cell_id,0)

        return root_gene, depth

def is_cell_near(cell_id, heading): # проверяет есть ли клетка рядом по орпеделномоу направелнию
    global fieldSize
    current_cell = cells[cell_id][0]
    x, y = current_cell["xy"]

    if x-1 < 0 or y-1 <0 or x+1 >= fieldSize or y+1 >= fieldSize:
        return True
    field_XY = [[x, y - 1], [x + 1, y], [x + 1, y], [x - 1, y]] # это массив с коордами клеток рядом

    x2, y2 = field_XY[heading]
    if field[x2][y2][0] != 0: # тут мы проверяем есть ли в том напрваденни клеть
        return True
    return False

def is_particular_cell_near(cell_id, heading, type): # проверяет есть ли ОПРЕДЕЛЕННАЯ клетка рядом по орпеделномоу направелнию
    current_cell = cells[cell_id][0]
    x, y = current_cell["xy"]
    field_XY = [[x, y - 1], [x + 1, y], [x + 1, y], [x - 1, y]] # это массив с коордами клеток рядом

    x2, y2 = field_XY[heading]
    if field[x2][y2][0] != 0: # тут мы проверяем есть ли в том напрваденни клеть
        if cells[field[x2][y2][0]][0]["type"] == type: #
            return True
    return False

def kill_cell_legacy(cell_ind): # убить клетку
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

def consume_energy(cell_id): # потребляем енергию
    cell = cells[cell_id][0]
    cells[cell_id][0]["energy"] -= energy_cons[cell["type"]] # кушоем енергию

def consume_energy_LEGACY(cell_ind): # потребляем енергию
    cell = cells[cell_ind][0]
    ###print(cells[cell_ind])
    cells[cell_ind][0]["energy"] = cell["energy"] - cell["energy consumption"] # кушоем енергию
    if cells[cell_ind][0]["energy"] < 0:
        return 1 # если енергии меньше 0, то посылаем сигнал шоб сдохнуть
    return 0

def produce_energy(cell_id):
    global energy_prod
    cell = cells[cell_id][0]
    if cell["type"] == "root":
        cells[cell_id][0]["energy"] += яша # УДАРЬ МЕНЯ
    cells[cell_id][0]["energy"] += energy_prod[cell["type"]]  # тут мы произвоидм енергию\ сколько произоводить мы достаем из словаря

def produce_energy_LEGACY(cell_ind): # производим энергию ок да
    global яша
    cell = cells[cell_ind][0]
    if cell["energy"] < 200:
        if cell["type"] == "leaf":
            cells[cell_ind][0]["energy"] += 15 # УДАРЬ МЕНЯ, я имею ввиду 15 потом перенести в переменную leaf_energy_prod
        elif cell["type"] == "root":
            cells[cell_ind][0]["energy"] += яша # ТУТ НАДО ОТДЕЛЬНАЯ ФУННКЕЦИЯ ДЛЯ ВЫКАЧИВАНИЯ ЕНЕРГИИ ИЗ ПОЧВЫ


def organics_check(cell): # чек органики на текущей клетке
    xy = cell["xy"]
    ###print("корды ", xy)
    if field[xy[0]][xy[1]][1] > 64: # если органики больше 128, то подых # УДАРЬ МЕНЯ, тут 64 потом в переменную перенести
        return 1
    return 0

def death_check(cell_id): # провекра штук и смерть если надо
    cell = cells[cell_id][0]
    die = -2 # АХАХАХАХАХАХАХАХААХХАХАХАХ

    if cell["energy"] < -10 or cell["energy"] > 950 : # если слишком мало энергии то умиарем, если слишком много то тож (НО ВОТ ЭТО ПОКА ЗАГЛУШКА)
        die = 1
    elif cell["type"] == "bnch": # если мы ветка то
        for i in range(1,4): # чекаем соседа слева, спереди, справи  #УДАРЬ МЕНЯ, тут можно скорее всего оптимизоравть шоб без ифа и цикла

            link = get_abs_heading(cell["heading"],i)-1
            if cell["linksB"][link] == 0:
                die += 1 # и если соседа нет то мы на шаг ближе к смерти) \\ а если соседей слева,спереди,справа нет то мы просто дохнем

    if die > 0:
        kill_cell(cell_id)

def upd_cell(cell_ind):  # связная функция, которая трогает каждую клетку, вызывает все остальные функции и переформатриуерт (нет) выходы входы функций шоб всё стыковалось
    ###print("===========================================================================")
    ###print("current cell id", cell_ind)
    death = 0 # не умираем
    cell = cells[cell_ind][0]
    consume_energy(cell_ind) # потрбляем енергию
    ###print("current cell ", cell["type"], "enetrgy ", cell["energy"])
    #move_energy(cell_ind)
    #genome_traverse(cell_ind, 0 , -1)
    genome_handle(cell_ind)

    move_energy_b(cell_ind)

    death_check(cell_ind)
    produce_energy(cell_ind) # производим энерегию (если мы листок иль корешок)




def get_cells_in_radius(cell_id, radius): # made by kirkaaaaaaa)
    """
    Круг едишн
    Ну типо вот хотим узнать айдишники соседей вокруг нас ну вот да
    :param id_of_cell: айди клетки вокруг которой ищем соседей
    :param radius: в каком радиусе искать
    :return: масив с индексами соседей
    """

    if radius < 0:
        raise ValueError("ало хули радиус меньше нуля")

    if radius == 0:
        return [cell_id]

    x0, y0 = cells[cell_id][0]["xy"]

    # x0, y0 = 5, 5
    x2 = 0
    res = [0] * (radius * radius * 4 * 2  )
    for i in range(-radius, radius + 1):
        for j in range(-(radius - abs(i)), radius + 1 - abs(i)):
            x = x0 + i
            y = y0 + j
            if 0 <= x < fieldSize and 0 <= y < fieldSize:
                # res[x] = matrix[x0 + i][y0 + j]
                res[x2] = field[x][y][0]
                x2 += 1

    return res


def get_cells_in_radius2(cell_id, radius): # made by kirkaaaaaaa) # ХЕЗЕШКА
    """
    Квадрат едишн
    Ну типо вот хотим узнать айдишники соседей вокруг нас ну вот да
    :param id_of_cell: айди клетки вокруг которой ищем соседей
    :param radius: в каком радиусе искать
    :return: масив с индексами соседей
    """

    if radius < 0:
        raise ValueError("ало хули радиус меньше нуля")

    if radius == 0:
        return [cell_id]

    # x0, y0 = cells[cell_id][0]["xy"]

    x0, y0 = 5, 5
    k = 0
    res = [0] * (2 * (radius + 1)) ** 2
    for i in range(-radius, radius + 1):
        for j in range(-radius, radius + 1):
            x = x0 + i
            y = y0 + j
            if 0 <= x < fieldSize and 0 <= y < fieldSize:
                res[k] = field[x][y][0]
                # res[x] = field[x0 + i][y0 + j][0]
                k += 1

    return res



def get_abs_heading(abs_rot, nada_rot): # сделано кирикой, берет относительное напрваление клетки (типо справо от клетки, спереди, слева), и выдаёт абсолютное направление (1 - вверх, 4 - лево)
    """
    Надо функцию которая берет на вход абсолютное направлние клетки, желаемое относительное направление и выдаёт абсолютное направление для относительного напрваление
    :param abs_rot: Направление 0 - никуда, 1 - вверх, 4 - влево  (2 вправо, 3 вниз)
    :param nada_rot: Желаемое направление - 1 - влево, 2 - впероед, 3- вправо 4 - зад
    :return: абсолютное направление для относительного напрваление
    """
    if abs_rot == 0:
        #2/0
        return nada_rot
    adekvat_cord = {1: -1, 2: 0, 3: 1, 4: 2} # переназначаю ваші ебанутіе координаті ібо нехуй
    res = (abs_rot + adekvat_cord[nada_rot]) % 4
    if res == 0:
        res = 4
    return res

def get_nearby_cells(cell_id): # ХЕЗЕШКА # Получить клетки рядом с выбранной клеткой
    current_cell = cells[cell_id][0]
    nearby_cells = [0, 0, 0, 0] # массив с клетками рядом, 0 - вверх, 3 - лево
    x, y = current_cell["xy"] # ху текущей клетки

    # получаем индексы клетком рядом
    nearby_cells[0] = field[x][y-1][0]
    nearby_cells[1] = field[x+1][y][0]
    nearby_cells[2] = field[x][y + 1][0]
    nearby_cells[3] = field[x - 1][y][0]
    return nearby_cells

def is_nearby_any_cells(cell_id): #ХЕЗЕШКА,  возвращает Тру если рядом есть клетки # возварщает Фалс если нет
    # ДОКУМЕНТЫ
    current_cell = cells[cell_id][0]
    x, y = current_cell["xy"]  # ху текущей клетки
    field_XY = [[x, y - 1], [x + 1, y], [x + 1, y], [x - 1, y]]

    for i in range(4):
        nearby_cell_id = field[field_XY[i][0]][field_XY[i][1]][0]
        if nearby_cell_id != 0:
            return True
    return False

def is_nearby_foreign_cells(cell_id): # ХЕЗЕШКА,  возвращает Тру если рядом есть неродные клетки # возварщает Фалс если нет
    # ДОКУМЕНТЫ
    current_cell = cells[cell_id][0]
    x, y = current_cell["xy"]  # ху текущей клетки
    field_XY = [[x, y - 1], [x + 1, y], [x + 1, y], [x - 1, y]]

    for i in range(4):
        nearby_cell_id = field[field_XY[i][0]][field_XY[i][1]][0]
        nearby_cell = cells[nearby_cell_id][0]
        if nearby_cell["genome"] != current_cell["genome"]:
            return True
    return False

def get_nearby_foreign_cells(cell_id): # ХЕЗЕШКА # Получить неродные клетки рядом с выбранной клеткой
    # ДОКУМЕНТЫ
    current_cell = cells[cell_id][0]
    nearby_cells = [0, 0, 0, 0] # массив с клетками рядом, 0 - вверх, 3 - лево
    x, y = current_cell["xy"] # ху текущей клетки
    field_XY = [[x,y-1],[x+1,y],[x+1,y],[x - 1,y]]

    for i in range(4):
        nearby_cell_id = field[field_XY[i][0]][field_XY[i][1]][0]
        nearby_cell = cells[nearby_cell_id][0]

        if nearby_cell["genome"] != current_cell["genome"]:
            nearby_cells[0] = nearby_cell_id
    return nearby_cells

def get_f_links_LEGACY(cell_id): # переформатировать # ЛЕГАСИ
    current_cell = cells[cell_id][0]
    links = [0,0,0,0]
    test_bit = 1

    ###print()
    for shift in range(4):
        if (test_bit << shift & current_cell["links"] > 0):
            links[shift] = 1
    return links



def get_linked_cells_LEGACY(cell_id): # УДАРЬ МЕНЯ, плохо написанная функция # шо это вообше такое # ЛЕГАСИ
    current_cell = cells[cell_id][0]
    linked_cells =get_f_links_LEGACY(cell_id)  # мммасссиввв с клетулями, отформатированный линкс (где на индексе 0 - вверх, индекс 3 - лево)
    x, y = current_cell["xy"]  # ху текущей клетки
    nearby_cells = get_nearby_cells(cell_id)


    for i in range(4):
        nearby_cells[i] = linked_cells[i] * nearby_cells[i]

    #print("nearby cells", nearby_cells)
    return nearby_cells

def move_energy_b(cell_id): # та самая буферная функция которая пузырит и формамит штуки шоб впихнуть в мув_енерджи_кор
    # СЛАВА БОГУ ЦЕЛОСТНОСТИ - может вызвать разрыв жопы, если что то пойдёт не так, то энергия будет уходить из непонятно откуда и куда
    current_cell = cells[cell_id][0]

    if current_cell["type"] != "stem" and current_cell["type"] != "none": # мы не хотим передавать энергию пустых клетко и ростков
        nearby_cells = current_cell["linksB"] # массив с индексками соседних клетко - [*индекс клетки сверху*, *индекс клетки справа*, ..., ...]
        f_nearby_cells = [[0, 0] for i in range(4)]


        for i in range(4): # форматим под кор функцию
            tmp_cell_id = nearby_cells[i]
            tmp_cell = cells[tmp_cell_id][0]

            f_nearby_cells[i][1] = tmp_cell["energy"] # энергию надо обязательно передать
            if tmp_cell_id == 0 or tmp_cell["type"] == "leaf": # если это указатель на фантомную (0) клеть или листок, то в него енергию не передаем
                f_nearby_cells[i][0] = False
            else:
                f_nearby_cells[i][0] = True

        free_energy = int(current_cell["energy"]/ 2) # УДАРЬ МЕНЯ
        free_energy = current_cell["energy"]
        own_energy = current_cell["energy"] - free_energy # это мутнаяя хуйня, Я НЕ ТОРЧ


        rem_energy, o_nearby_cells = move_energy_core(f_nearby_cells, free_energy )  # УДАРЬ МЕНЯ, тут пока просто даём всю энергию, а не свободную, шо кабы не очень
        # rem_energy - remaining energy for current cell
        # o_nearby_cells - output nearby cells, energy for neaby cells
        ###print("rem energy", rem_energy, cells[cell_id][0]["type"], cells[cell_id][0]["energy"])
        ###print("\n o_nearby_cells ", o_nearby_cells)
        cells[cell_id][0]["energy"] = rem_energy + own_energy # тут вставляем оставшуюся енергию в текущиюе клеть

        for i in range(4): # а тут раздаем соседям их новую енергию
            tmp_cell_id = nearby_cells[i]
            cells[tmp_cell_id][0]["energy"] = o_nearby_cells[i][1]


    elif current_cell["type"] == "none":
        print()
        print("Чёт ты накосячил: попытка передать энергию из пустой клетки (чекай move_energy_b)")
        input("Нажми enter что бы продолжить ")



def move_energy_LEGACY(cell_id): # та самая буферная функция которая пузырит и формамит штуки шоб впихнуть в мув_енерджи_кор

    current_cell = cells[cell_id][0]
    if current_cell["type"] != "stem" or current_cell["type"] != "none": # чёт там валидация шоб из пустого в порожнее не лить энергию
        nearby_cells = get_nearby_cells(cell_id) # клетки рядом
        nearby_cells = get_linked_cells(cell_id)
        f_nearby_cells = [[0,0] for i in range(4)] # formatted for move energy core (значит двумерный массив по структре [[*тип клетку сверху*,*кол-во енергии в этой клетке*])

        for i in range(4): # форматим под кор функцию
            tmp_cell_id = nearby_cells[i]
            tmp_cell = cells[tmp_cell_id][0]


            f_nearby_cells[i] = [True, tmp_cell["energy"]]
            if tmp_cell_id == 0 or tmp_cell["type"] == "leaf":
            #f_nearby_cells[tmp_cell_id] = [ tmp_cell["type"], tmp_cell["energy"] ] # берем кол-во енергии и тип

                f_nearby_cells[i][0] = False

        ###print("\n nearby cells pure ", nearby_cells)
        ###print(" f nearby cells ", f_nearby_cells)
        rem_energy, o_nearby_cells = move_energy_core(f_nearby_cells, current_cell["energy"] ) # УДАРЬ МЕНЯ, тут пока просто даём всю энергию, а не свободную, шо кабы не очень
        # rem_energy - remaining energy for current cell
        # o_nearby_cells - output nearby cells, energy for neaby cells
        ###print("rem energy", rem_energy, cells[cell_id][0]["type"],cells[cell_id][0]["energy"])
        ###print("\n aboba ", o_nearby_cells)


        cells[cell_id][0]["energy"] = rem_energy

       # for tmp_cell_id in range(4): # вставляем енергию в соседнии клетки
        #    cells[tmp_cell_id][0]["energy"] = o_nearby_cells[tmp_cell_id][1]

        for i in range(4):
            tmp_cell_id = nearby_cells[i]
            cells[tmp_cell_id][0]["energy"] = o_nearby_cells[i][1]


    elif current_cell["type"] == "none":
        print()
        print("Чёт ты накосячил: попытка передать энергию из пустой клетки (чекай move_energy)")
        input("Нажми enter что бы продолжить ")





def move_energy_core(arr, now_energy, want_energy=1000, min_energy=0, prioryty=None): # ИСПОЛЬЗОВАТЬ ЧРЕЗ БУФЕРНУЮ ФУНКЦИЮ # ебаный пиздец (сделано киркой), при помощи неких темных манипуляций (не ебу) равномерно распределяет свободную енергию в соседей
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
        prioryty =  {1: 0, 2: 1, 3: 2, 4: 3}  # ключи єто расположение (1 - вверрх и далье по часовой), а значения ето порядок обхода (по дефолту совпадают)

    if min_energy >= now_energy:
        return [now_energy, arr]  # если у нас уже енергии меньше чем мы хотим иметь в минимуме, то нихуя не отдаем и все

    averange = now_energy - min_energy # почитаем суму енергии у всех соседей, ну и сразу нас закидіваем

    x = 0
    for i in range(1, len(arr)+1):

        if (arr[prioryty[int(i)]][0] not in [False]):
            if ((arr[prioryty[i]][1] < now_energy) and (arr[prioryty[i]][1] < want_energy)):
                # сюда вместо фолс список с типами клеток в которіе не засовіваем енергию
                ###print("енергія соседа которого дабвляем ", arr[prioryty[i]][1])
                averange += arr[prioryty[i]][1]
                x += 1
    if x == 0:
        return [now_energy, arr] # если какогото хуя никому не можем передать то всьо

    averange2 = int(averange/x) # вот крч считаем по скок отдаем
    ###print("averange2 ", averange2 )

    if averange2 > want_energy:
        averange2 = want_energy

    for i in range(1, len(arr)+1): # вот отдаем типо
        if arr[prioryty[i]][0] not in [False] and arr[prioryty[i]][1] < now_energy and arr[prioryty[i]][1] < want_energy:
            arr[prioryty[i]][1] = averange2

    now_energy = min_energy + averange - averange2 * x # посчитали скок у нас осталось когда все отдали
    return [now_energy, arr]

def next_cell(cell_id): # это для получения след елмента линкед листа с клетками
    return cells[cell_id][2]

def add_dead(cell_id): # добавить мертвяка в конец очереди # ХЕЗЕШКА, не проверено
    global dead_last
    global cells_len
    dead_last += 1
    dead_last = dead_last % cells_len
    dead_cells_coords[dead_last] = cell_id
    # в целом тут немного шурли мурли и добавляем клетку в конец очереди

def get_dead(): # достать мертвяка из начала очереди # ХЕЗЕШКА, не проверено
    # СЛАВА БОГУ ЦЕЛОСТНОСТИ
    global dead_current
    global cells_len
    cell_id = dead_cells_coords[dead_current] # достаем индекс мертвяка
    dead_current += 1 # указатель инкрементируем на 1 (ну шоб на след мертвяка укащывал)
    dead_current = dead_current % cells_len # если мы вышли за границы массива, вовзарт в начало массива
    return cell_id
    # тут возвращаем айди мертвяка

def add_free_genome(genome_id): # Освободить геном
    # ДОКУМЕНТЫ
    global free_genomes_last
    global free_genomes_current
    global cells_len
    free_genomes_last += 1
    free_genomes_last = free_genomes_last % cells_len
    free_genomes[free_genomes_last] = genome_id

def get_free_genome(): # получить новый\неиспользуемый геном
    # ДОКУМЕНТЫ
    global free_genomes_last
    global free_genomes_current
    global cells_len
    free_genome = free_genomes[free_genomes_current]
    free_genomes_current +=1
    free_genomes_current = free_genomes_current % cells_len
    return free_genome

def render_leaf_a(x,y): # made by беззымянникк
    global rad1
    rad = rad1*2
    global block_size
    x = x+ int((block_size/2))
    y = y + int((block_size / 2))

    pygame.draw.circle(SCREEN, (0, 175, 0), (x, y), rad)
    pygame.draw.circle(SCREEN, (0, 122, 0), (x, y), rad, 3)

def render_branch_a(x,y,cell_id=0):
    global block_size
    # c - center
    xc = x + int((block_size / 2))
    yc = y + int((block_size / 2))
    rad = int(block_size / 2)
    col = (64, 64, 64)
    width = 5

    links = cells[cell_id][0]["linksB"]
    coords = [(xc, y),(x + block_size, yc),(xc, y + block_size),(x, yc)]

    for link in range(4):
        if links[link] != 0:
            pygame.draw.line(SCREEN, col, coords[link], (xc, yc), width=width)
    pygame.draw.circle(SCREEN, col, (xc, yc), width/2)
    """
    pygame.draw.line(SCREEN, col, (xc, y), (xc,yc), width=width) # вверх
    pygame.draw.line(SCREEN, col, (xc, y + block_size), (xc,yc) , width=width) # низ

    pygame.draw.line(SCREEN, col, (x, yc), (x, yc), width=width) # лево
    pygame.draw.line(SCREEN, col, (x + block_size, yc), (x, yc) , width=width) # право
    """

def render_heading(x,y,cell_id): # дебаг рендер направления
    global block_size
    # c - center
    xc = x + int((block_size / 2))
    yc = y + int((block_size / 2))
    rad = int(block_size / 2)
    col = (35, 35, 255)
    width = 6

    cell_heading = cells[cell_id][0]["heading"]

    coords = [(xc, y), (x + block_size, yc), (xc, y + block_size), (x, yc)] # вверх, вправо, вниз, влево

    for link in range(1,5):
        if cell_heading == link:
            pygame.draw.line(SCREEN, col, coords[link-1], (xc, yc), width=width)
            pygame.draw.circle(SCREEN, col, (xc, yc), width / 2)

def render_links_debug(x,y,cell_id): 
    global block_size
    # c - center
    xc = x + int((block_size / 2))
    yc = y + int((block_size / 2))
    rad = int(block_size / 2)
    col = (255, 35, 35)
    width = 4


    ###print("links", cell_links)
    links = cell_id["linksB"]
    coords = [(xc, y),(x + block_size, yc),(xc, y + block_size),(x, yc)]

    for link in range(4):
        if links[link] != 0:
            pygame.draw.line(SCREEN, col, coords[link], (xc, yc), width=width)


def render_stem_a(x,y,cell_id): # made by беззымянникк # Я НЕ ТОРЧ / УДАРЬ МЕНЯ \\ тут у росток можно увидеть линки
    global rad1
    rad = rad1
    global block_size
    # c - center
    xc = x+ int((block_size/2))
    yc = y + int((block_size / 2))
    #rad = int(block_size / 2)
    col = (64, 64, 64)
    width = 3

    render_branch_a(x,y,cell_id)
    #pygame.draw.circle(SCREEN, (0, 175, 0), (x, y), rad)
    pygame.draw.circle(SCREEN, (175, 175, 175), (xc, yc), rad)
    #pygame.draw.line(SCREEN, col, (xc,y), (xc,y+block_size), width=width)
    #pygame.draw.line(SCREEN, col, (x, yc), (x+block_size, yc), width=width)
    pygame.draw.circle(SCREEN, col, (xc, yc), rad, width)

def render_seed_a(x,y,cell_id):  # Я НЕ ТОРЧ / УДАРЬ МЕНЯ
    # ДОКУМЕНТЫ
    global rad1
    rad = rad1
    global block_size
    # c - center
    xc = x+ int((block_size/2))
    yc = y + int((block_size / 2))
    #rad = int(block_size / 2)
    col = (64, 64, 64)
    width = 2

    render_branch_a(x,y,cell_id)
    #pygame.draw.circle(SCREEN, (0, 175, 0), (x, y), rad)
    pygame.draw.circle(SCREEN, (230, 230, 0), (xc, yc), rad)
    #pygame.draw.line(SCREEN, col, (xc,y), (xc,y+block_size), width=width)
    #pygame.draw.line(SCREEN, col, (x, yc), (x+block_size, yc), width=width)
    pygame.draw.circle(SCREEN, (140, 140, 0), (xc, yc), rad, width)

def render_stem_simple(x,y): # made by беззымянникк, упрощенный рендер
    global block_size
    col = (255, 64, 64)
    pygame.draw.rect(SCREEN, col, (x, y, block_size, block_size))

def render_branch_simple(x,y): # made by беззымянникк, упрощенный рендер
    global block_size
    col = (64, 64, 64)
    pygame.draw.rect(SCREEN, col, (x, y, block_size, block_size))

def render_leaf_simple(x,y): # made by беззымянникк, упрощенный рендер
    global block_size
    col = (64, 255, 64)
    pygame.draw.rect(SCREEN, col, (x, y, block_size, block_size))

def render_seed_simple(x,y): # made by беззымянникк, упрощенный рендер
    global block_size
    col = (65, 65, 255)
    pygame.draw.rect(SCREEN, col, (x, y, block_size, block_size))

def render_monotone_simple(x,y,col): # made by беззымянникк, РЕНДЕР МОНОТОННОГО КВАДРАТИКА
    # счас исмпользуется для окараса организмов по геному
    global block_size
    #col = (65, 65, 255)
    pygame.draw.rect(SCREEN, col, (x, y, block_size, block_size))

def randomize_genome_cols():
    # ДОКУМЕНТЫ
    global cells_len
    diversion = 5
    for x in range(cells_len):
            chanLevel = random.randint(0, 255)  # channel level for each R, G and B
            #newCol = (chanLevel + chanDevLevel, chanLevel - chanDevLevel, chanLevel)
            genomesCols[x] = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
def randomize_cols_a_bit(): # установить для каждой ячейки поля чуть чуть отличюшийся цвет
    global fieldSize
    diversion = 5
    for x in range(fieldSize):
        for y in range(fieldSize):
            chanLevel = random.randint(240-diversion,255-diversion) # channel level for each R, G and B
            chanDevLevel = random.randint(-diversion,diversion) #channel deviation level
            newCol = (chanLevel+chanDevLevel,chanLevel-chanDevLevel,chanLevel)
            fieldCols[x][y][0] = newCol

def get_axy_from_fxy(fx,fy): # даем колонку и строку, получаем абсолютные коорды левого верхнего края этой клетки
    global block_size
    ax = block_size * fx
    ay = block_size * fy
    return ax, ay


def render(): # Рендерит поле, и клетки на нём
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    global block_size
    global render_mode
    global debug_mode
    global first_cell_LEGACY # мне надо
    global fontDebugSmall
    global smallFontSize
    global debug_links
    global debug_heading
    global render_cells
    global show_button
    global console_active

    match (render_mode): # отрисовка самого поля
        case 0:
            pass
        case 1: # anderfan
            draw_grid()
        case 1002: # no-name
            draw_grid_безымянник_эдитион(arg) # рисуем базовое пустое поле
        case 3:  # no-name - упрощенный рендер
            SCREEN.fill((255,255,255))




    match (render_cells): # отрисовка елементов самого поля (корни, ростки, листья и прочая моль)
        case 0:
            pass
        case 4:# base render
            for x in range(offset_x // block_size, ((WINDOW_WIDTH + offset_x) // block_size)):
                for y in range(offset_y // block_size,
                               ((WINDOW_WIDTH + offset_y) // block_size)):  # проходка только по видимой зоне
                    if x >= fieldSize:
                        x = fieldSize - 1
                    if y >= fieldSize:  # Проверка не вышли ли мы за границы field
                        y = fieldSize - 1
                    render_x, render_y = get_axy_from_fxy(x, y)
                    render_x -= offset_x
                    render_y -= offset_y
                    current_cell_id = field[x][y][0]
                    if cells[current_cell_id][0]["type"] == "stem":
                        render_stem_a(render_x, render_y, current_cell_id)
                        2 + 2
                    elif cells[current_cell_id][0]["type"] == "bnch":
                        render_branch_a(render_x, render_y, current_cell_id)
                        2 + 2
                    elif cells[current_cell_id][0]["type"] == "leaf":
                        render_leaf_a(render_x, render_y)
                        2 + 2
                    elif cells[current_cell_id][0]["type"] == "seed":
                        render_seed_a(render_x,render_y,current_cell_id)
                        2 + 2


                    #debug отсек

                    if debug_links == True:      #Сделал по запросу безымянника, но если честно не до конца понял зачем оно надо, если есть branch
                        render_links_debug(render_x,render_y,cells[current_cell_id][0])
                    if debug_heading == True:
                        render_heading(render_x,render_y,current_cell_id)

                    if debug_mode == True:

                        if cells[current_cell_id][0]["type"] != "none":
                            nudatipa = smallFontSize - 5

                            current_cell = cells[current_cell_id][0]
                            line1text = "Type:" + current_cell["type"]
                            line1 = fontDebugSmall.render(line1text, False, (255,255,255),(0,0,0))
                            SCREEN.blit(line1, (render_x,render_y))

                            line2text = "Enrg:" + str(current_cell["energy"])
                            line2 = fontDebugSmall.render(line2text, False, (255, 255, 255), (0, 0, 0))
                            SCREEN.blit(line2, (render_x, render_y+nudatipa*1))

                            line3text = "Ind:" + str(current_cell_id)
                            line3 = fontDebugSmall.render(line3text, False, (255, 255, 255), (0, 0, 0))

                    if x == 0 or y == 0 or y == -1 or x == -1 or x == fieldSize - 1 or y == fieldSize - 1:  # отрисовка границ
                        pygame.draw.rect(SCREEN, (41, 49, 51), [render_x, render_y, block_size, block_size])
          
        case 101:  # color by genome
            for x in range(offset_x // block_size, ((WINDOW_WIDTH + offset_x) // block_size)):
                for y in range(offset_y // block_size,
                               ((WINDOW_WIDTH + offset_y) // block_size)):  # проходка только по видимой зоне
                    if x >= fieldSize:
                        x = fieldSize - 1
                    if y >= fieldSize:  # Проверка не вышли ли мы за границы field
                        y = fieldSize - 1
                    render_x, render_y = get_axy_from_fxy(x, y)
                    render_x -= offset_x
                    render_y -= offset_y
                    current_cell_id = field[x][y][0]

                    col = genomesCols[cells[current_cell_id][0]["genome"]]
                    render_monotone_simple(render_x, render_y, col)
                    current_cell_id = next_cell(current_cell_id)

                    if x == 0 or y == 0 or y == -1 or x == -1 or x == fieldSize - 1 or y == fieldSize - 1:  # отрисовка границ
                        pygame.draw.rect(SCREEN, (41, 49, 51), [render_x, render_y, block_size, block_size])
        case 3: # simplified render
            for x in range(offset_x // block_size, ((WINDOW_WIDTH + offset_x) // block_size)):
                for y in range(offset_y // block_size,
                               ((WINDOW_WIDTH + offset_y) // block_size)):  # проходка только по видимой зоне
                    if x >= fieldSize:
                        x = fieldSize - 1
                    if y >= fieldSize:  # Проверка не вышли ли мы за границы field
                        y = fieldSize - 1
                    render_x, render_y = get_axy_from_fxy(x, y)
                    render_x -= offset_x
                    render_y -= offset_y
                    current_cell_id = field[x][y][0]
                    if cells[current_cell_id][0]["type"] == "stem":
                        render_stem_simple(render_x, render_y)
                        2 + 2
                    elif cells[current_cell_id][0]["type"] == "bnch":
                        render_branch_simple(render_x, render_y)
                        2 + 2
                    elif cells[current_cell_id][0]["type"] == "leaf":
                        render_leaf_simple(render_x, render_y)
                        2 + 2
                    elif cells[current_cell_id][0]["type"] == "seed":
                        render_seed_simple(render_x, render_y)
                        2 + 2

                    if x == 0 or y == 0 or y == -1 or x == -1 or x == fieldSize - 1 or y == fieldSize - 1:  # отрисовка границ
                        pygame.draw.rect(SCREEN, (41, 49, 51), [render_x, render_y, block_size, block_size])





    # Здесь отсек под кнопки, если не нравится, то можно вынести в отдельную функцию
    hide_button = create_button((87, 175, 235), 50, 50, '\/', WINDOW_WIDTH - 50, WINDOW_HEIGHT - 50, 10, 5)

    if console_active == True:
        console_btn_exit = create_button((255, 30, 30), 50, 50, 'x', WINDOW_WIDTH-50, WINDOW_HEIGHT // 3, 10, 3)

    if show_button == True:  # Если кнопки показываются - рисуем
        global burger_render_mode
        if burger_render_mode == True:
            render_base = create_button((50,109,129), 70, 70, 'r-b', 0, WINDOW_HEIGHT - 140, 10, 15)
            render_noname = create_button((50,109,129), 70, 70, 'r-n', 0, WINDOW_HEIGHT - 210, 10, 15)
            render_simple = create_button((50,109,129), 70, 70, 'r-s', 0, WINDOW_HEIGHT - 280, 10, 15)

            if render_cells == 4: 
                bdebug_links = create_button((70,129,149), 70, 70, 'd-l', 70, WINDOW_HEIGHT - 140, 10, 15)
                bdebug_heading = create_button((70,129,149), 70, 70, 'd-h', 70, WINDOW_HEIGHT - 210, 10, 15)
                bdebug_mode = create_button((70,129,149), 70, 70, 'd-m', 70, WINDOW_HEIGHT - 280, 10, 15)
        burger_render = create_button((30,89,109), 70, 70, '=', 0, WINDOW_HEIGHT - 70, 15, 15) 
      
        if running == False:
            next_step = create_button((97, 175, 235), 50, 70, '>', 100, WINDOW_HEIGHT - 70, 15, 15)
        pause = create_button((117, 195, 255), 150, 70, 'pause', 150, WINDOW_HEIGHT - 70, 25,
                              15)  # Что тут заполняется смотрите в комментах в самой функции

        interval_0 = create_button((182, 225, 252), 50, 50, '0', 0, 0, 10, 10)
        interval_1 = create_button((132, 205, 250), 50, 50, '1', 50, 0, 10, 10)
        interval_2 = create_button((84, 185, 247), 50, 50, '2', 100, 0, 10, 10)

        offset_y_up = create_button((204, 185, 247), 50, 50, '^', 175, 0, 10, 10)
        offset_x_left = create_button((204, 185, 247), 50, 50, '<', 150, 50, 10, 10)
        offset_x_right = create_button((204, 185, 247), 50, 50, '>', 200, 50, 10, 10)
        offset_y_down = create_button((204, 185, 247), 50, 50, '\/', 175, 100, 10, 10)

        scale_plus = create_button((204, 185, 247), 50, 50, '+', 250, 0, 10, 10)
        scale_minus = create_button((204, 185, 247), 50, 50, '-', 300, 0, 10, 10)

        sleep_btn = create_button((84, 185, 247), 150, 50, 'Sleep', WINDOW_WIDTH-150, 0, 10, 3)

        console_btn = create_button((44, 145, 207), 50, 50, '~', WINDOW_WIDTH-50, 50, 10, 3)

    #

    for event in pygame.event.get():  # Выход при нажатии на крестик
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if console_active == True:
                if console_btn_exit.collidepoint(event.pos):
                    console_active = False
                    show_button = True
            elif show_button == True:  # Если кнопки показываются, то проверяем жмяканье
                if running == False and next_step.collidepoint(event.pos): # Пауза активирует пошаговый режим. При нажатии на кнопку
                    update()                                               # Происходит один проход по update
                if pause.collidepoint(event.pos):  # №№№.collidepoint(event.pos) смотрит находится ли мышка на территории кнопки
                    func_pause()


                if interval_0.collidepoint(event.pos):
                    set_interval(1)
                if interval_1.collidepoint(event.pos):
                    set_interval(200)
                if interval_2.collidepoint(event.pos):
                    set_interval(1000)
                if sleep_btn.collidepoint(event.pos):
                    go_to_sleep(100)

                if offset_x_left.collidepoint(event.pos):
                    offset_horizontal(-offset)
                if offset_x_right.collidepoint(event.pos):
                    offset_horizontal(offset)

                if offset_y_up.collidepoint(event.pos):
                    offset_vertical(-offset)
                if offset_y_down.collidepoint(event.pos):
                    offset_vertical(offset)

                if scale_plus.collidepoint(event.pos):
                    scale(10)
                if scale_minus.collidepoint(event.pos):
                    scale(-10)

                # Это костыльное смена рендера и дебаг рендер
                if burger_render_mode == True:
                    if render_cells == 4: 
                        if bdebug_links.collidepoint(event.pos):
                            debug_links = not(debug_links)
                        if bdebug_heading.collidepoint(event.pos):
                            debug_heading = not(debug_heading)
                        if bdebug_mode.collidepoint(event.pos):
                            debug_mode = not(debug_mode)

                    if render_base.collidepoint(event.pos):
                        render_cells = 4 
                    if render_noname.collidepoint(event.pos):
                        render_cells = 101 
                    if render_simple.collidepoint(event.pos):
                        render_cells = 3



                if burger_render.collidepoint(event.pos): 
                    burger_render_mode = not(burger_render_mode)


                if console_btn.collidepoint(event.pos):
                    console_active = True
                    show_button = False


            if hide_button.collidepoint(event.pos):
                show_button = not (show_button)
    

    if console_active == True:
        pygame.draw.rect(SCREEN, (0,0,0), [0, 0, WINDOW_WIDTH, WINDOW_HEIGHT // 3])
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_SPACE]:
            pass




    pygame.display.update()


def create_button(color, width, height, mes, x, y, textX, textY): # color - цвет в rgb ((int, int,int)), width - ширина (int), height - высота (int), mes - текст на кнопке (str), x - координата по x (int),                                 # y - координата по y (int), react - реакция при клике (str)
    button = pygame.Rect(x,y,width, height) # textX и textY координаты текста относительно верхнего правого угла кнопки

    color_light = (min(color[0] + 40, 255), min(color[1] + 40, 255), min(color[2] + 40, 255))       # Делаем цвета


    text = font_button.render(mes, True, (255,255,255))

    if x <= pygame.mouse.get_pos()[0] <= x + width and y <= pygame.mouse.get_pos()[1] <= y + height: # проверка находится ли мышь на кнопке, можно сделать как проверке на нажатие, но я не хочу
            pygame.draw.rect(SCREEN, color_light, [x, y, width, height])
    else:
            pygame.draw.rect(SCREEN, color, [x, y, width, height])
    SCREEN.blit(text, (x + textX, y + textY)) # спавн текста

    return button # Возврат кнопки для того, что бы потом отлавливать нажатие

def buttons_react_LEGACY(react): #Функция для отслеживания какую функцию надо вызвать при нажатии на кнопку
    match(react):
        case 'hide_button':
            hide_button()
        case 'pause':
            pause()
        case 'inter_0':
            set_interval(1)
        case 'inter_1':
            set_interval(200)
        case 'inter_2':
            set_interval(1000)
        case "sleep_btn":
            go_to_sleep(100)

def go_to_sleep(alarm):
    global sleep_mode
    global tick
    sleep_mode = tick + alarm

def draw_grid(): # ебаный рот подсмешок, де коменты сука, давно реактивный пе-8 не выкачивал?
    # Set the size of the grid block # что это блять
    SCREEN.fill((255,255,255))
    for x in range(0, WINDOW_WIDTH, block_size):
        for y in range(0, WINDOW_HEIGHT, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)

            pygame.draw.rect(SCREEN, BLACK, rect, 1)


def draw_grid_безымянник_эдитион(arg): # рисуем поле путем беззымянника, ибо я хз шо в функции сверху происходит
    block_size, WINDOW_WIDTH, WINDOW_HEIGHT, BLACK = arg
    global fieldSize
    #fieldX = 0
    #fieldY = 0

    # fx/fy - field related X and Y (columns and rows)
    # ax/ay - absolute X and Y (actual pixel coodrinates)                           ІдІ нахуй
    # первое это колонки\строки, а второе это коорды пикселей

    for fx in range(0,fieldSize):
        for fy in range(0,fieldSize):
            ax = block_size * fx
            ay = block_size * fy

            rect = pygame.Rect(ax, ay, block_size, block_size)

            col = fieldCols[fx][fy][0] # цвет достаем из мега массива который я нашаманиваю где то выше

            pygame.draw.rect(SCREEN, col, rect, 0)


#### RENDER HELP VARIABLES
def offset_horizontal(int):
    global offset_x
    offset_x += int

def offset_vertical(int):
    global offset_y
    offset_y += int

def scale(int):
    global block_size
    if block_size + int <= 0 or block_size + int >= 50:
        pass
    else:
        block_size += int
        global rad1
        rad1 = 0.25 * block_size

def set_interval(int):
    global interval
    interval = int

def func_pause():
    global running
    running = not (running)

def pauseBdef():
    global pauseB
    pauseB = pauseB *-1

def handle_input():
    for event in pygame.event.get():  # Выход при нажатии на крестик
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
###END OF RENDER
### VARIBALES DECLARATION

# КЛЕТИ И ПОЛЕ
fieldSize = 300 # высота\широта игр.поля
cells_len = fieldSize ** 2 #  длинна массива с клетками и других связаных (генома, мертвых)

# ПОЛЕ
field = [[[0,0] for j in range(fieldSize)] for i in range(fieldSize)] # создаем матрицу с двух-мерным массивом, в пизду нумпи
fieldCols = [[[(255,0,0),(255,255,255)] for j in range(fieldSize)] for i in range(fieldSize)] # это отдельный массив с цветами для клеток, почему так, спросите беззымянника

# КЛЕТИ
cells = [[gen_empty_cell(),0,0] for _ in range(cells_len)]  # linked list, with all of the cells // связный список со всеми клетками
first_cell_LEGACY = 1 # УБЕЙСЯ, какойто долбоеб (беззымянник) забыл как у нас работает линкед лист и положил это сюда, оно тут не долэно быть
# для получения индекса первой клетки надо спрашивать cells[0][2] - фантомную клеть.

# МОРГ
dead_cells_coords = list(range(cells_len)) ## ааа, ээээ, ну это помоему очередб с пустыми индексами в cells
dead_current = 1# начало очереди
dead_last = -1 # свежие пирожки
dead_last = cells_len - 1 # конец очереди
# это были указатели начала и конца очереди

print(dead_cells_coords)
print(dead_current)
print(dead_last)
#print(cells)

# Проверяем \\ КОГО, О ЧЕМ ТЫ

# констатнты для клеток # ну или тип того ок да
# УДАРЬ МЕНЯ, блять а нахуя две матрицы под потрбление и производство енрегии, можно ведь всё в одну
energy_cons = {"leaf":0,"bnch":1,"none":0,"stem":5,"root":0,"seed":2} # energy consumption - потребление енргии разными клетями
energy_prod = {"leaf":15,"bnch":0,"none":0,"stem":0,"root":0,"seed":0} # energy production - производвтсво энергии разными лклетями
# у корня производсвтов не постоянно, потому пока 0 заглушка УДАРЬ МЕНЯ

яша = 42

# ГЕНОМ
adult_genome_len = 17
seed_genome_len = 5
total_genome_len = adult_genome_len+ seed_genome_len
gene_len = 18
genomes = [[[0 for ___ in range(gene_len)] for __ in range(total_genome_len) ] for _ in range(cells_len)] # array with all of the active genomes (len?)
genomesCols = [(255,0,0) for i in range(cells_len)]
free_genomes = list(range(cells_len)) # очередь с метрвыми\свободными геномами
free_genomes_current = 1 # начало
free_genomes_last = cells_len-1 # конец очер
genomes_usage = list(range(cells_len)) # массив с кол-вом клеток используюзих данный геном


# ХЕЗЕШКА ВАЖНО, у нас нет валидации очередей и линкед листа (типо пустой ли он, заполнен ли),
# ибо в нашей ситуации полностью заполеный или пустой очередь\связной лист
# означает либо полную смерть популяции(вероятно), или же что всё поле полностью занято(крайне маловеротняно)
# но поскольку у нас лапки, это может вызвать проблемы с целостностью, ибо чето где то один индекс забыть поменять и пизда
# СЛАВА БОГУ ЦЕЛОСТНОСТИ

##### render varibables
block_size = 30 # размеры квадратиков поля
render_mode = 3 # 1 - подсмешок база, 3 - упрощенный рендер
render_cells = 3 # 1 - приколы от подсмешка, 3 - упрщенный рендер
# 100 - рендер от генома
debug_links = False
debug_heading = False
debug_mode = False
burger_render_mode = False
running = True # На паузе ли прога
sleep_mode = 0 # Включен ли рендер (ну тоесть фалс это да) // когда просыпатсья (на каком тике)
tick = 0
#sleep_alarm = 0 #
global console_active
console_active = False # Включена ли консоль

console_buffer = ''

interval = 2 # Задержка между обновленями рассчётов (не действует на рендер)

global offset
offset = block_size * 4 # Дальность смещения

offset_x = 0
offset_y = 0

# ну тут цвета
BLACK = (29, 51, 74)
WHITE = (255, 255, 255)
NEW_CELL = (52, 201, 36)

# ну тут хз чёто наврнео очень нужное
WINDOW_WIDTH = 1270
WINDOW_HEIGHT = 720
pygame.init()  # вот это должно быть в сетапе
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()  # вот это время в чем то как то ну там спрашивайте ПодСмешка
SCREEN.fill(WHITE)
arg = block_size, WINDOW_WIDTH, WINDOW_HEIGHT, BLACK  # моль)
global radl
rad1 = 0.25 * block_size  # не забудь поменять в def scale тоже
radius = float(block_size / 30)  # УЛЬТИМАТИВНЫЙ РАДИУС???????? ЧТО ЭТО, ПОЧЕМУ /30 # Это вообще нигде не испульзуется УБЕЙСЯ
smallFontSize = 17 # УБЕЙСЯ, хуйня, я уже заспыпл когда писал, чёт мутное и нерабочее
fontDebugSmall = pygame.font.Font(None, smallFontSize)  # малый шрифт для дебага на клетках

global font_button
font_button = pygame.font.SysFont('Verdana', 35) # Задача фонта для кнопок

show_button = True # Перменная определяющая показываются ли кнопки


"""
легенда для комментов:
УДАРЬ МЕНЯ - чёт сломано, но немного может и работает
УБЕЙСЯ - не использовать, всё сломает
ХЕЗЕШКА - должно работать, но нормально не проверено
СЛАВА БОГУ ЦЕЛОСТНОСТИ - тут теоретически может разоравться целостсность (полететь индексы, укзатели, и т.д.)
ЛЕГАСИ - устаревшее решение, почти убейся
"""


def setup():
    #generate_cells(cellsLen)  # тута создаеём # хуйня, чёто мутное
    #randomize_cols_a_bit()
    randomize_genome_cols()
    #нонаме - перец с костью
    #create_Игорь_debug()
    create_Бибки_debug()
    #grow_cell(2, 1, "bnch", 0)
    create_debug_genome()
    genome_randomize()
    #create_cells_debug(3) # шутка генерит клетки, работает и ладно, слава целостности cells
    #randomize_cells_coords(fieldSize) # рандомазит коорды стартовых клеток, максмимальная залупа, использовать только и тут и сейчас, оно тупое и еле дышит

    #simplified_cells_print()
    #add_cell_lnkl(3) # ахах ты лох, переделуй) нихуя не працює)))))
    #print(cells)
    #simplified_cells_print()
    #(genome)
    pass


def update():

    global first_cell_LEGACY
    traverse = True
    current_cell_id = first_cell_LEGACY #first_cell_LEGACY # я ебу? фирст целл = 1, хуле? # Да завали, работает же # Сьебал, уже не ебу сколько и где оно менятеся, но всё ещё работает
    current_cell_id = cells[0][2]
    current_cell = cells[current_cell_id][0]

    while(current_cell_id != 0):

        upd_cell(current_cell_id)
        current_cell_id = next_cell(current_cell_id)



def loop():
    global running
    global pauseB
    global sleep_mode
    global tick

    while (tick < 5 or True):

        if tick > sleep_mode:
            render()

        if (running == True and tick%interval == 0):

            update()

        #handle_input()  # хуйня, не робе, пожалуйста кто то почините пж
        tick += 1
        print(tick, sleep_mode)



setup()
loop()



# credits: ТриГнома (ПодСмешок, Беззыммянникк, Кирка) )
# идея: foo52ru техношаман