//
// Created by davidrico on 14.05.22.
//

#ifndef ASSIGNMENT2_SRC_VALUE_ITERATION_H_
#define ASSIGNMENT2_SRC_VALUE_ITERATION_H_
#include <float.h>
#include <cmath>
#include "common.h"

vector<vector<pos_t>> vi_async(vector<vector<cell>> map, vector<vector<int>> rewards);
double bellman_update(vector<vector<pos_t>> & policy, vector<vector<double>> & V_global,
                   vector<vector<int>> rewards, vector<vector<cell>> map, pos_t state);
vector<vector<pos_t>> get_actions_results(vector<vector<cell>> map, pos_t node);
bool out_of_bounds_or_wall(vector<vector<cell>> map, pos_t node);
vector<pos_t> follow_policy(vector<vector<cell>> map, vector<vector<pos_t>> policy, pos_t start);

vector<vector<pos_t>> vi_async(vector<vector<cell>> map, vector<vector<int>> rewards){
  double r;
  double treshold = 1.0;
  vector<vector<pos_t>> policy(map.size(), vector<pos_t>(map[0].size()));
  vector<vector<double>> V_global(map.size(), vector<double>(map[0].size()));
  //cout << "Getting V vals\n";
  do {
    r = -DBL_MAX;
    for (int i = 0; i < map.size(); ++i) {
      for (int j = 0; j < map[0].size(); ++j) {
        if (map[i][j] != goal && map[i][j] != wall){
          pos_t state = {i, j};
          double new_r = bellman_update(policy, V_global, rewards, map, state);
          if (new_r > r){
            r = new_r;
          }
        }
      }
    }
  } while (r > treshold);

  return policy;
}

double bellman_update(vector<vector<pos_t>> & policy, vector<vector<double>> & V_global,
                   vector<vector<int>> rewards, vector<vector<cell>> map, pos_t state){
  double V_old = V_global[state.x][state.y];

  vector<vector<pos_t>> actions_results = get_actions_results(map, state);

  double q_max = -DBL_MAX;
  pos_t pol_chosen;
  for (auto action_res: actions_results) {
    double cost_action = 0.70*rewards[action_res[0].x][action_res[0].y];
    if (action_res[1].x == state.x && action_res[1].y == state.y) cost_action += 0.15*(-1);
    else cost_action += 0.15*rewards[action_res[1].x][action_res[1].y];
    if (action_res[2].x == state.x && action_res[2].y == state.y) cost_action += 0.15*(-1);
    else cost_action += 0.15*rewards[action_res[2].x][action_res[2].y];

    double V_prob = 0.70*V_global[action_res[0].x][action_res[0].y] +
                    0.15*V_global[action_res[1].x][action_res[1].y] +
                    0.15*V_global[action_res[2].x][action_res[2].y];

    double q = cost_action + V_prob;
    if (q > q_max){
      q_max = q;
      pol_chosen = {action_res[0].x, action_res[0].y};
    }
  }
  V_global[state.x][state.y] = q_max;
  policy[state.x][state.y] = pol_chosen;
  return std::abs(q_max - V_old);
}

vector<vector<pos_t>> get_actions_results(vector<vector<cell>> map, pos_t node){
  vector<vector<pos_t>> actions_results;
  pos_t neighbour;

  if(node.x != 0){
    if(map[node.x-1][node.y] != wall){
      vector<pos_t> res;
      neighbour.x = node.x-1;
      neighbour.y = node.y;
      res.push_back(neighbour);
      neighbour.x = node.x;
      neighbour.y = node.y+1;
      if(out_of_bounds_or_wall(map, neighbour)) res.push_back(node);
      else res.push_back(neighbour);
      neighbour.x = node.x;
      neighbour.y = node.y-1;
      if(out_of_bounds_or_wall(map, neighbour)) res.push_back(node);
      else res.push_back(neighbour);
      actions_results.push_back(res);
    }
  }
  if(node.x != map.size()-1){
    if(map[node.x+1][node.y] != wall){
      vector<pos_t> res;
      neighbour.x = node.x+1;
      neighbour.y = node.y;
      res.push_back(neighbour);
      neighbour.x = node.x;
      neighbour.y = node.y+1;
      if(out_of_bounds_or_wall(map, neighbour)) res.push_back(node);
      else res.push_back(neighbour);
      neighbour.x = node.x;
      neighbour.y = node.y-1;
      if(out_of_bounds_or_wall(map, neighbour)) res.push_back(node);
      else res.push_back(neighbour);
      actions_results.push_back(res);
    }
  }
  if(node.y != 0){
    if(map[node.x][node.y-1] != wall){
      vector<pos_t> res;
      neighbour.x = node.x;
      neighbour.y = node.y-1;
      res.push_back(neighbour);
      neighbour.x = node.x+1;
      neighbour.y = node.y;
      if(out_of_bounds_or_wall(map, neighbour)) res.push_back(node);
      else res.push_back(neighbour);
      neighbour.x = node.x-1;
      neighbour.y = node.y;
      if(out_of_bounds_or_wall(map, neighbour)) res.push_back(node);
      else res.push_back(neighbour);
      actions_results.push_back(res);
    }
  }
  if(node.y != map[0].size()-1){
    if(map[node.x][node.y+1] != wall){
      vector<pos_t> res;
      neighbour.x = node.x;
      neighbour.y = node.y+1;
      res.push_back(neighbour);
      neighbour.x = node.x+1;
      neighbour.y = node.y;
      if(out_of_bounds_or_wall(map, neighbour)) res.push_back(node);
      else res.push_back(neighbour);
      neighbour.x = node.x-1;
      neighbour.y = node.y;
      if(out_of_bounds_or_wall(map, neighbour)) res.push_back(node);
      else res.push_back(neighbour);
      actions_results.push_back(res);
    }
  }
  return actions_results;
}

bool out_of_bounds_or_wall(vector<vector<cell>> map, pos_t node){
  if(node.x == -1 || node.y == -1 || node.x == map.size() || node.y == map[0].size()) return true;
  if(map[node.x][node.y] == wall) return true;
  return false;
}

vector<pos_t> follow_policy(vector<vector<cell>> map, vector<vector<pos_t>> policy, pos_t start){
  vector<pos_t> path_taken;
  path_taken.push_back(start);
  pos_t curr_node = start;
  while (map[curr_node.x][curr_node.y] != goal){
    curr_node = take_action(map, curr_node, policy[curr_node.x][curr_node.y]);
    path_taken.push_back(curr_node);
  }
  return path_taken;
}

#endif // ASSIGNMENT2_SRC_VALUE_ITERATION_H_
