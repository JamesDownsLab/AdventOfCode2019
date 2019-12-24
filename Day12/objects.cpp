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

bool Moon::xsame() {
    return x_ == initialx_ && vx_==0;
}

bool Moon::ysame() {
    return y_ == initialy_ && vy_ == 0;
}

bool Moon::zsame() {
    return z_ == initialz_ && vz_ == 0;
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
}

void System::run(int steps) {
    for (int s{0}; s<steps; ++s){
        update_velocities();
        update_positions();
    }
}

std::vector<int> System::run_each_axis() {
    std::vector<int> output;
    int steps = 0;
    bool finished = false;
    bool x_done = false;
    bool y_done = false;
    bool z_done = false;

    while (!finished){
        steps += 1;
        run(1);
        if (!x_done) {
            bool all_same = true;
            for (Moon moon : moons_){
                if (!moon.xsame()){
                    all_same = false;
                }
            }
            if (all_same){
                output.push_back(steps);
                x_done = true;
            }
        }
        if (!y_done) {
            bool all_same = true;
            for (Moon moon : moons_){
                if (!moon.ysame()){
                    all_same = false;
                }
            }
            if (all_same){
                output.push_back(steps);
                y_done = true;
            }
        }
        if (!z_done) {
            bool all_same = true;
            for (Moon moon : moons_){
                if (!moon.zsame()){
                    all_same = false;
                }
            }
            if (all_same){
                output.push_back(steps);
                z_done = true;
            }
        }
        if (x_done && y_done && z_done){
            finished = true;
        }
    }
    return output;
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
    for (size_t i{0}; i < pair_indices_.size(); i+=2) {
        int index1 = pair_indices_[i];
        int index2 = pair_indices_[i+1];
        Moon &moon1 = moons_[index1];
        Moon &moon2 = moons_[index2];

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