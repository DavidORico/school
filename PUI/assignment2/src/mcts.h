//
// Created by davidrico on 11.05.22.
//

#ifndef ASSIGNMENT2_SRC_MCTS_H_
#define ASSIGNMENT2_SRC_MCTS_H_
#include <chrono>
#include <cmath>
#include "common.h"
#include "ff_replan.h"

using namespace std::chrono;

struct node {
  int num_visits = 1;
  double UCT_val = 0;
  double reward = 0;
  double mean_reward = 0;
  pos_t state;
  struct node * parent = nullptr;
  vector<pos_t> possible_actions;
  vector<struct node> successors;
};
typedef struct node node_t;

vector<pos_t> mcts(vector<vector<cell>> map, vector<vector<int>> rewards, vector<vector<pos_t>> policy, pos_t start_nd);
node_t * traverse_tree(node_t * root);
int depth_tree(node_t * root);
void backpropagate(node_t * expanded_node, int sim_reward);
int simulate(vector<vector<cell>> map, vector<vector<int>> rewards, vector<vector<pos_t>> policy, node_t * expanded_node);
node_t * expand_tree(vector<vector<cell>> map, node_t * leaf);
mcts_path_t follow_tree_policy(vector<vector<cell>> map, vector<vector<int>> rewards, node_t root);
vector<pos_t> random_moves(vector<vector<cell>> map, pos_t state);

vector<pos_t> mcts(vector<vector<cell>> map, vector<vector<int>> rewards, vector<vector<pos_t>> policy, pos_t start_nd){
  node_t root;
  root.state = start_nd;
  root.possible_actions = get_neighbours(map, start_nd);
  vector<pos_t> path;
  path.push_back(root.state);

  while (true) {
    while (depth_tree(&root) < 3) {
      node_t *leaf = traverse_tree(&root);
      node_t *expanded_node = expand_tree(map, leaf);
      int sim_reward = simulate(map, rewards, policy, expanded_node);
      backpropagate(expanded_node, sim_reward);
      if (map[expanded_node->state.x][expanded_node->state.y] == goal) break;
    }

    // choose best action from root
    double best_UCT = -DBL_MAX;
    node_t successor;
    for (auto succ : root.successors) {
      if (succ.UCT_val > best_UCT){
        best_UCT = succ.UCT_val;
        successor = succ;
      }
    }
    // Take action following the successor with highest UCT val
    pos_t next_state = take_action(map, root.state, successor.state);
    path.push_back(next_state);
    node_t new_root;
    new_root.state = next_state;
    new_root.possible_actions = get_neighbours(map, next_state);
    root = new_root;
    if(map[next_state.x][next_state.y] == goal) break;
  }
  return path;
}

node_t * traverse_tree(node_t * root){
  node_t * curr_node = root;

  while (curr_node->successors.size() == curr_node->possible_actions.size()){
    double best_UCT = -DBL_MAX;
    node_t * successor;
    for (int i = 0; i < curr_node->successors.size(); i++) {
      if (curr_node->successors[i].UCT_val > best_UCT){
        best_UCT = curr_node->successors[i].UCT_val;
        successor = &curr_node->successors[i];
      }
    }
    curr_node = successor;
  }

  return curr_node;
}

int depth_tree(node_t * root){
  node_t * curr_node = root;
  int depth = 0;

  while (curr_node->successors.size() == curr_node->possible_actions.size()){
    double best_UCT = -DBL_MAX;
    node_t * successor;
    for (int i = 0; i < curr_node->successors.size(); i++) {
      if (curr_node->successors[i].UCT_val > best_UCT){
        best_UCT = curr_node->successors[i].UCT_val;
        successor = &curr_node->successors[i];
      }
    }
    depth += 1;
    curr_node = successor;
  }

  return depth;
}

void backpropagate(node_t * expanded_node, int sim_reward){
  node_t * curr_node = expanded_node;
  while (curr_node->parent != nullptr){
    curr_node->num_visits += 1;
    curr_node->reward += sim_reward;
    curr_node->mean_reward = curr_node->reward / curr_node->num_visits;
    curr_node->UCT_val = curr_node->mean_reward + sqrt((2*log(curr_node->parent->num_visits)) / curr_node->num_visits);
    curr_node = curr_node->parent;
  }
}

int simulate(vector<vector<cell>> map, vector<vector<int>> rewards, vector<vector<pos_t>> policy, node_t * expanded_node){
  //vector<pos_t> simulate_path = bfs(map, rewards, expanded_node->state);
  //vector<pos_t> simulate_path = random_moves(map, expanded_node->state);
  if (map[expanded_node->state.x][expanded_node->state.y] == goal)  return 200;
  vector<pos_t> simulate_path = follow_policy(map, policy, expanded_node->state);
  int sim_reward = acc_reward(rewards, simulate_path);
  return sim_reward;
}

node_t * expand_tree(vector<vector<cell>> map, node_t * leaf){
  int num_taken_actions = leaf->successors.size();
  node_t untried_action;
  untried_action.state = leaf->possible_actions[num_taken_actions];
  untried_action.possible_actions = get_neighbours(map, untried_action.state);
  untried_action.parent = leaf;
  leaf->successors.push_back(untried_action);
  return &leaf->successors.back();
}

mcts_path_t follow_tree_policy(vector<vector<cell>> map, vector<vector<int>> rewards, node_t root){
  vector<pos_t> taken_path;
  taken_path.push_back(root.state);
  node_t curr_node = root;

  while (curr_node.successors.size() == curr_node.possible_actions.size()){
    if (map[curr_node.state.x][curr_node.state.y] == goal) break;
    double best_UCT = -DBL_MAX;
    node_t successor;
    for (auto succ : curr_node.successors) {
      if (succ.UCT_val > best_UCT){
        best_UCT = succ.UCT_val;
        successor = succ;
      }
    }

    // Take action following the successor with highest UCT val
    pos_t next_state = take_action(map, curr_node.state, successor.state);
    taken_path.push_back(next_state);
    if (next_state.x == curr_node.state.x && next_state.y == curr_node.state.y) continue;
    else if (next_state.x == successor.state.x && next_state.y == successor.state.y) curr_node = successor;
    else{
      for (auto succ : curr_node.successors) {
        if (next_state.x == succ.state.x && next_state.y == succ.state.y){
          curr_node = succ;
          break;
        }
      }
    }
  }

  mcts_path_t final_path;
  if (map[curr_node.state.x][curr_node.state.y] == goal) {
    final_path.path_mcts = taken_path;
    return final_path;
  }
  else{
    vector<pos_t> ff_path = ff_replan(map, rewards, curr_node.state);
    final_path.path_mcts = taken_path;
    final_path.path_ff = ff_path;
    return final_path;
  }
}

vector<pos_t> random_moves(vector<vector<cell>> map, pos_t state){
  vector<pos_t> path_taken;
  path_taken.push_back(state);
  pos_t cur_node = state;
  int num_moves = 15;
  int random_num;
  for (int i = 0; i < num_moves; ++i) {
    vector<pos_t> neighbours = get_neighbours(map, cur_node);
    random_num = rand() % neighbours.size();
    cur_node = take_action(map, cur_node, neighbours[random_num]);
    path_taken.push_back(cur_node);
  }
  return path_taken;
}
#endif // ASSIGNMENT2_SRC_MCTS_H_
