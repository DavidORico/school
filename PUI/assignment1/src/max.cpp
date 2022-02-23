#include <stdio.h>
#include <string>
#include <vector>
#include <priority_queue>
#include <set>
#include <unordered_set>
#include <iostream>
#include "problem.h"
 
using namespace std;

struct node {
  int cost;
  set<int> fact_name_id;
};
typedef struct node node_t;

string a_star(strips_t &strips);

string a_star(strips_t &strips, node_t init, node_t goal){
    // implementing open list as a priority queue that stores pointers to the nodes
    auto cmp = [](*node_t left, *node_t right) { return (left.cost ^ 1) > (right.cost ^ 1); };
    priority_queue<*node_t, vector<*node_t>, decltype(cmp)> open(cmp);
    // distances saved in unordered map by set of fact ids
    unordered_map<set<int>, int> dist;
    // visited nodes saved in unordered set by fact ids
    unordered_set<set<int>> closed;

    open.push(init);
    while(!open.empty()){
      nd = open.pop();

      auto search = dist.find(nd);
      int curr_dist = 0;
      if (search != example.end()) {
        std::cout << "Found " << search->first << " " << search->second << '\n';
        curr_dist = search->second;
      } else {
        std::cout << "Not found\n";
        curr_dist = -1;
      }
      if(closed.contains(nd) || nd.cost < curr_dist){
        closed.insert(nd);
        dist.insert_or_assign(nd, curr_dist);

        if(goal_reached(nd)){
          return "GOAL FOUND";
        }
        for(auto succ : nd){
          if(h_star_heur(succ) > 0){
            open.push(succ);
          }
        }
      }
    }
    string res = "FUTURE PATH";
    return res;
}

int main(int argc, char *argv[])
{
    strips_t strips;
    //fdr_t fdr;
 
    if (argc != 3){
        fprintf(stderr, "Usage: %s problem.strips problem.fdr\n", argv[0]);
        return -1;
    }
 
    // Load the planning problem in STRIPS or FDR
    stripsRead(&strips, argv[1]);
    //fdrRead(&fdr, argv[2]);
 
    // Implement the search here
    // create init and goal node
    node_t init, goal;
    for(int i = 0; i < strips.init_size; i++){
      init.fact_name_id.insert(strips.init[i]);
    }
    for(int i = 0; i < strips.goal_size; i++){
      goal.fact_name_id.insert(strips.goal[i]);
    }
    goal.cost = 0;
    init.cost = h_star_heur();
    string res = a_star(strips, init, goal);

    stripsFree(&strips);
    //fdrFree(&fdr);

    return 0;
}
