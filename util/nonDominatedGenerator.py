import itertools

#def is_dominated(problem, sol1, sol2):
#    """Check if sol1 is dominated by sol2"""
#    return (
#        problem.fit_min(sol2) <= problem.fit_min(sol1) and
#        problem.fit_max(sol2) >= problem.fit_max(sol1) and
#        (problem.fit_min(sol2) < problem.fit_min(sol1) or
#         problem.fit_max(sol2) > problem.fit_max(sol1))
#    )

# id_AP = id Algorithm with Problem.
def nonDomGenerator(problem):
    # Generate all possible candidates within the domain
    domains = [problem.domain(i) for i in range(problem.dimension)]
    #print("domains: ", domains)
    candidates = itertools.product(*domains)
    #print("candidates: ", candidates)

    ## Evaluate feasible candidates
    feasible_solutions = [sol for sol in candidates if problem.isFeasible(sol)]
    #with mp.Pool() as pool:
    #    feasible_solutions = list(filter(None, pool.map(is_feasible_wrapper, [(problem, sol) for sol in candidates])))
    #print(feasible_solutions)

    # Obtain non-dominated solutions (Pareto Frontier)
    #pareto_front = []
    #for sol in feasible_solutions:
    #    dominated = False
    #    for other in feasible_solutions:
    #        #print("sol:", sol, "other:", other)
    #        if is_dominated(problem, sol, other):
    #            dominated = True
    #            break
    #    if not dominated:
    #        pareto_front.append(sol)
    #        print("Not dom: ", sol)

    feasible_solutions.sort(key=lambda sol: problem.fit_min(sol))
    pareto_front = []
    best_value_so_far = float('-inf')

    for sol in feasible_solutions:
        value = problem.fit_max(sol)
        if value > best_value_so_far:
            pareto_front.append(sol)
            best_value_so_far = value
            #print("Not dom: ", sol)

    ## Save to file
    path = "data/non_dominated_solutions-" + problem.name + ".txt"
    with open(path, "w") as f:
        for sol in pareto_front:
            cost  = problem.fit_min(sol)
            value = problem.fit_max(sol)
            f.write(f"{cost}-{value}\n")

    #print(f"{len(pareto_front)} no dominated solutions were saved in 'pareto_solutions.txt'")
    return path
