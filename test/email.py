import nice_re_dsl as nrd

email_regex = nrd.Regexp() \
    .start_with() \
    .once_or_more(nrd.CharSet([nrd.a2z_A2Z_029, '_', '-'])) \
    .then('@') \
    .zero_or_more(
    nrd.Op.once_or_more(nrd.CharSet([nrd.a2z_A2Z_029, '_', '-'])) \
        .then('.')
) \
    .once_or_more(nrd.CharSet([nrd.a2z_A2Z])) \
    .end_with()

print(email_regex)
