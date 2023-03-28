class Graph:  # graful problemei
    def __init__(self, file_name):
        """
        Datele clasei si structura fisierului de intrare:
        Q-multimea starilor
        L-alfabetul
        S-starea de start
        F-multimea starilor finale
        T-multimea tranzitiilor (o tranzitie pe fiecare linie, structura nod1 nod2 litera)
        W-cuvantul (un string fara separatori ex. abac)
        """
        f = open(file_name, "r")
        self.Q = [int(x) for x in f.readline().split()]
        self.L = [x for x in f.readline().split()]
        self.S = int(f.readline())
        self.F = [int(x) for x in f.readline().split()]
        self.W = f.readline().strip()
        transitions = []
        for l in f:
            line = l.split()
            transitions.append([int(line[0]), int(line[1]), line[2]])
        self.T = transitions

    def __repr__(self):
        representation = "Stari: "
        representation += " ".join(str(x) for x in self.Q)
        representation += "\nAlfabet: "
        representation += " ".join(x for x in self.L)
        representation += "\nStarea de start: "
        representation += str(self.S)
        representation += "\nStarile finale: "
        representation += " ".join(str(x) for x in self.F)
        representation += "\nTranzitii:\n"
        for t in self.T:
            representation += " ".join(str(x) for x in t)
            representation += "\n"
        representation += "Cuvant: "
        representation += self.W
        return representation

    def NFA(self):
        node = [self.S]
        node2 = []
        search = "Succesiunea de stari a cuvantului {}: ".format("".join(self.W))
        countWord = 0
        flag = False
        while len(self.W) != countWord:
            #pentru fiecare nod unde am ajuns sunt verificate toate tranzitiile posibile pentru a afla toate nodurile unde se poate ajunge
            for k in range(len(node)):
                for t in self.T:
                    if t[0] == node[k] and t[2] == self.W[countWord] and t[0] in self.Q and t[1] in self.Q and t[2] in self.L:
                        if t[1] not in node2:
                            node2.append(t[1])
                        search += "{} -> {}; ".format(t[0], t[1])
            countWord += 1
            node = node2[:]
            node2.clear()
        for n in node:
            if n in self.F:
                flag = True
                break
        return flag, search

graph = Graph("data2.in")
print(str(graph))
flag, search = graph.NFA()
if flag:
    print("DA\n{}\n".format(search))
else:
    print("NU")
