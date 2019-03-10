from helper_classes import *
class GridPlayer:

    def __init__(self):
        self.foo = True
 
    def pre_game_calc(self, game_map, your_units):
        workers = your_units.get_all_unit_of_type('worker')
        melees = your_units.get_all_unit_of_type('melee')
        num_workers = your_units.get_all_unit_of_type('worker')
        num_melees = your_units.get_all_unit_of_type('worker')
        print("team resources: " + resources)
        resource_nodes = game_map.find_all_resources()
        column = len(game_map.grid[0])
        row = len(game_map.grid)
        print("MAP SIZE: {0} x {1}".format(column, row))

        enemy_distance = []
        for m in melees:
            enemy_coord = (abs(column - m.x), abs(row - m.y))
            enemy_distance.append(len(game_map.bfs(enemy_coord, resource_nodes[0])) - 1)
        self.set_safety(min(enemy_distance))

    def tick(self, game_map, your_units, enemy_units, resources, turns_left):
        protectDist =  4
        num_resources = resources
        workers = your_units.get_all_unit_of_type('worker')
        melees = your_units.get_all_unit_of_type('melee')
        num_workers = len(workers)
        num_soldiers = len(melees)
        moves = []
        
        unused_workers = your_units.get_all_unit_of_type('worker')
        print("Num of enemies" + str(len(enemy_units.units)))
        print("Turn:" + str(100 - turns_left))
        print("collected Resources: " + str(num_resources)) 
        res = game_map.find_all_resources()
        workers_to_resources = {}
        unused_workers = []
        counter = 0
        if workers != None and len(workers) > 0:
            for worker in workers:
                unused_workers.append(str(worker.id))
            output_worker_path = {}
            k = 0
            while k  < len(unused_workers) and k < len(res) and unused_workers != None and res != None:
                if unused_workers == None or res == None:
                    break;
                for worker in unused_workers:
                    shortest = (9999999999,None)
                    for r in res :
                        print("Testing path to: " + str(res))
                        print("From worker: " + worker)
                        print("Path before" + str(shortest))
                        new_path = bfs(game_map, your_units, enemy_units, your_units.get_unit(str(worker)).position(),r)
                        print("test path: " +  str(new_path))
                        if new_path != None and len(new_path) < shortest[0]:
                            shortest = (len(new_path),r)
                        print("Path after" + str(shortest))
                    workers_to_resources[str(worker)] = shortest
                j_path = ((999999999999999999,0),"workerID")
                for key in workers_to_resources:
                    print("type")
                    print(type(workers_to_resources[key][0]))
                    print(type(j_path[0][0]))
                    if workers_to_resources[key][0] < j_path[0][0]:
                        j_path = (workers_to_resources[key],key)
                output_worker_path[j_path[1]] = j_path[0][1]

                print("ok")
                print(output_worker_path)
                print(j_path[1])
                print(unused_workers)
                print(res)
                print("ok")
                unused_workers.remove(j_path[1])
                res.remove(j_path[0][1])
                k += 1
            for worker in unused_workers:
                #unused workers can Roam!!!!
                break
            for worker in output_worker_path:
                worker = your_units.get_unit(worker) 
                print("Worker:" + str(worker.id))
                parse_alertables = worker.nearby_enemies_by_distance(enemy_units)
                alertables = []
                for parse in parse_alertables:
                    if(enemy_units.get_unit(parse[0]).type == "melee"):
                        alertables.append(parse)
                #Get alerted, run from enemies within distance    
                if len(alertables) > 0 and alertables[0][1] <= 2:
                    #run
                    print("I've been spooked!" + str(alertables))
                    current_alertable = 0
                    directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
                    while current_alertable < len(alertables) and alertables[current_alertable][1] < 1:
                        direction = worker.direction_to(enemy_units.get_unit(alertables[current_alertable]).position())
                        print("Enemy found in direction: " + direction) 
                        if direction != None and  (direction in directions):
                            directions.remove(direction)
                    if len(directions) > 0:
                        print("running away, to: " + directions[0])
                        moves.append(worker.move(directions[0]))
                # If its safe to, and you can mine, mine
                elif worker.can_mine(game_map):
                    print("Mining:" + str(worker.id))
                    moves.append(worker.mine())
                # If its safe to go wherever and you can mine, go to the drug dropoff
                else:
                    # get path
                    print(worker.position())
                    worker_path = bfs(game_map, your_units, enemy_units, worker.position(),output_worker_path[str(worker.id)])
                    if worker_path != None and len(worker_path) > 1:
                        print("Goal: " + str(worker_path[1]))
                        #move
                        if is_open(game_map, worker_path[1], your_units, enemy_units):
                            move = worker.move_towards(worker_path[1])
                            print("Move" + str(move.to_tuple()))
                            moves.append(move)
                    else:
                        print("worker_path is None or 0")
        #Guard dog and sentry code
        is_guarding =  False
        guarded = {}
        guardedL = {}
        for worker in workers:
            distance_pair =  worker.nearby_enemies_by_distance(your_units)
            print("Pairs for worker: " + str(worker.id))
            print(str(len(distance_pair)))
            print(distance_pair)
            for pair in distance_pair:
                if pair[1] < protectDist and your_units.get_unit(pair[0]).type == 'melee':
                    print("adding pair: " + str(pair))
                    if worker.id not in guarded.keys():
                        print("created list for worker")
                        guarded[worker.id] = [pair[0]]
                        guardedL[worker.id] = [pair[1]]
                    else:
                        
                        print("added to list for worker")
                        guarded[worker.id].append(pair[0])
                        guardedL[worker.id] = [pair[1]]
                    if len(guarded[worker.id])  > 3:
                        break
        attackers = []
        for melee in melees:
            if melee != None:
                isAttacking = False
                targets = melee.can_attack(enemy_units)
                print("")
                print("Melee at" + str(melee.position())+ ": " + str(melee.id))
                # if you can hit someone, hit that man bruh
                if len(targets) >= 1 :
                    target = targets[0][0]
                    print("Attacking: " + str(melee.id) + " to " +   str(target.id))
                    moves.append(melee.attack(melee.direction_to(target.position())))
                    isAttacking = True
                    attackers.append(melee)
                else:
                    enemies = melee.nearby_enemies_by_distance(enemy_units)
                    print("total enemies" + str(len(enemy_units.units)) + " , nearby enemies:" + str(len(enemies)) )
                    if len(enemies) >= 1:
                        attackers.append(melee)
                        isAttacking = True
                        enemy = enemy_units.get_unit(enemies[0][0])# enemies is a unit
                        print("enemy position: " + str(enemy.position()))
                        melee_path = bfs(game_map, your_units, enemy_units, melee.position(),enemy.position())
                        if melee_path != None and len(melee_path) > 2:
                            print("Next Position: " + str(melee_path[1]))
                            if is_open(game_map, melee_path[1], your_units, enemy_units):
                                move = melee.move_towards(melee_path[1])
                                print("Move" + str(move.to_tuple()))
                                moves.append(move)
                            else:
                                print("bfs sucks kyrel, this shouldnt ever happen")
                        else:
                            print("Bruh that shit none!")
                    else:
                        
                        is_guarding = False
                        guarding = None
                        for key in guarded.keys():
                            print(str(key) + "guarded by:" + str(guarded[key]))
                            if str(melee.id) in guarded[key]:
                                print("Melee is guarding!")
                                is_guarding = True
                                guarding = your_units.get_unit(str(key))
                                break;
                        if is_guarding:
                            move = melee.move_towards(guarding.position())
                            moves.append(move)
                        elif len(melees) <  num_resources*num_workers//2 : #len(resources)*num_melees:
                            teammates = melee.nearby_enemies_by_distance(your_units)
                            if len(teammates) >= 1 and melee.can_duplicate(num_resources):
                                directions = []
                                for teammate in teammates:# find viable direction to teammates
                                    direction = melee.direction_to(your_units.get_unit(teammate[0]).position())
                                    if direction != None and (not direction in directions ):
                                        directions.append(direction)
                                for direction in ('UP', 'DOWN', 'LEFT', 'RIGHT'):
                                    if not (direction in directions):
                                        directions.append(direction)
                                print("directions: " + str(directions))
                                for direction in directions:
                                    print("direction" + str(direction))
                                    goal = coordinate_from_direction(melee.position()[0], melee.position()[1], direction)
                                    if goal == None:
                                      print("goal is none")
                                    if goal != None and is_open(game_map,goal, your_units, enemy_units):
                                        moves.append(melee.duplicate(direction))
                                        break;
                                    break;
        print("moves")
        for move in moves:
            print("move:" + str(move.to_tuple()))
        return moves

def is_open(game_map, position, your_units, enemy_units):
    for unit_id in your_units.get_all_unit_ids():
        if position == your_units.get_unit(unit_id).position():
            return False
    for unit_id in enemy_units.get_all_unit_ids():
        if position == enemy_units.get_unit(unit_id).position():
            return False
    return not game_map.is_wall(position[0], position[1])

def bfs(game_map, your_units, enemy_units, start: (int, int), dest: (int, int)) -> [(int, int)]:
    """(Map, (int, int), (int, int)) -> [(int, int)]
    Finds the shortest path from <start> to <dest>.
    Returns a path with a list of coordinates starting with
    <start> to <dest>.
    """
    graph = game_map.grid
    queue = [[start]]
    vis = set(start)
    if start == dest or graph[start[1]][start[0]] == 'X' or \
            not (0 < start[0] < len(graph[0])-1
                 and 0 < start[1] < len(graph)-1):
        return [start]

    while queue:
        path = queue.pop(0)
        node = path[-1]
        r = node[1]
        c = node[0]

        if node == dest:
            return path
        for adj in ((c+1, r), (c-1, r), (c, r+1), (c, r-1)):
            if (is_open(game_map, adj, your_units, enemy_units ) or
                    graph[adj[1]][adj[0]] == 'R') and adj not in vis:
                queue.append(path + [adj])
                vis.add(adj)
