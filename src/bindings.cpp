#include <pybind11/pybind11.h>
#include "DEMSimulation.cpp"

namespace py = pybind11;

PYBIND11_MODULE(pyDEM, m) {
    py::class_<DEMSimulation>(m, "DEMSimulation")
        .def(py::init<double, double, double, double, double, double, double, double, double>())
        .def("run", &DEMSimulation::run);
}
