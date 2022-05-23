//
// Created by davidrico on 11.05.22.
//

#ifndef ASSIGNMENT2_SRC_FF_REPLAN_H_
#define ASSIGNMENT2_SRC_FF_REPLAN_H_
#include <queue>
#include <algorithm>
#include "common.h"

vector<pos_t> ff_replan(vector<vector<cell>> map, vector<vector<int>> rewards, pos_t start);
vector<pos_t> bfs(vector<vector<cell>> map, vector<vector<int>> rewards, pos_t start);
vector<pos_t> get_neighbours(vector<vector<cell>> map, pos_t node);
vector<pos_t> reconstruct_path(pos_t start, pos_t goal_node, vector<vector<pos_t>> parents);


vector<pos_t> ff_replan(vector<vector<cell>> map, vector<vector<int>> rewards, pos_t start){
  vector<pos_t> path_taken;
  vector<pos_t> optimal_path;
  optimal_path = bfs(map, rewards, start);

  bool reached_goal = false;
  while (true){
    for (int i = 1; i < optimal_path.size(); ++i) {
      pos_t next_pos = optimal_path[i];
      pos_t actual_next = take_action(map, optimal_path[i-1], optimal_path[i]);
      path_taken.push_back(actual_next);

      if(optimal_path[i-1].x == actual_next.x && optimal_path[i-1].y == actual_next.y){
        i -= 1;
        continue;
      }

      if(next_pos.x != actual_next.x || next_pos.y != actual_next.y){
        optimal_path = bfs(map, rewards, actual_next);
        break;
      }

      if(i == optimal_path.size() - 1) reached_goal = true;
    }
    if(reached_goal) break;
  }

  return path_taken;
}

vector<pos_t> bfs(vector<vector<cell>> map, vector<vector<int>> rewards, pos_t start){
  vector<vector<bool>> visited(map.size(), vector<bool>(map[0].size()));
  vector<vector<int>> costs(map.size(), vector<int>(map[0].size()));
  vector<vector<pos_t>> parents(map.size(), vector<pos_t>(map[0].size()));
  queue<pos_t> q;
  pos_t goal_node;

  q.push(start);
  visited[start.x][start.y] = true;

  while (!q.empty()){
    pos_t curr_node = q.front();
    q.pop();
    if (map[curr_node.x][curr_node.y] == goal) {
      goal_node.x = curr_node.x;
      goal_node.y = curr_node.y;
      break;
    }

    vector<pos_t> neighbours = get_neighbours(map, curr_node);
    int curr_cost;
    for (auto succ: neighbours) {
      curr_cost = costs[curr_node.x][curr_node.y] + rewards[curr_node.x][curr_node.y];
      if(!visited[succ.x][succ.y] || curr_cost > costs[succ.x][succ.y]){
        visited[succ.x][succ.y] = true;
        costs[succ.x][succ.y] = curr_cost;
        parents[succ.x][succ.y] = curr_node;
        q.push(succ);
      }
    }
  }

  return reconstruct_path(start, goal_node, parents);
}

vector<pos_t> get_neighbours(vector<vector<cell>> map, pos_t node){
  vector<pos_t> neighbours;
  pos_t neighbour;

  if(node.x != 0){
    if(map[node.x-1][node.y] != wall){
      neighbour.x = node.x-1;
      neighbour.y = node.y;
      neighbours.push_back(neighbour);
    }
  }
  if(node.x != map.size()-1){
    if(map[node.x+1][node.y] != wall){
      neighbour.x = node.x+1;
      neighbour.y = node.y;
      neighbours.push_back(neighbour);
    }
  }
  if(node.y != 0){
    if(map[node.x][node.y-1] != wall){
      neighbour.x = node.x;
      neighbour.y = node.y-1;
      neighbours.push_back(neighbour);
    }
  }
  if(node.y != map[0].size()-1){
    if(map[node.x][node.y+1] != wall){
      neighbour.x = node.x;
      neighbour.y = node.y+1;
      neighbours.push_back(neighbour);
    }
  }
  return neighbours;
}

vector<pos_t> reconstruct_path(pos_t start, pos_t goal_node, vector<vector<pos_t>> parents){
  vector<pos_t> path;
  pos_t curr_node = goal_node;
  path.push_back(curr_node);
  while(true){
    if(curr_node.x == start.x && curr_node.y == start.y) break;
    curr_node = parents[curr_node.x][curr_node.y];
    path.push_back(curr_node);
  }
  reverse(path.begin(), path.end());
  return path;
}

#endif // ASSIGNMENT2_SRC_FF_REPLAN_H_
