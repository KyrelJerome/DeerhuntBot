from helper_classes import *
class GridPlayer:

    def __init__(self):
        self.foo = True

    def tick(self, game_map, your_units, enemy_units, resources, turns_left):
        workers = your_units.get_all_unit_of_type('worker')
        melees = your_units.get_all_unit_of_type('melee')
        moves = []
        for worker in workers:
            if worker != None:  
                if worker.can_mine(game_map):
                    print("Worker:" + str(worker.id))
                    moves.append(worker.mine())
                else:
                    # move worker towards resource
                    resources = game_map.closest_resources(worker)
                    print("Turn:" + str(100 - turns_left))
                    print("Resources: " + str(resources))
                    worker_path = game_map.bfs(worker.position(),resources)
                    if worker_path != None and len(worker_path) > 1:
                        print("Goal: " + str(worker_path[1]))
                        if is_open(game_map, worker_path[1], your_units, enemy_units):
                            move = worker.move_towards(worker_path[1])
                            print("Move" + str(move.to_tuple()))
                            moves.append(move)
        for melee in melees:
            if melee != None:  
                if len(melee.can_attack(enemy_units)) >= 1:
                    print("melee:" + str(melee.id))
                    moves.append(melee.mine())
                else:
                    # move worker towards resource
                    resources = game_map.closest_resources(melee)
                    print("Turn:" + str(100 - turns_left))
                    print("Resources: " + str(resources))
                    melee_path = game_map.bfs(melee.position(),resources)
                    if melee_path != None and len(melee_path) > 1:
                        print("Goal: " + str(melee_path[1]))
                        if is_open(game_map, melee_path[1], your_units, enemy_units):
                            move = melee.move_towards(melee_path[1])
                            print("Move" + str(move.to_tuple()))
                            moves.append(move)
        return moves

def is_open(game_map, position, your_units, enemy_units):
    for unit in your_units.get_all_unit_ids():
        if position == your_units.get_unit(unit).position():
            return False
    for unit in enemy_units.get_all_unit_ids():
        if position == enemy_units.get_unit(unit).position():
            return False
    return not game_map.is_wall(position[0], position[1])
    pass

'''
for melee in melees:
            if melee != None:
                
                if melee.can_attack(game_map):
                    moves.append(melee.mine())
                else:
                    # move worker towards resource
                    resources = game_map.closest_resources(melee)
                    print("Turn:" + str(100 - turns_left))
                    print("Resources: " + str(resources))
                    melee_path = game_map.bfs(melee.position(),resources)
                    print("Goal: " + str(melee_path[0]))
                    move = melee.move_towards(melee_path[1])
                    #worker_path = None
                    print("Move" + str(move.to_tuple()))
                    moves.append(move)
'''
