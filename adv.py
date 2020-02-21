from room import Room
from player import Player
from world import World
from utils import Queue, Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

visited = {}

def map_traversal(): 
    while len(visited) < len(room_graph):
        current_room = player.current_room
        current_room_id = player.current_room.id
        current_exits = player.current_room.get_exits()
        unvisited_directions = []

        # checks if current id isn't in visited
        if current_room_id not in visited:
            room_exits = {}
            for i in current_exits:
                room_exits[i] = "?"
            visited[current_room_id]= room_exits

        # unvisited exits added to unvisited_directions list    
        for i in visited[current_room_id]:
            if visited[current_room_id][i] == '?':
                unvisited_directions.append(i)

        # checks for unvisited rooms from current
        if len(unvisited_directions) > 0:
            #Gives player random direction to move in unvisited rooms
            random_index = random.randint(0, len(unvisited_directions) - 1)
            random_direction = unvisited_directions[random_index]
            player.travel(random_direction)
            traversal_path.append(random_direction)
            # saves current room id, and exits
            new_traveled_id = player.current_room.id
            new_traveled_exits = player.current_room.get_exits()

            if new_traveled_id not in visited:
                new_room_exits = {}
                for i in new_traveled_exits:
                    new_room_exits[i] = "?"
                visited[new_traveled_id] = new_room_exits

            reverse = direction_reversal(random_direction)
            visited[current_room_id][random_direction] = new_traveled_id
            visited[new_traveled_id][reverse] = current_room_id
 
        else:
            directions_moved = bfs(visited, current_room)

            if len(directions_moved) > 0:
                for i in directions_moved:
                    traversal_path.append(i)

    # print("END", visited)
    # print("END PATH", traversal_path)     
       
def direction_reversal(direction):
    if direction == "n":
        return 's'
    elif direction == "s":
        return 'n'
    elif direction == 'e':
        return 'w'
    elif direction == 'w':
        return 'e'

def bfs(visited, current_room):
    visited_path = set()
    queue = Queue()
    queue.enqueue([current_room.id])
    directions_used = []
    tracked_path = ''

    while queue.size() > 0:

        path = queue.dequeue()
        v = path[-1]

        unvisited_list = []
        for i in visited[v]:
            if visited[v][i] == '?':
                unvisited_list.append(i)

        if len(unvisited_list) > 0:
            tracked_path = path
            break 

        # Checks current rooms, if no unvisited exits adds checked room to visited_path
        if v not in visited_path:
            visited_path.add(v)
            for i in visited[v]:
                direction = visited[v][i]
                new_path = list(path)
                new_path.append(direction)
                queue.enqueue(new_path)

    # reverse to find which direction has the id's of each room
    # add direction to list(used_directions)

    while len(tracked_path) >= 2:
        room = tracked_path.pop(0)
        for i in visited[room]:
            if visited[room][i] == tracked_path[0]:
                directions_used.append(i)

    for i in directions_used:
        player.travel(i)
        
    return directions_used


map_traversal()


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
