class KnowledgeBase:
    def __init__(self):
        self.clauses = set()  # Store logical sentences as sets of literals in CNF

    def add_clause(self, clause):
        """Add a clause to the KB."""
        self.clauses.add(frozenset(clause))  # Ensure immutability with frozenset
        print(f"Added to KB: {clause}")

    def pl_resolve(self, clause1, clause2):
        """Resolve two clauses by removing complementary literals."""
        resolvents = set()
        for literal in clause1:
            complement = f"¬{literal}" if not literal.startswith('¬') else literal[1:]
            if complement in clause2:
                resolvent = (clause1 | clause2) - {literal, complement}
                resolvents.add(frozenset(resolvent))
        return resolvents

    def entails(self, query):
        """Check if the KB entails a query using PL-Resolution."""
        negated_query = frozenset({f"¬{query}" if not query.startswith('¬') else query[1:]})
        new_clauses = self.clauses | {negated_query}

        while True:
            new_resolvents = set()
            for clause1 in new_clauses:
                for clause2 in new_clauses:
                    if clause1 != clause2:
                        resolvents = self.pl_resolve(clause1, clause2)
                        if frozenset() in resolvents:  # Found a contradiction
                            print(f"Entailed: {query}")
                            return True
                        new_resolvents |= resolvents

            if new_resolvents.issubset(new_clauses):  # No new information gained
                return False
            new_clauses |= new_resolvents
