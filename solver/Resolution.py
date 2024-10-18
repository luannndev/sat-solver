import sys
from builtins import frozenset

from nltk.sem import Expression
from nltk.sem import logic

sys.setrecursionlimit(150000)

logic._counter._value = 0

TRUE = logic.Expression.fromstring('1')
FALSE = logic.Expression.fromstring('0')

debug = False


class Resolution():
    def simplify_formula(self, formula):
        parsed_formula = logic.Expression.fromstring(formula)

        def apply_laws(expression):
            if isinstance(expression, logic.OrExpression):
                first_simplified = apply_laws(expression.first)
                second_simplified = apply_laws(expression.second)

                if first_simplified == second_simplified:
                    return first_simplified
                elif first_simplified == TRUE or second_simplified == TRUE:
                    return TRUE
                elif first_simplified == FALSE:
                    return second_simplified
                elif second_simplified == FALSE:
                    return first_simplified
                else:
                    return logic.OrExpression(first_simplified, second_simplified)

            elif isinstance(expression, logic.AndExpression):
                first_simplified = apply_laws(expression.first)
                second_simplified = apply_laws(expression.second)

                if first_simplified == second_simplified:
                    return first_simplified
                elif first_simplified == TRUE:
                    return second_simplified
                elif second_simplified == TRUE:
                    return first_simplified
                elif first_simplified == FALSE or second_simplified == FALSE:
                    return FALSE
                else:
                    return logic.AndExpression(first_simplified, second_simplified)

            elif isinstance(expression, logic.NegatedExpression):
                term_simplified = apply_laws(expression.term)

                if isinstance(term_simplified, logic.NegatedExpression):
                    return apply_laws(term_simplified.term)
                else:
                    return logic.NegatedExpression(term_simplified)

            else:
                return expression

        simplified_formula = apply_laws(parsed_formula)

        if str(simplified_formula) != str(parsed_formula):
            return self.simplify_formula(str(simplified_formula))
        else:
            return str(simplified_formula)

    def extract_clause_set(self, expr):
        clause_set = []

        if isinstance(expr, logic.AndExpression):
            clause_set.extend(self.extract_clause_set(expr.first))
            clause_set.extend(self.extract_clause_set(expr.second))
        else:
            clause_set.append([expr.simplify()])

        return clause_set

    def create_clause_set(self, clause_set):
        c_set = set()
        for clause in clause_set:
            for literal in clause:
                if not '|' in str(literal):
                    c_set.add(frozenset(str(literal).split(' ')))
                else:
                    c_set.add(frozenset(str(literal).strip("()").replace(" ", "").split('|')))

        print(c_set)
        return c_set

    def make_resolvent(self, clause_set):
        resolventen = set()
        print("Bilde Resolventen...")
        for clause1 in clause_set:
            for clause2 in clause_set:
                if clause1 == clause2:
                    continue
                for literal1 in clause1:
                    for literal2 in clause2:
                        if str('-' + literal1) == literal2 or str('-' + literal2) == literal1:
                            resolvente = frozenset(element for element in
                                                   frozenset(e for e in clause1 if e not in {literal1}).union(
                                                       frozenset(e for e in clause2 if e not in {literal2})))
                            if debug:
                                if frozenset() == resolvente:
                                    print()
                                print(f"Klausel 1: {clause1}, Klausel 2: {clause2}, Resolvente: {resolvente}")
                                if frozenset() == resolvente:
                                    print()
                            resolventen.add(resolvente)

        return resolventen.union(clause_set)

    def solve(self, formular):
        clause_set = self.extract_clause_set(Expression.fromstring(formular))

        last_clause = self.make_resolvent(self.create_clause_set(clause_set))
        iteration = 1
        if debug:
            print(f"Iteration: {iteration} | {last_clause}")
        while frozenset() not in last_clause:
            iteration += 1
            resolvent = self.make_resolvent(last_clause)
            if debug:
                print(f"Iteration: {iteration}\nnew_clause: {resolvent}\nlast_clause: {last_clause}")
            if resolvent != last_clause:
                last_clause = resolvent
            else:
                break

        print(f"Formular '{formular}' is {'satisfied' if frozenset() not in last_clause else 'unsatisfied'}.")
        print(f"clause_set: {last_clause}\nclauses: {len(last_clause)}")