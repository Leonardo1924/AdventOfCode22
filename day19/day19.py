#read file
with open("input.txt") as f:
    data = f.read().splitlines()
    
def parse_blueprint(blueprint_strings):

    # Initialize an empty list to hold the component lists
    blueprint_list = []

    # Iterate through each line of the blueprint
    for line in blueprint_strings:
        # Split the line into a list of words
        words = line.split()
        robot_list = []
        # Iterate through each word in the line
        for i in range(len(words)):
            if words[i] == "robot":
                components = [0, 0, 0]
                continue
            if words[i][:3] == "ore" and words[i-1].isdigit():
                components[0] = int(words[i-1])
            elif words[i][:4] == "clay" and words[i-1].isdigit():
                components[1] = int(words[i-1])
            elif words[i][:8] == "obsidian" and words[i-1].isdigit():
                components[2] = int(words[i-1])
            if words[i][-1] == ".":
                robot_list.append(components)
        blueprint_list.append(robot_list)
    return blueprint_list


from z3 import *
def solve(t,blueprint):
    # Variables
    t = t # Number of time stamps
    ore = [Int("ore_{}".format(i)) for i in range(t+1)]  # Amount of ore at each time stamp
    clay = [Int("clay_{}".format(i)) for i in range(t+1)]  # Amount of clay at each time stamp
    obsidian = [Int("obsidian_{}".format(i)) for i in range(t+1)]  # Amount of obsidian at each time stamp
    geode = [Int("geode_{}".format(i)) for i in range(t+1)]  # Amount of geodes at each time stamp

    ore_robot = [Int("ore_r_{}".format(i)) for i in range(t+1)]  # Amount of robot that produce ore at each time stamp
    clay_robot = [Int("clay_r_{}".format(i)) for i in range(t+1)]  # Amount of robot that produce clay at each time stamp
    obsidian_robot = [Int("obsidian_r_{}".format(i)) for i in range(t+1)]  # Amount of robot that produce obsidian at each time stamp
    geode_robot = [Int("geode_r_{}".format(i)) for i in range(t+1)]  # Amount of robot that produce geodes at each time stamp

    buy_ore_robot = [Int("buy_ore_r_{}".format(i)) for i in range(t+1)]  # Amount of robot to buy produce ore at each time stamp
    buy_clay_robot = [Int("buy_clay_r_{}".format(i)) for i in range(t+1)]  # Amount of robot to buy produce clay at each time stamp
    buy_obsidian_robot = [Int("buy_obsidian_r_{}".format(i)) for i in range(t+1)]  # Amount of robot to buy produce obsidian at each time stamp
    buy_geode_robot = [Int("buy_geode_r_{}".format(i)) for i in range(t+1)]  # Amount of robot to buy produce geodes at each time stamp



    # Constraints
    constraints = []

    # Initial amount of minerals is 0
    constraints.append(ore[0] == 0)
    constraints.append(clay[0] == 0)
    constraints.append(obsidian[0] == 0)
    constraints.append(geode[0] == 0)


    # At each time stamp, the amount of mineral is the previous amount plus the income from the robots minus the cost of buying a new robot 
    for i in range(1, t+1):
        constraints.append(ore[i] == ore[i-1] + ore_robot[i-1] 
            - (buy_ore_robot[i-1])*blueprint[0][0] 
            - (buy_clay_robot[i-1])*blueprint[1][0] 
            - (buy_obsidian_robot[i-1])*blueprint[2][0] 
            - (buy_geode_robot[i-1])*blueprint[3][0])

        constraints.append(clay[i] == clay[i-1] + clay_robot[i-1]
            - (buy_ore_robot[i-1])*blueprint[0][1]
            - (buy_clay_robot[i-1])*blueprint[1][1]
            - (buy_obsidian_robot[i-1])*blueprint[2][1]
            - (buy_geode_robot[i-1])*blueprint[3][1])


        constraints.append(obsidian[i] == obsidian[i-1] + obsidian_robot[i-1]
            - (buy_ore_robot[i-1])*blueprint[0][2]
            - (buy_clay_robot[i-1])*blueprint[1][2]
            - (buy_obsidian_robot[i-1])*blueprint[2][2]
            - (buy_geode_robot[i-1])*blueprint[3][2])


        constraints.append(geode[i] == geode[i-1] + geode_robot[i-1])
    # Can buy only if the amount of minerals is enough
    for i in range(1, t+1):
        constraints.append(buy_ore_robot[i]*blueprint[0][0] <= ore[i])
        constraints.append(buy_clay_robot[i]*blueprint[1][0] <= ore[i])
        constraints.append(buy_obsidian_robot[i]*blueprint[2][0] <= ore[i])
        constraints.append(buy_geode_robot[i]*blueprint[3][0] <= ore[i])

        constraints.append(buy_ore_robot[i]*blueprint[0][1] <= clay[i])
        constraints.append(buy_clay_robot[i]*blueprint[1][1] <= clay[i])
        constraints.append(buy_obsidian_robot[i]*blueprint[2][1] <= clay[i])
        constraints.append(buy_geode_robot[i]*blueprint[3][1] <= clay[i])

        constraints.append(buy_ore_robot[i]*blueprint[0][2] <= obsidian[i])
        constraints.append(buy_clay_robot[i]*blueprint[1][2] <= obsidian[i])
        constraints.append(buy_obsidian_robot[i]*blueprint[2][2] <= obsidian[i])
        constraints.append(buy_geode_robot[i]*blueprint[3][2] <= obsidian[i])
    # Can take a new robot if the amount of minerals is enough
    for i in range(1, t+1):    
        constraints.append(ore_robot[i] == ore_robot[i-1] + buy_ore_robot[i-1])
        constraints.append(clay_robot[i] == clay_robot[i-1] + buy_clay_robot[i-1])
        constraints.append(obsidian_robot[i] == obsidian_robot[i-1] + buy_obsidian_robot[i-1])
        constraints.append(geode_robot[i] == geode_robot[i-1] + buy_geode_robot[i-1])

    for i in range(1, t+1):
        constraints.append(buy_ore_robot[i] <= 1)
        constraints.append(buy_clay_robot[i] <= 1)
        constraints.append(buy_obsidian_robot[i] <= 1)
        constraints.append(buy_geode_robot[i] <= 1)

        constraints.append(ore[i] >= 0)
        constraints.append(clay[i] >= 0)
        constraints.append(obsidian[i] >= 0)
        constraints.append(geode[i] >= 0)

        constraints.append(ore_robot[i] >= 0)
        constraints.append(clay_robot[i] >= 0)
        constraints.append(obsidian_robot[i] >= 0)
        constraints.append(geode_robot[i] >= 0)

        constraints.append(buy_ore_robot[i] >= 0)
        constraints.append(buy_clay_robot[i] >= 0)
        constraints.append(buy_obsidian_robot[i] >= 0)
        constraints.append(buy_geode_robot[i] >= 0)

        #buy mux a robot per turn
        constraints.append(buy_ore_robot[i] + buy_clay_robot[i] + buy_obsidian_robot[i] + buy_geode_robot[i] <= 1)
    #Start with a robot
    constraints.append(ore_robot[0] == 1)
    constraints.append(clay_robot[0] == 0)
    constraints.append(obsidian_robot[0] == 0)
    constraints.append(geode_robot[0] == 0)

    constraints.append(buy_ore_robot[0] == 0)
    constraints.append(buy_clay_robot[0] == 0)
    constraints.append(buy_obsidian_robot[0] == 0)
    constraints.append(buy_geode_robot[0] == 0)

    constraints.append(ore[0] == 0)
    constraints.append(clay[0] == 0)
    constraints.append(obsidian[0] == 0)
    constraints.append(geode[0] == 0)

    # Objective: maximize the amount of geode[t] at time t=100
    objective = geode[t]

    

    # Solve the problem
    solver = Optimize()
    solver.add(constraints)
    solver.maximize(objective)
    #solver.set_objective(objective)
    if solver.check() == sat:
        model = solver.model()
        print("The maximum amount of geodes is {}".format(model[geode[t]]))
        #for i in range(t+1):
            #print(i, ")",model[ore[i]], model[clay[i]],model[obsidian[i]], model[geode[i]],"---", model[buy_ore_robot[i]], model[buy_clay_robot[i]], model[buy_obsidian_robot[i]], model[buy_geode_robot[i]],"---", model[ore_robot[i]], model[clay_robot[i]], model[obsidian_robot[i]], model[geode_robot[i]])
        return model[geode[t]].as_long()

    
blueprint_list = parse_blueprint(data) # This contain the blueprint of the robots (amount of minerals needed to buy each robot)

print(sum([solve(24,blueprint_list[i])*(i+1) for i in range(len(blueprint_list))]))

print(solve(32,blueprint_list[0])*solve(32,blueprint_list[1])*solve(32,blueprint_list[2]))
    
