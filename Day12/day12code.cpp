
#include "objects.hpp"
#include "iostream"
#include <chrono>

int main (){
    std::vector<Moon> moons {
        Moon(16, -8, 13),
        Moon(4, 10, 10),
        Moon(17, -5, 6),
        Moon(13, -3, 0)
    };

//    std::vector<Moon> moons {
//        Moon(-1, 0, 2),
//        Moon(2, -10, -7),
//        Moon(4, -8, 8),
//        Moon(3, 5, -1)
//    };
    System system{System(moons)};

//    system.run(1000);
//
//
//    int energy = system.energy();
//    std::cout << "Energy : " << energy << std::endl;

    auto start = std::chrono::high_resolution_clock::now();
    std::cout << "Steps until same: " << system.run_until_same() << std::endl;
    auto stop = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop-start);
    std::cout << duration.count() << std::endl;
};