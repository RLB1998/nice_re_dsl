import nice_re_dsl as nerd

words_regexp = nerd.Regexp() \
    .from_here_ignore_case() \
    .then(
    nerd.WordBoundary(
        nerd.Op.once_or_more(
            nerd.CharSet([nerd.a2z_A2Z, "'-"])
        )
    )
) \
    .done()

print(words_regexp)
