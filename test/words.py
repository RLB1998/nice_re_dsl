import nice_re_dsl as nrd

words_regexp = nrd.Regexp() \
    .from_here_ignore_case() \
    .then(nrd.WORD_BOUNDARY) \
    .once_or_more(
    nrd.CharSet([nrd.a2z_A2Z, "'-"])
) \
    .then(nrd.WORD_BOUNDARY) \
    .done()

print(words_regexp)
