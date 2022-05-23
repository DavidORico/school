//
// Created by davidrico on 11.05.22.
//

#ifndef ASSIGNMENT2_SRC_COMMON_H_
#define ASSIGNMENT2_SRC_COMMON_H_
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>

using namespace std;

enum cell {empty, wall, delay, start, goal, traversed, mcts_spec,
            up, down, lft, rght};

struct pos {
  int x;
  int y;
};
typedef struct pos pos_t;

struct mcts_path {
  vector<pos_t> path_mcts;
  vector<pos_t> path_ff;
};
typedef struct mcts_path mcts_path_t;

vector<vector<cell>> load_map(string file_name){
  vector<vector<cell>> map;
  string line;
  ifstream my_file (file_name);
  if (my_file.is_open()){
    getline (my_file,line);
    stringstream stream(line);
    int rows, cols;
    stream >> rows;
    stream >> cols;
    map.resize(rows);

    for (int i = 0; i < rows; ++i) {
      map[i].resize(cols);
      getline (my_file,line);
      for (int j = 0; j < cols; ++j) {
        switch (line[j]) {
          case ' ':
            map[i][j] = empty;
            break;
          case '#':
            map[i][j] = wall;
            break;
          case 'D':
            map[i][j] = delay;
            break;
          case 'S':
            map[i][j] = start;
            break;
          case 'E':
            map[i][j] = goal;
            break;
          }
      }
    }

    my_file.close();
  }
  else cout << "Unable to open file";

  return map;
}

vector<vector<int>> get_rewards(vector<vector<cell>> map){
  vector<vector<int>> rewards;
  rewards.resize(map.size());
  for (int i = 0; i < rewards.size(); ++i) {
    rewards[i].resize(map[0].size());
    for (int j = 0; j < rewards[i].size(); ++j) {
      if (map[i][j] == empty || map[i][j] == start){
        rewards[i][j] = -1;
      } else if (map[i][j] == delay){
        rewards[i][j] = -50;
      } else if (map[i][j] == goal){
        rewards[i][j] = 200;
      }
    }
  }

  return rewards;
}

pos_t get_start_pos(vector<vector<cell>> map){
  pos_t start_pos;
  for (int i = 0; i < map.size(); ++i) {
    for (int j = 0; j < map[0].size(); ++j) {
      if(map[i][j] == start){
        start_pos.x = i;
        start_pos.y = j;
        return start_pos;
      }
    }
  }
  return start_pos;
}

pos_t take_action(vector<vector<cell>> map, pos_t from, pos_t to){
  int random_num = rand() % 100;
  if(random_num < 70){
    return to;
  }

  //moving sideways
  if (from.x != to.x){
    pos_t left;
    pos_t right;
    if (from.y == 0) left = from;
    else if (map[from.x][from.y-1] == wall) left = from;
    else{
      left = from;
      left.y -= 1;
    }

    if (from.y == map[0].size()-1) right = from;
    else if (map[from.x][from.y+1] == wall) right = from;
    else{
      right = from;
      right.y += 1;
    }

    if (random_num < 85) return left;
    else return right;
  } else{
    pos_t up;
    pos_t down;
    if (from.x == 0) up = from;
    else if (map[from.x-1][from.y] == wall) up = from;
    else{
      up = from;
      up.x -= 1;
    }

    if (from.x == map.size()-1) down = from;
    else if (map[from.x+1][from.y] == wall) down = from;
    else{
      down = from;
      down.x += 1;
    }

    if (random_num < 85) return up;
    else return down;
  }
}

void save_taken_path(vector<vector<cell>> map, vector<pos_t> path, string filename){
  vector<vector<cell>> mod_map = map;
  for (auto nd: path) {
    mod_map[nd.x][nd.y] = traversed;
  }

  string maze_out = "";
  for (auto vec: mod_map) {
    for (auto nd: vec) {
      switch (nd) {
      case empty:
        maze_out += ' ';
        break;
      case wall:
        maze_out += '#';
        break;
      case delay:
        maze_out += 'D';
        break;
      case start:
        maze_out += 'S';
        break;
      case goal:
        maze_out += 'E';
        break;
      case traversed:
        maze_out += 'T';
        break;
      }
    }
    maze_out += '\n';
  }

  std::ofstream out(filename);
  out << maze_out;
  out.close();
}

void save_taken_path_mcts(vector<vector<cell>> map, vector<pos_t> path_mcts, vector<pos_t> path_ff, string filename){
  vector<vector<cell>> mod_map = map;
  for (auto nd: path_mcts) {
    mod_map[nd.x][nd.y] = mcts_spec;
  }
  for (auto nd: path_ff) {
    mod_map[nd.x][nd.y] = traversed;
  }

  string maze_out = "";
  for (auto vec: mod_map) {
    for (auto nd: vec) {
      switch (nd) {
      case empty:
        maze_out += ' ';
        break;
      case wall:
        maze_out += '#';
        break;
      case delay:
        maze_out += 'D';
        break;
      case start:
        maze_out += 'S';
        break;
      case goal:
        maze_out += 'E';
        break;
      case traversed:
        maze_out += 'T';
        break;
      case mcts_spec:
        maze_out += 'M';
        break;
      }
    }
    maze_out += '\n';
  }

  std::ofstream out(filename);
  out << maze_out;
  out.close();
}

int acc_reward(vector<vector<int>> rewards, vector<pos_t> path){
  int accumulated_reward = 0;
  for (int i = 1; i < path.size(); ++i) {
    if (path[i-1].x == path[i].x && path[i-1].y == path[i].y){
      accumulated_reward = accumulated_reward - 1;
    } else {
      accumulated_reward = accumulated_reward + rewards[path[i].x][path[i].y];
    }
  }
  return accumulated_reward;
}

void save_policy(vector<vector<cell>> map, vector<vector<pos_t>> policy, string list_file){
  vector<vector<cell>> mod_map = map;
  for (int i = 0; i < map.size(); ++i) {
    for (int j = 0; j < map[0].size(); ++j) {
      if (map[i][j] != wall){
        if (i + 1 == policy[i][j].x) mod_map[i][j] = down;
        else if (i - 1 == policy[i][j].x) mod_map[i][j] = up;
        else if (j + 1 == policy[i][j].y) mod_map[i][j] = rght;
        else if (j - 1 == policy[i][j].y) mod_map[i][j] = lft;
      }
    }
  }


  string maze_out = "";
  for (auto vec: mod_map) {
    for (auto nd: vec) {
      switch (nd) {
      case wall:
        maze_out += '#';
        break;
      case goal:
        maze_out += 'E';
        break;
      case up:
        maze_out += 'U';
        break;
      case down:
        maze_out += 'D';
        break;
      case lft:
        maze_out += 'L';
        break;
      case rght:
        maze_out += "R";
      }
    }
    maze_out += '\n';
  }

  std::ofstream policy_vis_file("../output/policy/policy_visualization-" + list_file);
  policy_vis_file << maze_out;
  policy_vis_file.close();
}

#endif // ASSIGNMENT2_SRC_COMMON_H_
