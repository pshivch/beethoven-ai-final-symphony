#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
double polyphony_score(const std::vector<double>&);

namespace py = pybind11;
PYBIND11_MODULE(cpp_dsp, m) {
    m.def("polyphony_score", &polyphony_score, "Harmonicity/dissonance score");
}
