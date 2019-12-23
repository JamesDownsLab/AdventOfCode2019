//
// Created by james on 23/12/2019.
//

#ifndef DAY12_OBJECTS_HPP
#define DAY12_OBJECTS_HPP

#include <vector>
#include <algorithm>
#include <iostream>

class Moon {
public:
    explicit Moon (int x, int y, int z);
    int x_;
    int y_;
    int z_;
    int vx_{0};
    int vy_{0};
    int vz_{0};

    void update_positions();

    int energy();

    bool original_state();

private:

    int initialx_;
    int initialy_;
    int initialz_;
};

class System {
public:
explicit System(std::vector<Moon> &moons);

std::vector<Moon>& moons_;

void run(int steps);

int energy();

private:
    void update_velocities();
    void update_positions();
    std::vector<std::pair<int, int>> pair_indices_;
};



#endif //DAY12_OBJECTS_HPP
