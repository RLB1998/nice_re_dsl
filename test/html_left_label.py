import nice_re_dsl as nrd

html_left_label = nrd.Regexp() \
    .then(nrd.Elem('<')) \
    .then(
    nrd.Group(
        (
            nrd.CharSet([nrd.a2z_A2Z]),
            nrd.Op.zero_or_more(nrd.CharSet([nrd.a2z_A2Z_029, '-']))
        )
    )
) \
    .zero_or_more(nrd.SPACE) \
    .then(
    nrd.Group(
        (nrd.Op.zero_or_more(nrd.CharSet(['>'], is_exclude=True), non_greedy=True),)
    )
) \
    .then(nrd.Elem('>')) \
    .done()

print(html_left_label)
