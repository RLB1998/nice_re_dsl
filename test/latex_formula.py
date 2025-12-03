import nice_re_dsl as nrd

latex_formula = nrd.Regexp() \
    .from_here_match_multilines() \
    .then(
    nrd.Group(
        (
            nrd.NLB('\\') \
                .then(nrd.Elem("$")) \
                .once_or_more(nrd.ANY_CHAR, non_greedy=True) \
                .then(nrd.NLB('\\')) \
                .then(nrd.Elem("$")),
            nrd.Elem("$$").once_or_more(nrd.ANY_CHAR, non_greedy=True).then(nrd.Elem("$$")),
            nrd.Elem("\[").once_or_more(nrd.ANY_CHAR, non_greedy=True).then(nrd.Elem("\]")),
            nrd.Elem("\(").once_or_more(nrd.ANY_CHAR, non_greedy=True).then(nrd.Elem("\)"))
        )
        , is_alternative=True, is_catch=True)
) \
    .done()

print(latex_formula)
