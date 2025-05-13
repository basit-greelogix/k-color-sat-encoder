def read_graph():
    """ Reads the graph from standard input (mimicking a .col file) """
    vertices = set()
    edges = []

    print("Paste the graph lines (e.g., 'e 1 2'), then enter an empty line to finish:")

    while True:
        try:
            line = input()
            if line.strip() == "":
                break
            parts = line.strip().split()
            if parts and parts[0] == "e":
                u, v = int(parts[1]), int(parts[2])
                edges.append((u, v))
                vertices.add(u)
                vertices.add(v)
        except EOFError:
            break

    return sorted(vertices), edges

def generate_sat(vertices, edges, k):
    """ Generates SAT clauses for k-colorability """
    clauses = []
    var_map = {}

    # Map variables to CNF encoding format
    var_count = 1
    for v in vertices:
        for c in range(1, k + 1):
            var_map[(v, c)] = var_count
            var_count += 1

    # Each vertex must have at least one color
    for v in vertices:
        clauses.append(" ".join(str(var_map[(v, c)]) for c in range(1, k + 1)) + " 0")

    # No vertex can have more than one color
    for v in vertices:
        for c1 in range(1, k + 1):
            for c2 in range(c1 + 1, k + 1):
                clauses.append(f"-{var_map[(v, c1)]} -{var_map[(v, c2)]} 0")

    # Adjacent vertices must have different colors
    for u, v in edges:
        for c in range(1, k + 1):
            clauses.append(f"-{var_map[(u, c)]} -{var_map[(v, c)]} 0")

    return clauses, var_count - 1

def write_dimacs(clauses, num_vars):
    """ Outputs the SAT problem in DIMACS CNF format """
    print(f"p cnf {num_vars} {len(clauses)}")
    for clause in clauses:
        print(clause)

if __name__ == "__main__":
    try:
        k = int(input("Enter number of colors (k): "))
        vertices, edges = read_graph()
        sat_clauses, num_vars = generate_sat(vertices, edges, k)
        write_dimacs(sat_clauses, num_vars)
    except ValueError:
        print("Invalid input. Please enter an integer for the number of colors.")
