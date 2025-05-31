import sys
import pygame
import random




def create_debug_genome():
    genomes[0][0][0] = 2
    genomes[0][0][1] = 2
    genomes[0][0][2] = 2

def create_first_cell():
    global dead_current
    global dead_last
    dead_current += 1
    cells[1][0]["type"] = "root"

def turn_branch(cell_id):
    cells[cell_id][0]["type"] = "bnch"

def genome_duplicate(old_genome_id):
    new_genome_id = get_free_genome()
    global total_genome_len
    global gene_len
    for i in range(total_genome_len):
        for j in range(gene_len):
            genomes[new_genome_id][i][j] = genomes[old_genome_id][i][j]
    return new_genome_id


def genome_mutate(cell_id):
    genome_id = cells[cell_id][0]["genome"]
    global adult_genome_len
    global total_genome_len
    global gene_len
    mutation_location  = random.randint(0,100)
    allele_to_mutate = random.randint(0,gene_len-1)
    mutation_significance = random.randint(-60,60)

    if mutation_location < total_genome_len:
         genomes[genome_id][mutation_location][allele_to_mutate] = (genomes[genome_id][mutation_location][allele_to_mutate] + mutation_significance)%256

def kill_cell(cell_id):
    cell = cells[cell_id][0]


    for i in range(0,4):
        linked_cell_id = cell["linksB"][i]
        linked_cell_link = (i + 2 ) % 4
        cells[linked_cell_id][0]["linksB"][linked_cell_link] = 0

    for i in range(0, 4):
        cells[cell_id][0]["linksB"][i] = 0

    genome_id = cell["genome"]
    genomes_usage[genome_id] -= 1
    if genomes_usage[genome_id] == 0:
        add_free_genome(genome_id)

    x, y = cells[cell_id][0]["xy"]
    field[x][y][0] = 0
    remove_cell_lnkl(cell_id)


def grow_independent_cell_ID( heading, new_type, xy, genome_id, new_energy=0):
    global fieldSize
    child_x = xy[0]
    child_y = xy[1]

    if (child_x < 1 or child_x >= fieldSize -1 ) or (child_y < 1 or child_y >= fieldSize-1):
        print("при создании новой клетки вышли за границы")
        return 0

    if field[child_x][child_y][0] == 0:

        child_cell_id = add_cell_lnkl_past(0)
        heading = heading -1


        cells[child_cell_id][0]["type"] = new_type
        cells[child_cell_id][0]["energy"] = new_energy
        field[child_x][child_y][0] = child_cell_id
        cells[child_cell_id][0]["xy"] = (child_x, child_y)
        cells[child_cell_id][0]["genome"] =   genome_id
        cells[child_cell_id][0]["heading"] = heading + 1

        genomes_usage[genome_id] += 1
        return child_cell_id
    else:
        return 0

def split_from_parent(cell_id):
    heading = cells[cell_id][0]["heading"] - 1
    parent_link_heading = (heading +  2 ) % 4
    cells[cells[cell_id][0]["linksB"][parent_link_heading]][0]["linksB"][heading] = 0
    cells[cell_id][0]["linksB"][parent_link_heading] = 0


def grow_cell(parent_cell_id, heading, new_type, new_energy=0):
    global fieldSize
    global genomes_usage
    child_x = cells[parent_cell_id][0]["xy"][0]
    child_y = cells[parent_cell_id][0]["xy"][1]
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
        return 0

    if field[child_x][child_y][0] == 0:


        child_cell_id = add_cell_lnkl(parent_cell_id)
        heading = heading -1
        cells[parent_cell_id][0]["linksB"][heading] = child_cell_id
        child_link_heading = (heading +  2 ) % 4
        cells[child_cell_id][0]["linksB"][child_link_heading] = parent_cell_id

        cells[child_cell_id][0]["type"] = new_type
        cells[child_cell_id][0]["energy"] = new_energy
        field[child_x][child_y][0] = child_cell_id
        cells[child_cell_id][0]["xy"] = (child_x, child_y)
        cells[child_cell_id][0]["genome"] =   cells[parent_cell_id][0]["genome"]
        cells[child_cell_id][0]["heading"] = heading + 1

        genome_id = cells[parent_cell_id][0]["genome"]
        genomes_usage[genome_id] += 1

        return 1
    else:
        return 0

def change_to_leaf_LEGACY(cell_id):
    cells[cell_id][0]["type"] = "leaf"
    enrg_cons = 15

    cells[cell_id][0]["energy"] = 234634623547425734574573457

def create_Бибки_debug():

    пирожки = 40
    n= 0
    for i in range(1,пирожки):
        for j in range(1,пирожки):
            x = i * 6
            y = j * 6
            cell_id_tmp = grow_independent_cell_ID(1,"stem",(x,y),n,150)

            n += 1




def create_Игорь_debug():
    global dead_current

    cells[0][2] = 1

    cells[1][2] = 2

    cells[2][1] = 1
    cells[2][2] = 3

    cells[3][1] = 2
    cells[1][0]["type"] = "stem"
    cells[2][0]["type"] = "bnch"
    cells[3][0]["type"] = "leaf"
    cells[3][0]["energy"] = 200

    dead_current = 4

    cells[1][0]["heading"] = 4
    cells[2][0]["heading"] = 4
    cells[3][0]["heading"] = 4

    cells[1][0]["links"] = 8
    cells[2][0]["links"] = 8+ 4
    cells[3][0]["links"] = 1

    cells[1][0]["linksB"][1] = 2
    cells[2][0]["linksB"][2] = 3
    cells[2][0]["linksB"][3] = 1
    cells[3][0]["linksB"][0] = 2

    startX = 4
    startY = 4

    cells[1][0]["xy"] = (startX, startY)
    field[startX][startY][0] = 1
    cells[2][0]["xy"] = (startX+1, startY)
    field[startX+1][startY][0] = 2
    cells[3][0]["xy"] = (startX + 1, startY + 1)
    field[startX + 1][startY + 1][0] = 3



def create_cells_debug_LEGACY(cells_number):


    global dead_current
    cells[1][2] = 2
    change_cell_root_debug(1)
    change_cell_root_debug(2)
    cells[2][1] = 1
    dead_current = 3

    simplified_cells_print(cells)


    for i in range(2,cells_number):
        cell_id = add_cell_lnkl(2)
        change_cell_root_debug(cell_id)

    simplified_cells_print(cells)





def add_cell_lnkl(id_of_cell):
    global dead_current
    global dead_last

    prev = cells[id_of_cell][1]
    new_id = get_dead()
    cells[prev][2] = new_id
    cells[id_of_cell][1] = new_id
    cells[new_id][1] = prev
    cells[new_id][2] = id_of_cell
    return new_id

def add_cell_lnkl_past(id_of_cell):
    global dead_current
    global dead_last

    next = cells[id_of_cell][2]
    new_id = get_dead()
    cells[next][1] = new_id
    cells[id_of_cell][2] = new_id
    cells[new_id][2] = next
    cells[new_id][1] = id_of_cell
    return new_id

def create_cell_debug():


    global dead_current
    global dead_last
    cell_id = dead_current
    dead_current += 1
    cells[cell_id][0]["type"] = "DEBUG"
    change_cell_root_debug(cell_id)

def randomize_cells_coords(fieldSize):
    print("================================================================")
    print("RANDOMIZING COORDS")
    print()
    global first_cell_LEGACY
    current_cell_id = first_cell_LEGACY
    generated = True

    while(current_cell_id != 0):


        generated = False
        while(generated == False):

            cells[current_cell_id][0]["xy"] = (random.randint(0, fieldSize - 1), random.randint(0, fieldSize - 1))
            x, y = cells[current_cell_id][0]["xy"]
            blockCellId = field[x][y][0]
            generated = True
            print("block cell id", blockCellId)
            if blockCellId != 0:
                generated = False

        x, y = cells[current_cell_id][0]["xy"]
        field[x][y][0] = current_cell_id

        current_cell_id = next_cell(current_cell_id)
    print("RANDOMIZING FINISHED")
    print("========================================")
    print()


def change_cell_root_debug(моль):
    cells[моль][0]["type"] = "root"
    return "заебись)"

def remove_cell_lnkl(cell_id):
    global dead_current
    global dead_last

    prev = cells[cell_id][1]
    next = cells[cell_id][2]
    cells[prev][2] = next
    cells[next][1] = prev
    add_dead(cell_id)


def gen_empty_cell():
    cell = {"int type": 0, "type": "none", "heading": 0, "energy": 0, "xy": (-1, -1), "genome": 0, "links": 0, "linksB":[0,0,0,0], "active gene": 0 , "mutation rate": 0, "energy consumption": 0}
    return cell


def generate_cells(cellsLen):
    '''
    Это генерит первые скокото живых штук
    '''
    global dead_current
    global dead_last

    num_of_cells = 5
    for i in range(1, num_of_cells+1):
        cells[i][0]["type"] = "DEBUG"
        cells[i][1] = i - 1
        cells[i][2] = i + 1

    cells[1][1] = num_of_cells
    cells[num_of_cells][2] = 0

    dead_current = num_of_cells + 1

    dead_last = dead_current + 1


def simplified_cells_print(cells):
    toPrint = ["XXX",0,0]

    for i in cells:

        toPrint[0] = i[0]["type"]
        toPrint[1] = i[1]
        toPrint[2] = i[2]
        print(toPrint)

def get_genome(cell_id):
    cell = cells[cell_id][0]
    return genomes[cell["genome"]]

def create_cell(xy):
    pass

def genome_randomize():
    global total_genome_len
    global gene_len
    global cells_len
    for genome_ind in range(0,cells_len):
        for gene_ind in range(0,total_genome_len):
            for trait in range(0,gene_len):
                genomes[genome_ind][gene_ind][trait] = random.randint(0,255)

def genome_traverse_для_торчей(cell_id):
    cell = cells[cell_id][0]
    genome = get_genome(cell_id)
    grow = False
    new_cell_type = "none"

    if cell["type"] == "stem":
        turn_branch(cell_id)

def categorise(x, border):
   return int((x + 1) / int(256 / border))


def get_fX_trait_LEGACY(X,border):
    MAX = 255
    num = int(MAX / (border + 1))
    num2 = X // num
    return num2

def genome_handle(cell_id):
    global adult_genome_len
    cell = cells[cell_id][0]
    if cell["type"] == "stem":
        active_gene = cell["active gene"]
        genome_traverse_M(cell_id, active_gene,0)
    elif cell["type"] == "seed":
        active_gene = cell["active gene"]
        if cell["active gene"] < adult_genome_len:
            active_gene = adult_genome_len
        genome_traverse_M(cell_id, active_gene, 0)
    """cell = cells[cell_id][0]
    active_gene = cell["active gene"]
    if cell["type"] == "seed":
        active_gene, _ = genome_traverse_seed_ТОРЧ(cell_id, active_gene, active_gene, 0)
    else:
        active_gene, _ = genome_traverse(cell_id, active_gene, active_gene, 0)
    cells[cell_id][0]["active gene"] = active_gene"""

def turn_stem_from_seed(cell_id, adult_gene):
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

def genome_conditions(cell_id, gene_id):
    genome = get_genome(cell_id)
    cell = cells[cell_id][0]
    gene = genome[gene_id]
    global tick
    condition_num = categorise(gene[3], 8)

    next = 0
    if cell["type"] == "seed" :
        next +=1
        if tick %30 != 0:
            return (0,0)

    if condition_num < 5:
        condition_X = gene[4]
        condition_Y = gene[5]
        condition_Success = False

        match (condition_num):

            case 0:
                condition_Success = True
            case 1:
                if cell["energy"] > condition_X:
                    condition_Success = True
            case 2:
                condition_Success = is_nearby_foreign_cells(cell_id)
            case 999999999:
                condition_X = 0
                heading = get_abs_heading(cell["heading"], condition_X) - 1
                condition_Success = is_cell_near(cell_id, heading)
            case 3:
                condition_X = categorise(condition_X, 3)
                моль = {0: 1, 1: 2, 2: 3, 3: 2}
                heading = get_abs_heading(cell["heading"], моль[condition_X]) - 1
                condition_Y = categorise(condition_Y, 11)
                муха = {0: "stem", 1: "bnch", 2: "leaf", 3: "root", 4: "sead",
                        5: "яша"}
                if condition_Y > 4:
                    condition_Success = is_cell_near(cell_id, heading)
                else:
                    condition_Success = is_particular_cell_near(cell_id, heading, муха[condition_Y])
            case 4:
                radius = categorise(condition_X, 32)
                cells_nearby = get_cells_in_radius(cell_id, radius)
                cells_count = 0
                for i in cells_nearby:
                    if i != 0:
                        cells_count += 1
                if cells_count > condition_Y:
                    condition_Success = True


        return (next+2, int(condition_Success))
    return (next+6, 0)

def genome_conditions_LEGACY(cell_id, gene_id):
    genome = get_genome(cell_id)
    cell = cells[cell_id][0]
    gene = genome[gene_id]
    global tick

    condition_num = categorise(gene[3], 8)

    next = 0
    if cell["type"] == "seed":
        next +=1



    if condition_num < 5:
        condition_X = gene[4]
        condition_Y = gene[5]
        condition_Success = False

        if condition_num == 0:
            condition_Success = True
        if condition_num == 1:
            if cell["energy"] > condition_X:
                condition_Success = True
        if condition_num == 2:
            condition_Success = is_nearby_foreign_cells(cell_id)
        if condition_num == 999999999:
            condition_X = 0
            heading = get_abs_heading(cell["heading"], condition_X) - 1
            condition_Success = is_cell_near(cell_id, heading)
        if condition_num == 3:
            condition_X = categorise(condition_X, 3)
            моль = {0: 1, 1: 2, 2: 3, 3: 2}
            heading = get_abs_heading(cell["heading"], моль[condition_X]) - 1
            condition_Y = categorise(condition_Y, 11)
            муха = {0: "stem", 1: "bnch", 2: "leaf", 3: "root", 4: "sead",
                    5: "яша"}
            if condition_Y > 4:
                condition_Success = is_cell_near(cell_id, heading)
            else:
                condition_Success = is_particular_cell_near(cell_id, heading, муха[condition_Y])
        if condition_num == 4:
            radius = categorise(condition_X, 32)
            cells_nearby = get_cells_in_radius(cell_id, radius)
            cells_count = 0
            for i in cells_nearby:
                if i != 0:
                    cells_count += 1
            if cells_count > condition_Y:
                condition_Success = True


        return (next+2, int(condition_Success))
    return (next+6, 0)

def set_new_root_gene(cell_id, new_root_gene):
    cells[cell_id][0]["active gene"] = new_root_gene
    return True

def genome_commands_seed(cell_id, gene_id, command_start_ind):
    global adult_genome_len
    global seed_genome_len

    genome = get_genome(cell_id)
    cell = cells[cell_id][0]
    gene = genome[gene_id]

    command_num = categorise(gene[command_start_ind], 16)
    command_X = gene[command_start_ind + 1]
    command_Y = gene[command_start_ind + 2]
    command_Success = False

    if command_num == 12:
        command_Success = True
    if command_num == 13:
        command_X = categorise(command_X, seed_genome_len - 1) * 2
        if command_X < seed_genome_len:
            command_X =  adult_genome_len + command_X
            set_new_root_gene(cell_id,command_X)
        else:
            set_new_root_gene(cell_id,gene_id)
        command_Success = True
    if command_num < 8:
        return (0,1)
    if command_num == 14:
        command_X = categorise(command_X, 4)
        cells[cell_id][0]["heading"] = ((cells[cell_id][0]["heading"]-1 + command_X) % 4) + 1

        command_Success = True
    if command_num == 15:
        split_from_parent(cell_id)
        command_Success = True

    return (5, command_Success)

def genome_commands(cell_id, gene_id, command_start_ind):
    genome = get_genome(cell_id)
    cell = cells[cell_id][0]
    gene = genome[gene_id]
    global adult_genome_len

    command_num = categorise(gene[command_start_ind], 8)
    command_X = gene[command_start_ind + 1]
    command_Y = gene[command_start_ind + 2]
    command_Success = False

    match (command_num):
        case 0:
            command_Success = True
        case 1:
            command_X = categorise(command_X, (adult_genome_len - 1) *2)
            if command_X < adult_genome_len:
                set_new_root_gene(cell_id,command_X)
            else:
                set_new_root_gene(cell_id,gene_id)
            command_Success = True
        case 2:
            return (0,1)
        case 3:
            command_X = categorise(command_X, 4)
            cells[cell_id][0]["heading"] = ((cells[cell_id][0]["heading"]-1 + command_X) % 4) + 1
            command_Success = True
        case 4:
            split_from_parent(cell_id)
            command_Success = True
    return (4, command_Success)

def genome_commands_LEGACY(cell_id, gene_id, command_start_ind):
    genome = get_genome(cell_id)
    cell = cells[cell_id][0]
    gene = genome[gene_id]
    global adult_genome_len

    command_num = categorise(gene[command_start_ind], 8)
    command_X = gene[command_start_ind + 1]
    command_Y = gene[command_start_ind + 2]
    command_Success = False

    if command_num == 0:
        command_Success = True
    if command_num == 1:
        command_X = categorise(command_X, (adult_genome_len - 1) *2)
        if command_X < adult_genome_len:
            set_new_root_gene(cell_id,command_X)
        else:
            set_new_root_gene(cell_id,gene_id)
        command_Success = True
    if command_num == 2:
        return (0,1)
    if command_num == 3:
        command_X = categorise(command_X, 4)
        cells[cell_id][0]["heading"] = ((cells[cell_id][0]["heading"]-1 + command_X) % 4) + 1
        command_Success = True
    if command_num == 4:
        split_from_parent(cell_id)
        command_Success = True

    return (4, command_Success)

def genome_get_next_gene(cell_id, condition,command, genome_start, genome_end):
    command = int(command)
    condition = int(condition)
    command = command << 1
    sum = command + condition
    next_gene_dict = {0:10, 1:15, 2:9, 3:14}
    next_gene_bare = next_gene_dict[sum]
    next_gene = genome_start + categorise(next_gene_bare,genome_end)
    return (9,next_gene)

def genome_grow_seed(cell_id):
    active_gene = 0
    turn_stem_from_seed(cell_id, active_gene)
    return 0

def genome_grow(cell_id,gene_id):
    cell =  cells[cell_id][0]
    gene = get_genome(cell_id)
    gene = gene[gene_id]
    new_cell_type = "я котик ты котик"
    if cell["energy"] > 100:
        grow_success = 0
        for i in range(0,3):
            grow = False
            abs_heading = get_abs_heading(cell["heading"], i + 1)
            if gene[i] // 32 <= 2:
                new_cell_type = "stem"
                grow = True
            elif gene[i] // 32 == 4:
                new_cell_type = "leaf"
                grow = True
            elif gene[i] // 32 == 5:
                new_cell_type = "seed"
                grow = True

            if grow:
                energy_to_give = energy_cons[new_cell_type] * 2
                grow_success += grow_cell(cell_id, abs_heading, new_cell_type, energy_to_give)
        if grow_success > 0:
            turn_branch(cell_id)
    return 0

def  genome_traverse_M(cell_id, active_gene, depth):
    global adult_genome_len
    global total_genome_len
    global seed_genome_len
    """
    condition_loc = 3
    condition_X_loc = 4
    condition_Y_loc = 5

    command_1_loc = 6
    command_1_X_loc = 7
    command_1_Y_loc = 8

    gene_1_loc = 9
    gene_2_loc = 10

    command_1_loc = 11
    command_1_X_loc = 12
    command_1_Y_loc = 13

    gene_3_loc = 14
    gene_4_loc = 15
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
    command_id = "та не ври"
    command_success = "ну офигеть теперь"
    next_gene = 69
    depth += 1


    next = 1

    next = 2 * (1 + (depth < total_genome_len)) - 3

    while (next > 0 ):
        match(next):
            case 1:
                next, condition_success = genome_conditions(cell_id,active_gene)
                command_id = 6 + 5*condition_success
            case 2:
                next, command_success = genome_commands(cell_id,active_gene,command_id)
            case 3:
                next, command_success = genome_commands_seed(cell_id,active_gene,command_id)
            case 4:
                next, next_gene = genome_get_next_gene(cell_id,condition_success,command_success,0,adult_genome_len-1)
            case 5:
                next, next_gene = genome_get_next_gene(cell_id,condition_success,command_success,adult_genome_len,total_genome_len-1)
            case 6:
                next = genome_grow(cell_id,active_gene)
            case 7:
                 next = genome_grow_seed(cell_id)
            case 9:
                next = genome_traverse_M(cell_id, next_gene, depth)
            case -1:
                print(" БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
                print(" БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
                print(" БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
                print(" БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
                print(" БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
                kill_cell(cell_id)
                next = 0
                return 0
            case 0:
                return 0
            case _:
                while True:
                    print("АХАХАХАХАХХАХАХАХАХХА")
    return 0




def genome_traverse(cell_id, active_gene=0, root_gene = -1, depth = 0):
    global adult_genome_len
    cell = cells[cell_id][0]
    genome = get_genome(cell_id)
    if active_gene >= adult_genome_len:
        active_gene = adult_genome_len-1
        return root_gene, depth

    gene = genome[active_gene]
    grow = False
    new_cell_type = "none"

    if depth > 50:
        print(" БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
        print(" БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
        print(" БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
        print(" БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
        print(" БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
        kill_cell(cell_id)
        return root_gene, depth
    depth += 1


    if cell["type"] == "stem":

        condition_num = categorise(gene[3],8)
        if condition_num < 5:
            condition_X = gene[4]
            condition_Y = gene[5]
            condition_Success = False

            if condition_num == 0:
                condition_Success = True
            if condition_num == 1:
                if cell["energy"] > condition_X:
                    condition_Success = True
            if condition_num == 2:
                condition_Success = is_nearby_foreign_cells(cell_id)
            if condition_num == 999999999:
                condition_X = 0
                heading = get_abs_heading(cell["heading"],condition_X)-1
                condition_Success = is_cell_near(cell_id,heading)
            if condition_num == 3:
                condition_X = categorise(condition_X,3)
                моль = {0:1, 1:2, 2:3, 3:2}
                heading = get_abs_heading(cell["heading"], моль[condition_X]) - 1
                condition_Y = categorise(condition_Y,11)
                муха = {0: "stem", 1: "bnch", 2: "leaf", 3: "root", 4:"sead", 5:"яша"}
                if condition_Y > 4:
                    condition_Success = is_cell_near(cell_id,heading)
                else:
                    condition_Success = is_particular_cell_near(cell_id, heading, муха[condition_Y])
            if condition_num == 4:
                radius = categorise(condition_X,32)
                cells_nearby = get_cells_in_radius(cell_id,radius)
                cells_count = 0
                for i in cells_nearby:
                    if i != 0:
                        cells_count += 1
                if cells_count > condition_Y:
                    condition_Success = True




            command_start_ind = 11
            if condition_Success:
                command_start_ind = 6

            command_num = categorise(gene[command_start_ind], 8)
            command_X = gene[command_start_ind+1]
            command_Y = gene[command_start_ind+1]
            command_Success = False

            if command_num == 0:
                command_Success = True
            if command_num == 1:
                command_X = categorise(command_X, adult_genome_len-1 )
                if command_X < adult_genome_len:
                    root_gene = command_Y
                else:
                    root_gene = active_gene
                command_Success = True
            if command_num == 2:
                return root_gene, depth
            if command_num == 3:
                command_X = categorise(command_X, 4)
                cells[cell_id][0]["heading"] = (cells[cell_id][0]["heading"]+command_X) % 4 + 1
                command_Success = True
            if command_num == 4:
                split_from_parent(cell_id)
                command_Success = True



            next_gene_ind = 0
            if condition_Success:
                next_gene_ind = 9
                if command_Success:
                    next_gene_ind += 1
            elif not condition_Success:
                next_gene_ind = 9
                if command_Success:
                    next_gene_ind += 1
            else:
                print("ЩО ТИ НАКОЇВ, ДІДЬКО")
                input()

            next_gene = gene[next_gene_ind]
            next_gene = categorise(next_gene, adult_genome_len-1)
            if next_gene != active_gene:
                root_gene, depth = genome_traverse(cell_id, next_gene, root_gene, depth)
            return root_gene, depth

        else:

            if cell["energy"] > 100:
                grow_success = 0
                for i in range(0,3):
                    grow = False
                    abs_heading = get_abs_heading(cell["heading"], i+1)
                    if gene[i]//32 <= 2:
                        new_cell_type = "stem"
                        grow = True
                    elif gene[i]//32 == 4:
                        new_cell_type = "leaf"
                        grow = True
                    elif gene[i]// 32 == 5:
                        new_cell_type = "seed"
                        grow = True

                    if grow:
                        energy_to_give = energy_cons[new_cell_type]  *  2
                        grow_success += grow_cell(cell_id, abs_heading, new_cell_type, energy_to_give )
                if grow_success > 0:
                    turn_branch(cell_id)

        return root_gene, depth
    return root_gene, depth

def genome_traverse_seed_ТОРЧ(cell_id, active_gene=0, root_gene = -1, depth = 0):
    turn_stem_from_seed(cell_id, active_gene)
    global adult_genome_len
    if active_gene >= adult_genome_len:
        return 0, "lol"
    return active_gene, "lol"

def genome_traverse_seed(cell_id, active_gene=0, root_gene = -1, depth = 0):

    global adult_genome_len
    global seed_genome_len

    if active_gene < adult_genome_len or root_gene < adult_genome_len:
        active_gene = adult_genome_len
        root_gene = adult_genome_len

    cell = cells[cell_id][0]
    genome = get_genome(cell_id)
    gene = genome[active_gene]
    grow = False
    new_cell_type = "none"

    if depth > 20:
        print(" БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
        print(" БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
        print(" БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
        print(" БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
        print(" БЕСКОНЕЧНЫЙ ЛУП В ГЕНОМЕ")
        kill_cell(cell_id)
        return root_gene, depth
    depth += 1


    if cell["type"] == "seed":

        condition_num = categorise(gene[3],8)
        if condition_num < 5:
            condition_X = gene[4]
            condition_Y = gene[5]
            condition_Success = False

            if condition_num == 0:
                condition_Success = True
            if condition_num == 1:
                if cell["energy"] > condition_X:
                    condition_Success = True
            if condition_num == 2:
                condition_Success = is_nearby_foreign_cells(cell_id)
            if condition_num == 999999999:
                condition_X = 0
                heading = get_abs_heading(cell["heading"],condition_X)-1
                condition_Success = is_cell_near(cell_id,heading)
            if condition_num == 3:
                condition_X = categorise(condition_X,3)
                моль = {0:1, 1:2, 2:3, 3:2}
                heading = get_abs_heading(cell["heading"], моль[condition_X]) - 1
                condition_Y = categorise(condition_Y,11)
                муха = {0: "stem", 1: "bnch", 2: "leaf", 3: "root", 4:"sead", 5:"яша"}
                if condition_Y > 4:
                    condition_Success = is_cell_near(cell_id,heading)
                else:
                    condition_Success = is_particular_cell_near(cell_id, heading, муха[condition_Y])
            if condition_num == 4:
                radius = categorise(condition_X,32)
                cells_nearby = get_cells_in_radius(cell_id,radius)
                cells_count = 0
                for i in cells_nearby:
                    if i != 0:
                        cells_count += 1
                if cells_count > condition_Y:
                    condition_Success = True




            command_start_ind = 11
            if condition_Success:
                command_start_ind = 6

            command_num = categorise(gene[command_start_ind], 8)
            command_X = gene[command_start_ind+1]
            command_Y = gene[command_start_ind+1]
            command_Success = False

            if command_num == 0:
                command_Success = True
            if command_num == 1:
                command_X = categorise(command_X, adult_genome_len*2 )
                if command_X < adult_genome_len:
                    root_gene = command_Y
                else:
                    root_gene = active_gene
            if command_num == 2:
                return root_gene, depth
            if command_num == 3333333333:
                command_X = categorise(command_X, 4)
                cells[cell_id][0]["heading"] = (cells[cell_id][0]["heading"]+command_X) % 4 + 1



            next_gene_ind = 0
            if condition_Success:
                next_gene_ind = 9
                if command_Success:
                    next_gene_ind += 1
            elif not condition_Success:
                next_gene_ind = 9
                if command_Success:
                    next_gene_ind += 1
            else:
                print("ЩО ТИ НАКОЇВ, ДІДЬКО")
                input()

            next_gene = gene[next_gene_ind]
            next_gene = adult_genome_len + categorise(next_gene, seed_genome_len-1)
            if next_gene != active_gene:
                root_gene, depth = genome_traverse(cell_id, next_gene, root_gene, depth)
            return root_gene, depth

        else:

            turn_stem_from_seed(cell_id,0)

        return root_gene, depth

def is_cell_near(cell_id, heading):
    global fieldSize
    current_cell = cells[cell_id][0]
    x, y = current_cell["xy"]

    if x-1 < 0 or y-1 <0 or x+1 >= fieldSize or y+1 >= fieldSize:
        return True
    field_XY = [[x, y - 1], [x + 1, y], [x + 1, y], [x - 1, y]]

    x2, y2 = field_XY[heading]
    if field[x2][y2][0] != 0:
        return True
    return False

def is_particular_cell_near(cell_id, heading, type):
    current_cell = cells[cell_id][0]
    x, y = current_cell["xy"]
    field_XY = [[x, y - 1], [x + 1, y], [x + 1, y], [x - 1, y]]

    x2, y2 = field_XY[heading]
    if field[x2][y2][0] != 0:
        if cells[field[x2][y2][0]][0]["type"] == type:
            return True
    return False


def consume_energy(cell_id):
    cell = cells[cell_id][0]
    cells[cell_id][0]["energy"] -= energy_cons[cell["type"]]

def consume_energy_LEGACY(cell_ind):
    cell = cells[cell_ind][0]
    cells[cell_ind][0]["energy"] = cell["energy"] - cell["energy consumption"]
    if cells[cell_ind][0]["energy"] < 0:
        return 1
    return 0

def produce_energy(cell_id):
    global energy_prod
    cell = cells[cell_id][0]
    if cell["type"] == "root":
        cells[cell_id][0]["energy"] += яша
    cells[cell_id][0]["energy"] += energy_prod[cell["type"]]

def produce_energy_LEGACY(cell_ind):
    global яша
    cell = cells[cell_ind][0]
    if cell["energy"] < 200:
        if cell["type"] == "leaf":
            cells[cell_ind][0]["energy"] += 15
        elif cell["type"] == "root":
            cells[cell_ind][0]["energy"] += яша


def organics_check(cell):
    xy = cell["xy"]
    if field[xy[0]][xy[1]][1] > 64:
        return 1
    return 0

def death_check(cell_id):
    cell = cells[cell_id][0]
    die = -2

    if cell["energy"] < -10 or cell["energy"] > 950 :
        die = 1
    elif cell["type"] == "bnch":
        for i in range(1,4):

            link = get_abs_heading(cell["heading"],i)-1
            if cell["linksB"][link] == 0:
                die += 1

    if die > 0:
        kill_cell(cell_id)

def upd_cell(cell_ind):
    death = 0
    cell = cells[cell_ind][0]
    consume_energy(cell_ind)
    genome_handle(cell_ind)

    move_energy_b(cell_ind)

    death_check(cell_ind)
    produce_energy(cell_ind)




def get_cells_in_radius(cell_id, radius):
    if radius < 0:
        raise ValueError("радиус меньше нуля")

    if radius == 0:
        return [cell_id]

    x0, y0 = cells[cell_id][0]["xy"]

    x2 = 0
    res = [0] * (radius * radius * 4 * 2  )
    for i in range(-radius, radius + 1):
        for j in range(-(radius - abs(i)), radius + 1 - abs(i)):
            x = x0 + i
            y = y0 + j
            if 0 <= x < fieldSize and 0 <= y < fieldSize:
                res[x2] = field[x][y][0]
                x2 += 1

    return res


def get_cells_in_radius2(cell_id, radius):
    if radius < 0:
        raise ValueError("радиус меньше нуля")

    if radius == 0:
        return [cell_id]


    x0, y0 = 5, 5
    k = 0
    res = [0] * (2 * (radius + 1)) ** 2
    for i in range(-radius, radius + 1):
        for j in range(-radius, radius + 1):
            x = x0 + i
            y = y0 + j
            if 0 <= x < fieldSize and 0 <= y < fieldSize:
                res[k] = field[x][y][0]
                k += 1

    return res



def get_abs_heading(abs_rot, nada_rot):
    if abs_rot == 0:
        return nada_rot
    adekvat_cord = {1: -1, 2: 0, 3: 1, 4: 2}
    res = (abs_rot + adekvat_cord[nada_rot]) % 4
    if res == 0:
        res = 4
    return res

def get_nearby_cells(cell_id):
    current_cell = cells[cell_id][0]
    nearby_cells = [0, 0, 0, 0]
    x, y = current_cell["xy"]

    nearby_cells[0] = field[x][y-1][0]
    nearby_cells[1] = field[x+1][y][0]
    nearby_cells[2] = field[x][y + 1][0]
    nearby_cells[3] = field[x - 1][y][0]
    return nearby_cells

def is_nearby_any_cells(cell_id):
    current_cell = cells[cell_id][0]
    x, y = current_cell["xy"]
    field_XY = [[x, y - 1], [x + 1, y], [x + 1, y], [x - 1, y]]

    for i in range(4):
        nearby_cell_id = field[field_XY[i][0]][field_XY[i][1]][0]
        if nearby_cell_id != 0:
            return True
    return False

def is_nearby_foreign_cells(cell_id):
    current_cell = cells[cell_id][0]
    x, y = current_cell["xy"]
    field_XY = [[x, y - 1], [x + 1, y], [x + 1, y], [x - 1, y]]

    for i in range(4):
        nearby_cell_id = field[field_XY[i][0]][field_XY[i][1]][0]
        nearby_cell = cells[nearby_cell_id][0]
        if nearby_cell["genome"] != current_cell["genome"]:
            return True
    return False

def get_nearby_foreign_cells(cell_id):
    current_cell = cells[cell_id][0]
    nearby_cells = [0, 0, 0, 0]
    x, y = current_cell["xy"]
    field_XY = [[x,y-1],[x+1,y],[x+1,y],[x - 1,y]]

    for i in range(4):
        nearby_cell_id = field[field_XY[i][0]][field_XY[i][1]][0]
        nearby_cell = cells[nearby_cell_id][0]

        if nearby_cell["genome"] != current_cell["genome"]:
            nearby_cells[0] = nearby_cell_id
    return nearby_cells

def get_f_links_LEGACY(cell_id):
    current_cell = cells[cell_id][0]
    links = [0,0,0,0]
    test_bit = 1

    for shift in range(4):
        if (test_bit << shift & current_cell["links"] > 0):
            links[shift] = 1
    return links



def get_linked_cells_LEGACY(cell_id):
    current_cell = cells[cell_id][0]
    linked_cells =get_f_links_LEGACY(cell_id)
    x, y = current_cell["xy"]
    nearby_cells = get_nearby_cells(cell_id)


    for i in range(4):
        nearby_cells[i] = linked_cells[i] * nearby_cells[i]

    return nearby_cells

def move_energy_b(cell_id):
    current_cell = cells[cell_id][0]

    if current_cell["type"] != "stem" and current_cell["type"] != "none":
        nearby_cells = current_cell["linksB"]
        f_nearby_cells = [[0, 0] for i in range(4)]


        for i in range(4):
            tmp_cell_id = nearby_cells[i]
            tmp_cell = cells[tmp_cell_id][0]

            f_nearby_cells[i][1] = tmp_cell["energy"]
            if tmp_cell_id == 0 or tmp_cell["type"] == "leaf":
                f_nearby_cells[i][0] = False
            else:
                f_nearby_cells[i][0] = True

        free_energy = int(current_cell["energy"]/ 2)
        free_energy = current_cell["energy"]
        own_energy = current_cell["energy"] - free_energy


        rem_energy, o_nearby_cells = move_energy_core(f_nearby_cells, free_energy )
        cells[cell_id][0]["energy"] = rem_energy + own_energy

        for i in range(4):
            tmp_cell_id = nearby_cells[i]
            cells[tmp_cell_id][0]["energy"] = o_nearby_cells[i][1]


    elif current_cell["type"] == "none":
        print()
        print("Чёт ты накосячил: попытка передать энергию из пустой клетки (чекай move_energy_b)")
        input("Нажми enter что бы продолжить ")



def move_energy_LEGACY(cell_id):

    current_cell = cells[cell_id][0]
    if current_cell["type"] != "stem" or current_cell["type"] != "none":
        nearby_cells = get_nearby_cells(cell_id)
        nearby_cells = get_linked_cells(cell_id)
        f_nearby_cells = [[0,0] for i in range(4)]

        for i in range(4):
            tmp_cell_id = nearby_cells[i]
            tmp_cell = cells[tmp_cell_id][0]


            f_nearby_cells[i] = [True, tmp_cell["energy"]]
            if tmp_cell_id == 0 or tmp_cell["type"] == "leaf":

                f_nearby_cells[i][0] = False

        rem_energy, o_nearby_cells = move_energy_core(f_nearby_cells, current_cell["energy"] )


        cells[cell_id][0]["energy"] = rem_energy


        for i in range(4):
            tmp_cell_id = nearby_cells[i]
            cells[tmp_cell_id][0]["energy"] = o_nearby_cells[i][1]


    elif current_cell["type"] == "none":
        print()
        print("Чёт ты накосячил: попытка передать энергию из пустой клетки (чекай move_energy)")
        input("Нажми enter что бы продолжить ")





def move_energy_core(arr, now_energy, want_energy=1000, min_energy=0, prioryty=None):
    if prioryty is None:
        prioryty =  {1: 0, 2: 1, 3: 2, 4: 3}

    if min_energy >= now_energy:
        return [now_energy, arr]

    averange = now_energy - min_energy

    x = 0
    for i in range(1, len(arr)+1):

        if (arr[prioryty[int(i)]][0] not in [False]):
            if ((arr[prioryty[i]][1] < now_energy) and (arr[prioryty[i]][1] < want_energy)):
                averange += arr[prioryty[i]][1]
                x += 1
    if x == 0:
        return [now_energy, arr]

    averange2 = int(averange/x)

    if averange2 > want_energy:
        averange2 = want_energy

    for i in range(1, len(arr)+1):
        if arr[prioryty[i]][0] not in [False] and arr[prioryty[i]][1] < now_energy and arr[prioryty[i]][1] < want_energy:
            arr[prioryty[i]][1] = averange2

    now_energy = min_energy + averange - averange2 * x
    return [now_energy, arr]

def next_cell(cell_id):
    return cells[cell_id][2]

def add_dead(cell_id):
    global dead_last
    global cells_len
    dead_last += 1
    dead_last = dead_last % cells_len
    dead_cells_coords[dead_last] = cell_id

def get_dead():
    global dead_current
    global cells_len
    cell_id = dead_cells_coords[dead_current]
    dead_current += 1
    dead_current = dead_current % cells_len
    return cell_id

def add_free_genome(genome_id):
    global free_genomes_last
    global free_genomes_current
    global cells_len
    free_genomes_last += 1
    free_genomes_last = free_genomes_last % cells_len
    free_genomes[free_genomes_last] = genome_id

def get_free_genome():
    global free_genomes_last
    global free_genomes_current
    global cells_len
    free_genome = free_genomes[free_genomes_current]
    free_genomes_current +=1
    free_genomes_current = free_genomes_current % cells_len
    return free_genome

def render_leaf_a(x,y):
    global rad1
    rad = rad1*2
    global block_size
    x = x+ int((block_size/2))
    y = y + int((block_size / 2))

    pygame.draw.circle(SCREEN, (0, 175, 0), (x, y), rad)
    pygame.draw.circle(SCREEN, (0, 122, 0), (x, y), rad, 3)

def render_branch_a(x,y,cell_id=0):
    global block_size
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

def render_heading(x,y,cell_id):
    global block_size
    xc = x + int((block_size / 2))
    yc = y + int((block_size / 2))
    rad = int(block_size / 2)
    col = (35, 35, 255)
    width = 6

    cell_heading = cells[cell_id][0]["heading"]

    coords = [(xc, y), (x + block_size, yc), (xc, y + block_size), (x, yc)]

    for link in range(1,5):
        if cell_heading == link:
            pygame.draw.line(SCREEN, col, coords[link-1], (xc, yc), width=width)
            pygame.draw.circle(SCREEN, col, (xc, yc), width / 2)

def render_links_debug(x,y,cell_id): 
    global block_size
    xc = x + int((block_size / 2))
    yc = y + int((block_size / 2))
    rad = int(block_size / 2)
    col = (255, 35, 35)
    width = 4


    links = cell_id["linksB"]
    coords = [(xc, y),(x + block_size, yc),(xc, y + block_size),(x, yc)]

    for link in range(4):
        if links[link] != 0:
            pygame.draw.line(SCREEN, col, coords[link], (xc, yc), width=width)


def render_stem_a(x,y,cell_id):
    global rad1
    rad = rad1
    global block_size
    xc = x+ int((block_size/2))
    yc = y + int((block_size / 2))
    col = (64, 64, 64)
    width = 3

    render_branch_a(x,y,cell_id)
    pygame.draw.circle(SCREEN, (175, 175, 175), (xc, yc), rad)
    pygame.draw.circle(SCREEN, col, (xc, yc), rad, width)

def render_seed_a(x,y,cell_id):
    global rad1
    rad = rad1
    global block_size
    xc = x+ int((block_size/2))
    yc = y + int((block_size / 2))
    col = (64, 64, 64)
    width = 2

    render_branch_a(x,y,cell_id)
    pygame.draw.circle(SCREEN, (230, 230, 0), (xc, yc), rad)
    pygame.draw.circle(SCREEN, (140, 140, 0), (xc, yc), rad, width)

def render_stem_simple(x,y):
    global block_size
    col = (255, 64, 64)
    pygame.draw.rect(SCREEN, col, (x, y, block_size, block_size))

def render_branch_simple(x,y):
    global block_size
    col = (64, 64, 64)
    pygame.draw.rect(SCREEN, col, (x, y, block_size, block_size))

def render_leaf_simple(x,y):
    global block_size
    col = (64, 255, 64)
    pygame.draw.rect(SCREEN, col, (x, y, block_size, block_size))

def render_seed_simple(x,y):
    global block_size
    col = (65, 65, 255)
    pygame.draw.rect(SCREEN, col, (x, y, block_size, block_size))

def render_monotone_simple(x,y,col):
    global block_size
    pygame.draw.rect(SCREEN, col, (x, y, block_size, block_size))

def randomize_genome_cols():
    global cells_len
    diversion = 5
    for x in range(cells_len):
            chanLevel = random.randint(0, 255)
            genomesCols[x] = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
def randomize_cols_a_bit():
    global fieldSize
    diversion = 5
    for x in range(fieldSize):
        for y in range(fieldSize):
            chanLevel = random.randint(240-diversion,255-diversion)
            chanDevLevel = random.randint(-diversion,diversion)
            newCol = (chanLevel+chanDevLevel,chanLevel-chanDevLevel,chanLevel)
            fieldCols[x][y][0] = newCol

def get_axy_from_fxy(fx,fy):
    global block_size
    ax = block_size * fx
    ay = block_size * fy
    return ax, ay


def render():
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    global block_size
    global render_mode
    global debug_mode
    global first_cell_LEGACY
    global fontDebugSmall
    global smallFontSize
    global debug_links
    global debug_heading
    global render_cells
    global show_button
    global console_active

    match (render_mode):
        case 0:
            pass
        case 1:
            draw_grid()
        case 1002:
            draw_grid_безымянник_эдитион(arg)
        case 3:
            SCREEN.fill((255,255,255))




    match (render_cells):
        case 0:
            pass
        case 4:
            for x in range(offset_x // block_size, ((WINDOW_WIDTH + offset_x) // block_size)):
                for y in range(offset_y // block_size,
                               ((WINDOW_WIDTH + offset_y) // block_size)):
                    if x >= fieldSize:
                        x = fieldSize - 1
                    if y >= fieldSize:
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



                    if debug_links == True:
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

                    if x == 0 or y == 0 or y == -1 or x == -1 or x == fieldSize - 1 or y == fieldSize - 1:
                        pygame.draw.rect(SCREEN, (41, 49, 51), [render_x, render_y, block_size, block_size])
          
        case 101:
            for x in range(offset_x // block_size, ((WINDOW_WIDTH + offset_x) // block_size)):
                for y in range(offset_y // block_size,
                               ((WINDOW_WIDTH + offset_y) // block_size)):
                    if x >= fieldSize:
                        x = fieldSize - 1
                    if y >= fieldSize:
                        y = fieldSize - 1
                    render_x, render_y = get_axy_from_fxy(x, y)
                    render_x -= offset_x
                    render_y -= offset_y
                    current_cell_id = field[x][y][0]

                    col = genomesCols[cells[current_cell_id][0]["genome"]]
                    render_monotone_simple(render_x, render_y, col)
                    current_cell_id = next_cell(current_cell_id)

                    if x == 0 or y == 0 or y == -1 or x == -1 or x == fieldSize - 1 or y == fieldSize - 1:
                        pygame.draw.rect(SCREEN, (41, 49, 51), [render_x, render_y, block_size, block_size])
        case 3:
            for x in range(offset_x // block_size, ((WINDOW_WIDTH + offset_x) // block_size)):
                for y in range(offset_y // block_size,
                               ((WINDOW_WIDTH + offset_y) // block_size)):
                    if x >= fieldSize:
                        x = fieldSize - 1
                    if y >= fieldSize:
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

                    if x == 0 or y == 0 or y == -1 or x == -1 or x == fieldSize - 1 or y == fieldSize - 1:
                        pygame.draw.rect(SCREEN, (41, 49, 51), [render_x, render_y, block_size, block_size])





    hide_button = create_button((87, 175, 235), 50, 50, '\/', WINDOW_WIDTH - 50, WINDOW_HEIGHT - 50, 10, 5)

    if show_button == True:
        global burger_render_mode
        pygame.draw.rect(SCREEN, (235, 235, 235), [0, 0, 210, WINDOW_HEIGHT])
        if burger_render_mode == True:
            render_base = create_button((50,109,129), 70, 70, 'r-b', 210, WINDOW_HEIGHT - 70, 10,  15)
            render_noname = create_button((50,109,129), 70, 70, 'r-n', 280, WINDOW_HEIGHT - 70, 10,  15)
            render_simple = create_button((50,109,129), 70, 70, 'r-s', 350, WINDOW_HEIGHT - 70, 10,  15)

            if render_cells == 4: 
                bdebug_links = create_button((70,129,149), 70, 70, 'd-l', 210, WINDOW_HEIGHT - 140, 10, 15)
                bdebug_heading = create_button((70,129,149), 70, 70, 'd-h', 280, WINDOW_HEIGHT - 140, 10, 15)
                bdebug_mode = create_button((70,129,149), 70, 70, 'd-m', 350, WINDOW_HEIGHT - 140, 10, 15)
        burger_render = create_button((30,89,109), 70, 70, '=', 140, WINDOW_HEIGHT - 70, 15, 15) 
      
        if running == False:
            next_step = create_button((97, 175, 235), 50, 70, '>', 70, WINDOW_HEIGHT - 70, 15, 15)
        pause = create_button((117, 195, 255), 70, 70, '||', 0, WINDOW_HEIGHT - 70, 15, 15)

        interval_0 = create_button((182, 225, 252), 50, 50, '0', 0, 0, 10, 10)
        interval_1 = create_button((132, 205, 250), 50, 50, '1', 50, 0, 10, 10)
        interval_2 = create_button((84, 185, 247), 50, 50, '2', 100, 0, 10, 10)

        offset_y_up = create_button((204, 185, 247), 50, 50, '^', 50, 150, 10, 10)
        offset_x_left = create_button((204, 185, 247), 50, 50, '<', 10, 200, 10, 10)
        offset_x_right = create_button((204, 185, 247), 50, 50, '>', 90, 200, 10, 10)
        offset_y_down = create_button((204, 185, 247), 50, 50, '\/', 50, 250, 10, 10)

        scale_plus = create_button((204, 185, 247), 40, 40, '+', 10, 160, 10, 0)
        scale_minus = create_button((204, 185, 247), 40, 40, '-', 100, 160, 10, 0)

        sleep_btn = create_button((84, 185, 247), 150, 50, 'Sleep', 0, WINDOW_HEIGHT-120, 10, 3)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if show_button == True:
                if running == False and next_step.collidepoint(event.pos):
                    update()
                if pause.collidepoint(event.pos):
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


            if hide_button.collidepoint(event.pos):
                show_button = not (show_button)
    





    pygame.display.update()


def create_button(color, width, height, mes, x, y, textX, textY):
    button = pygame.Rect(x,y,width, height)

    color_light = (min(color[0] + 40, 255), min(color[1] + 40, 255), min(color[2] + 40, 255))


    text = font_button.render(mes, True, (255,255,255))

    if x <= pygame.mouse.get_pos()[0] <= x + width and y <= pygame.mouse.get_pos()[1] <= y + height:
            pygame.draw.rect(SCREEN, color_light, [x, y, width, height])
    else:
            pygame.draw.rect(SCREEN, color, [x, y, width, height])
    SCREEN.blit(text, (x + textX, y + textY))

    return button

def buttons_react_LEGACY(react):
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

def draw_grid():
    SCREEN.fill((255,255,255))
    for x in range(0, WINDOW_WIDTH, block_size):
        for y in range(0, WINDOW_HEIGHT, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)

            pygame.draw.rect(SCREEN, BLACK, rect, 1)


def draw_grid_безымянник_эдитион(arg):
    block_size, WINDOW_WIDTH, WINDOW_HEIGHT, BLACK = arg
    global fieldSize


    for fx in range(0,fieldSize):
        for fy in range(0,fieldSize):
            ax = block_size * fx
            ay = block_size * fy

            rect = pygame.Rect(ax, ay, block_size, block_size)

            col = fieldCols[fx][fy][0]

            pygame.draw.rect(SCREEN, col, rect, 0)


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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

fieldSize = 300
cells_len = fieldSize ** 2

field = [[[0,0] for j in range(fieldSize)] for i in range(fieldSize)]
fieldCols = [[[(255,0,0),(255,255,255)] for j in range(fieldSize)] for i in range(fieldSize)]

cells = [[gen_empty_cell(),0,0] for _ in range(cells_len)]
first_cell_LEGACY = 1

dead_cells_coords = list(range(cells_len))
dead_current = 1
dead_last = -1
dead_last = cells_len - 1

print(dead_cells_coords)
print(dead_current)
print(dead_last)


energy_cons = {"leaf":0,"bnch":1,"none":0,"stem":5,"root":0,"seed":2}
energy_prod = {"leaf":15,"bnch":0,"none":0,"stem":0,"root":0,"seed":0}

яша = 42

adult_genome_len = 17
seed_genome_len = 5
total_genome_len = adult_genome_len+ seed_genome_len
gene_len = 18
genomes = [[[0 for ___ in range(gene_len)] for __ in range(total_genome_len) ] for _ in range(cells_len)]
genomesCols = [(255,0,0) for i in range(cells_len)]
free_genomes = list(range(cells_len))
free_genomes_current = 1
free_genomes_last = cells_len-1
genomes_usage = list(range(cells_len))



block_size = 30
render_mode = 3
render_cells = 3
debug_links = False
debug_heading = False
debug_mode = False
burger_render_mode = False
running = True
sleep_mode = 0
tick = 0
global console_active
console_active = False

console_buffer = ''

interval = 2

global offset
offset = block_size * 4

offset_x = 0
offset_y = 0

BLACK = (29, 51, 74)
WHITE = (255, 255, 255)
NEW_CELL = (52, 201, 36)

WINDOW_WIDTH = 1270
WINDOW_HEIGHT = 720
pygame.init()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()
SCREEN.fill(WHITE)
arg = block_size, WINDOW_WIDTH, WINDOW_HEIGHT, BLACK
global radl
rad1 = 0.25 * block_size
radius = float(block_size / 30)
smallFontSize = 17
fontDebugSmall = pygame.font.Font(None, smallFontSize)

global font_button
font_button = pygame.font.SysFont('Verdana', 35)

show_button = True


def setup():
    randomize_genome_cols()
    create_Бибки_debug()
    create_debug_genome()
    genome_randomize()

    pass


def update():

    global first_cell_LEGACY
    traverse = True
    current_cell_id = first_cell_LEGACY
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

        tick += 1
        print(tick, sleep_mode)



setup()
loop()



