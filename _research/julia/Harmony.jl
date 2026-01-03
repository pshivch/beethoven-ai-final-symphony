module Harmony
export cadence_score

function cadence_score(pchs::Vector{Int})
    has7 = any(==(7), pchs)
    has0 = any(==(0), pchs)
    base = (has7 && has0) ? 1.0 : 0.2
    dom = count(==(7), pchs)
    return base + 0.1 * dom
end

end
