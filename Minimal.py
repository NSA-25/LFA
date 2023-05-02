import copy


class Graph:
    def __init__(self, file_name):
        """
        Datele clasei si structura fisierului de intrare:
        Q-multimea starilor
        L-alfabetul
        S-starea de start
        F-multimea starilor finale
        W-cuvantul (un string fara separatori ex. abac)
        T-multimea tranzitiilor (o tranzitie pe fiecare linie, structura nod1 nod2 litera)
        """
        f = open(file_name, "r")
        self.Q = [int(x) for x in f.readline().split()]
        self.L = [x for x in f.readline().split()]
        self.S = int(f.readline())
        self.F = [int(x) for x in f.readline().split()]
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
        return representation

    def minimization(self):
        first_partition = [[x for x in self.Q if x not in self.F], self.F]
        second_partition = copy.deepcopy(first_partition)
        flag = True
        while flag:
            third_partition = []
            fourth_partition = copy.deepcopy(second_partition)
            for part in fourth_partition:
                if len(part) == 1:
                    third_partition.append(part)
                else:
                    equivalences = []
                    for state in part:
                        other_states = [n for n in part if n is not state]
                        indistinguishables = []
                        while other_states:
                            distinct = False
                            test_state = other_states.pop()
                            for l in self.L:
                                flag1 = False
                                flag2 = False
                                for t in self.T:
                                    if t[0] == state and t[1] not in part and t[2] == l:
                                        flag1 = True
                                    if t[0] == test_state and t[1] not in part and t[2] == l:
                                        flag2 = True
                                if flag1 != flag2:
                                    distinct = True
                                    break
                            if not distinct:
                                indistinguishables.append(test_state)
                                if state not in indistinguishables:
                                    indistinguishables.append(state)
                        if (sorted(indistinguishables) not in equivalences) and indistinguishables:
                            equivalences.append(sorted(indistinguishables))
                    if not equivalences:
                        for state in part:
                            third_partition.append([state])
                    else:
                        for eq in equivalences:
                            third_partition.append(eq)
                        for state in part:
                            flag_oth = False
                            for eq in equivalences:
                                if state in eq:
                                    flag_oth = True
                            if not flag_oth:
                                third_partition.append([state])
            if sorted(third_partition) == sorted(fourth_partition):
                flag = False
            second_partition = copy.deepcopy(third_partition)
        dict = {}
        for part in second_partition:
            dict[second_partition.index(part)] = part
        print(dict)
        new_T = []
        for k in dict.keys():
            for t in self.T:
                if t[0] in dict[k] and t[2] in self.L:
                    for a, b in dict.items():
                        if t[1] in b:
                            temp = [k, a, t[2]]
                            if temp not in new_T:
                                new_T.append(temp)
        new_Q = [k for k in dict.keys()]
        new_S = None
        for k in dict.keys():
            for s in dict[k]:
                if s == self.S:
                    new_S = k
        new_F = []
        for k in dict.keys():
            for s in dict[k]:
                if s in self.F and k not in new_F:
                    new_F.append(k)
        self.Q = new_Q
        self.T = new_T
        self.F = new_F
        self.S = new_S
g = Graph("data3.in")
g.minimization()
print(str(g))



