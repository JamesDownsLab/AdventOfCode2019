//
// Created by james on 23/12/2019.
//

#include "objects.hpp"

Moon::Moon(int x, int y, int z){
x_ = x;
y_ = y;
z_ = z;
initialx_ = x;
initialy_ = y;
initialz_ = z;
}

void Moon::update_positions() {
    x_ += vx_;
    y_ += vy_;
    z_ += vz_;
}

int Moon::energy() {
    int energy {0};
    energy = (abs(x_) + abs(y_) + abs(z_)) * (abs(vx_) + abs(vy_) + abs(vz_));
    return energy;
}

bool Moon::original_state() {
    return x_ == initialx_ && y_ == initialy_ && z_ == initialz_ &&
           vx_ == 0 && vy_ == 0 && vz_ == 0;
}


System::System(std::vector<Moon> &moons) : moons_{moons}{
    pair_indices_.emplace_back(0, 1);
    pair_indices_.emplace_back(0, 2);
    pair_indices_.emplace_back(0, 3);
    pair_indices_.emplace_back(1, 2);
    pair_indices_.emplace_back(1, 3);
    pair_indices_.emplace_back(2, 3);
}

void System::run(int steps) {
    for (int s{0}; s<steps; ++s){
        update_velocities();
        update_positions();
    }
}

int System::energy() {
    int total_energy {0};
    for (size_t i{0}; i<moons_.size(); ++i){
        int moon_energy = moons_[i].energy();
        total_energy += moon_energy;
    }
    return total_energy;
}

void System::update_velocities() {
    for (size_t i{0}; i < pair_indices_.size(); ++i) {
        auto &indices = pair_indices_[i];
        Moon &moon1 = moons_[indices.first];
        Moon &moon2 = moons_[indices.second];

        if (moon1.x_ > moon2.x_) {
            moon1.vx_ -= 1;
            moon2.vx_ += 1;
        } else if (moon1.x_ < moon2.x_) {
            moon1.vx_ += 1;
            moon2.vx_ -= 1;
        }

        if (moon1.y_ > moon2.y_) {
            moon1.vy_ -= 1;
            moon2.vy_ += 1;
        } else if (moon1.y_ < moon2.y_) {
            moon1.vy_ += 1;
            moon2.vy_ -= 1;
        }

        if (moon1.z_ > moon2.z_) {
            moon1.vz_ -= 1;
            moon2.vz_ += 1;
        } else if (moon1.z_ < moon2.z_) {
            moon1.vz_ += 1;
            moon2.vz_ -= 1;
        }
    }
}

void System::update_positions() {
    for (size_t i{0}; i<moons_.size(); ++i){
        Moon& moon {moons_[i]};
        moon.update_positions();
    }
}

int System::run_until_same() {
    bool finished {false};
    int step {0};
    while (!finished){
        step += 1;
        run(1);
        finished = check_equal();
    }
    return step;
}

bool System::check_equal() {
    for (Moon& moon : moons_){
        if (!moon.original_state()){
            return false;
        }
    }
    return true;
}