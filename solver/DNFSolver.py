from nltk.sem import logic

logic._counter._value = 0

TRUE = logic.Expression.fromstring('1')
FALSE = logic.Expression.fromstring('0')


class DNFSolver():

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

    def solve_monom(self, monom):
        if "&" not in monom:
            return True

        literals = []
        for literal in monom.replace("(", "").replace(")", "").split("&"):
            literals.append(literal.strip())

        for literal1 in literals:
            for literal2 in literals:
                if "-" + literal1 == literal2 or "'" + literal2 == literal1:
                    return False
        print(f"Monom: {monom}\nLiterals: {literals}\n")
        return True

    def solve(self, formula):
        if "|" in formula:
            monoms = [monom for monom in str('(' + formula.strip("()") + ')').split("|")]
            for monom in monoms:
                return self.solve_monom(monom)
        else:
            return self.solve_monom(formula)