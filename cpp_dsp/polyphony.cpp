#include <vector>
#include <cmath>

double polyphony_score(const std::vector<double>& freqs_hz) {
    if (freqs_hz.empty()) return 0.0;
    double score = 0.0;
    for (size_t i=0;i<freqs_hz.size();++i){
        for (size_t j=i+1;j<freqs_hz.size();++j){
            double r = freqs_hz[i] / freqs_hz[j];
            if (r < 1.0) r = 1.0/r;
            double nearest = std::round(r);
            score += std::abs(r - nearest);
        }
    }
    return score;
}
