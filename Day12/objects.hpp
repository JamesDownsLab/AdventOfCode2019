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

    bool xsame();
    bool ysame();
    bool zsame();

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

int run_until_same();

std::vector<int> run_each_axis();

private:
    void update_velocities();
    void update_positions();
//    std::vector<std::pair<int, int>> pair_indices_;
    std::vector<int> pair_indices_ {0, 1, 0, 2, 0, 3, 1, 2, 1, 3, 2, 3};
    bool check_equal();
};



#endif //DAY12_OBJECTS_HPP
