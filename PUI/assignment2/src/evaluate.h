//
// Created by davidrico on 14.05.22.
//

#ifndef ASSIGNMENT2_SRC_EVALUATE_H_
#define ASSIGNMENT2_SRC_EVALUATE_H_
#include <string>
#include <chrono>
#include "common.h"
#include "ff_replan.h"
#include "value_iteration.h"
#include "mcts.h"

using namespace std::chrono;

void evaluate_ff_replan(vector<string> list_files, unsigned int num_runs){
  string strategy = "FF_REPLAN";
  cout << "Using " + strategy << endl;

  for (auto & list_file : list_files) {
    std::ofstream time_file("../output/" + strategy + "/time_microsec_maze-" + list_file);
    std::ofstream num_steps_file("../output/" + strategy + "/num_steps_maze-" + list_file);
    std::ofstream rewards_file("../output/" + strategy + "/rewards_maze" + list_file);
    vector<vector<cell>> map = load_map("../dataset-assignment2/data/maze-" + list_file);
    vector<vector<int>> rewards = get_rewards(map);
    pos_t start = get_start_pos(map);
    vector<pos_t> path;

    for (unsigned int i = 0; i < num_runs; i++) {
      srand (i);
      auto start_time = high_resolution_clock::now();
      path = ff_replan(map, rewards, start);
      auto stop_time = high_resolution_clock::now();
      auto duration = duration_cast<microseconds>(stop_time - start_time);

      time_file << " " << duration.count();
      num_steps_file << " " << path.size();
      rewards_file << " " << acc_reward(rewards, path);
    }

    time_file << endl;
    num_steps_file << endl;
    rewards_file << endl;

    save_taken_path(map, path, "../output/" + strategy + "/maze-" + list_file);

    cout << list_file << " processed" << endl;
    time_file.close();
    num_steps_file.close();
    rewards_file.close();
  }
}

void evaluate_vi(vector<string> list_files, unsigned int num_runs){
  string strategy = "VI";
  cout << "Using " + strategy << endl;

  for (auto & list_file : list_files) {
    std::ofstream time_file("../output/" + strategy + "/time_microsec_maze-" + list_file);
    std::ofstream num_steps_file("../output/" + strategy + "/num_steps_maze-" + list_file);
    std::ofstream rewards_file("../output/" + strategy + "/rewards_maze" + list_file);
    vector<vector<cell>> map = load_map("../dataset-assignment2/data/maze-" + list_file);
    vector<vector<int>> rewards = get_rewards(map);
    pos_t start = get_start_pos(map);
    vector<pos_t> path;

    std::ofstream policy_time_file("../output/" + strategy + "/policy_time_microsec_maze-" + list_file);
    auto start_time = high_resolution_clock::now();
    vector<vector<pos_t>> policy = vi_async(map, rewards);
    auto stop_time = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop_time - start_time);
    policy_time_file << " " << duration.count();
    policy_time_file.close();
    cout << "Policy gained\n";

    for (unsigned int i = 0; i < num_runs; i++) {
      srand (i);
      start_time = high_resolution_clock::now();
      path = follow_policy(map, policy, start);
      stop_time = high_resolution_clock::now();
      duration = duration_cast<microseconds>(stop_time - start_time);

      time_file << " " << duration.count();
      num_steps_file << " " << path.size();
      rewards_file << " " << acc_reward(rewards, path);
    }

    time_file << endl;
    num_steps_file << endl;
    rewards_file << endl;

    save_taken_path(map, path, "../output/" + strategy + "/maze-" + list_file);

    cout << list_file << " processed" << endl;
    time_file.close();
    num_steps_file.close();
    rewards_file.close();
  }
}

void evaluate_mcts(vector<string> list_files, unsigned int num_runs){
  string strategy = "MCTS";
  cout << "Using " + strategy << endl;

  for (int i = 0; i < list_files.size(); i++) {
    std::ofstream time_file("../output/" + strategy + "/time_microsec_maze-" + list_files[i]);
    std::ofstream num_steps_file("../output/" + strategy + "/num_steps_maze-" + list_files[i]);
    std::ofstream rewards_file("../output/" + strategy + "/rewards_maze" + list_files[i]);
    vector<vector<cell>> map = load_map("../dataset-assignment2/data/maze-" + list_files[i]);
    vector<vector<int>> rewards = get_rewards(map);
    pos_t start = get_start_pos(map);
    vector<vector<pos_t>> policy = vi_async(map, rewards);
    save_policy(map, policy, list_files[i]);
    cout << "Got policy for MCTS\n";
    vector<pos_t> path;

    for (unsigned int i = 0; i < num_runs; i++) {
      srand (i);
      auto start_time = high_resolution_clock::now();
      path = mcts(map, rewards, policy, start);
      auto stop_time = high_resolution_clock::now();
      auto duration = duration_cast<microseconds>(stop_time - start_time);

      time_file << " " << duration.count();
      num_steps_file << " " << path.size();
      rewards_file << " " << acc_reward(rewards, path);
    }

    time_file << endl;
    num_steps_file << endl;
    rewards_file << endl;

    save_taken_path(map, path, "../output/" + strategy + "/maze-" + list_files[i]);
    //save_taken_path_mcts(map, path.path_mcts, path.path_ff, "../output/" + strategy + "/maze-" + list_files[i]);

    cout << list_files[i] << " processed" << endl;
    time_file.close();
    num_steps_file.close();
    rewards_file.close();
  }
}

#endif // ASSIGNMENT2_SRC_EVALUATE_H_
