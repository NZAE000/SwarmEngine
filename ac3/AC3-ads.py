domains = { # map(key, value)
    "x1": [],
    "x2": [],
    "x3": [],
    "x4": [],
    "x5": []
}

constraints = { # map(key, value)
    ("x1", "x2"): lambda x1, x2: ( 8*x1 <= 190 - 15*x2 ),
    ("x2", "x1"): lambda x2, x1: ( 190 - 15*x2 >= 8*x1 ),
    ("x3", "x4"): lambda x3, x4: ( 2*x3 <= 140 - 5*x4  ),
    ("x4", "x3"): lambda x4, x3: ( 140 - 5*x4 >= 2*x3  ),
    ("x3", "x5"): lambda x3, x5: ( 4*x3 <= 350 - x5    ),
    ("x5", "x3"): lambda x5, x3: ( 350 - x5 >= 4*x3    )
}

def revise(x, y):
    revised  = False
    x_domain = domains[x] # list
    y_domain = domains[y] # list
    
    # tuple list
    all_constraints = [constraint for constraint in constraints if constraint[0] == x and constraint[1] == y]

    for x_value in x_domain:
        satisfies = False
        for y_value in y_domain:
            for constraint in all_constraints: # constraint = tuple
                constraint_func = constraints[constraint] # get lambda of specific tuple
                if constraint_func(x_value, y_value):
                    satisfies = True
        if not satisfies:
            x_domain.remove(x_value)
            revised = True
    return revised

def ac3(arcs):
    queue = arcs[:]
    while queue:
        (x, y) = queue.pop(0)
        revised = revise(x, y)
        if revised:
            neighbors = [neighbor for neighbor in arcs if neighbor[1] == x]
            queue = queue + neighbors

def init_domains():
    # dom(x1) = {1, 2, 3, .., 15}, p. ej
    doms = { "x1": (0, 15), "x2": (0, 10), "x3": (0, 25), "x4": (0, 4), "x5": (0, 30) } 

    for key in doms:
        (min, max) = doms[key]
        domain     = domains[key]
        for i in range (min, max+1): # fill each dom(xi)
            domain.append(i)

def stdcout(domains):

    for domain in domains:
        print(domain, ": ", domains[domain])

arcs = [ # tuple list
    ("x1", "x2"),
    ("x2", "x1"),
    ("x3", "x4"),
    ("x4", "x3"),
    ("x3", "x5"),
    ("x5", "x3")
]

init_domains()
print("Current domains:")
stdcout(domains)
ac3(arcs)
print("New domains:")
stdcout(domains)