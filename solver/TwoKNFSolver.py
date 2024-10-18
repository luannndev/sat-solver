from collections import defaultdict

class TwoSAT:
    def __init__(self, num_vars):
        self.n = num_vars * 2
        self.adj = defaultdict(list)
        self.adj_t = defaultdict(list)
        self.used = [False] * self.n
        self.order = []
        self.comp = [-1] * self.n
        self.assignment = [False] * num_vars
        self.formula = ""

    def dfs1(self, v):
        self.used[v] = True
        for u in self.adj[v]:
            if not self.used[u]:
                self.dfs1(u)
        self.order.append(v)

    def dfs2(self, v, cl):
        self.comp[v] = cl
        for u in self.adj_t[v]:
            if self.comp[u] == -1:
                self.dfs2(u, cl)

    def solve_2SAT(self):
        self.order.clear()
        self.used = [False] * self.n
        for i in range(self.n):
            if not self.used[i]:
                self.dfs1(i)

        self.comp = [-1] * self.n
        for i in range(self.n):
            v = self.order[self.n - i - 1]
            if self.comp[v] == -1:
                self.dfs2(v, i)

        for i in range(0, self.n, 2):
            if self.comp[i] == self.comp[i + 1]:
                return False
            self.assignment[i // 2] = self.comp[i] > self.comp[i + 1]
        return True

    def add_disjunction(self, a, na, b, nb):
        a = 2 * a + int(na)
        b = 2 * b + int(nb)
        neg_a = a ^ 1
        neg_b = b ^ 1
        self.adj[neg_a].append(b)
        self.adj[neg_b].append(a)
        self.adj_t[b].append(neg_a)
        self.adj_t[a].append(neg_b)
        self.formula += '(' + ('-' if na else '') + 'x' + str(a) + ' | ' + ('-' if nb else '') + 'x' + str(b) + ') & '