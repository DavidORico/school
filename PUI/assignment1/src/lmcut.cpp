#include <stdio.h>
#include <string>
#include <vector>
#include <queue>
#include <unordered_set>
#include <set>
#include <map>
#include <algorithm>
#include <iostream>

#include "problem.h"
 
using namespace std;

struct node {
  int cost_f;
  int cost_g;
  vector<int> operators_used;
  vector<int> facts;
};
typedef struct node node_t;

struct hmax_ret {
  int cost;
  vector<int> deltas;
};
typedef struct hmax_ret hmax_ret_t;

struct lm_op {
  int supporter;
  int cost;
  vector<int> pre_cond;
  vector<int> add_eff;
  vector<int> dell_eff;
};
typedef struct lm_op lm_op_t;

/*struct just_node {
  vector<int> predecessor;
};

struct just_graph {
  int id_goal_node;
  int id_init_node;
  vector<just_node_t> just_nodes;
};
typedef struct just_graph just_graph_t;*/

node_t a_star(strips_t &strips, node_t init, node_t goal);
hmax_ret_t h_max_heur(strips_t &strips, node_t s, node_t goal);
int lm_cut_heur(strips_t &strips, node_t init, node_t goal, node_t nd);
vector<lm_op_t>construct_new_operators(strips_t &strips,node_t init,node_t goal);
void set_supporters(vector<lm_op_t> &lm_ops, vector<int> deltas);
unordered_set<int> get_N_star(vector<lm_op_t> &lm_ops);
bool facts_obtained(unordered_set<int> C, node_t goal);
bool goal_reached(node_t nd, node_t goal);
bool apply_operator(node_t &nd, strips_operator_t op);
string recreate_path(node_t init, node_t res, strips_t strips);

node_t a_star(strips_t &strips, node_t init, node_t goal){
    // open list as a priority queue that stores nodes and compares them by the f cost
    auto cmp = [](node_t left, node_t right) { return left.cost_f > right.cost_f; };
    priority_queue<node_t, vector<node_t>, decltype(cmp)> open(cmp);
    // closed list as a map
    map<vector<int>, int> scores;

    open.push(init);
    while(!open.empty()){
      node_t curr_nd = open.top();
      open.pop();

      auto search = scores.find(curr_nd.facts);
      if (search == scores.end() || (curr_nd.cost_g < search->second && search != scores.end())) {
        //not visited or cost is lower
        scores[curr_nd.facts] = curr_nd.cost_g;

        if(goal_reached(curr_nd, goal)){
          return curr_nd;
        }

        node_t succ;
        for(int i = 0; i < strips.num_operators; i++){
          succ.facts = curr_nd.facts;
          succ.operators_used = curr_nd.operators_used;

          if(apply_operator(succ, strips.operators[i])){
            //operator applied
            //Set successor_current_cost = g(node_current) + w(node_current, node_successor)
            succ.cost_g = curr_nd.cost_g + strips.operators[i].cost;
            //Add history of operators used
            succ.operators_used.push_back(i);

            int cost_h = h_max_heur(strips, succ, goal);
            if(cost_h != INT32_MAX){
              succ.cost_f = succ.cost_g + cost_h;
              open.push(succ);
            }
          }
        }
      }
    }

    return init;
}

hmax_ret_t h_max_heur(strips_t &strips, node_t s, node_t goal){
  //return 0;
  hmax_ret_t res;
  int inf = INT32_MAX;
  vector<int> deltas(strips.num_facts, inf);
  vector<int> Us(strips.num_operators);
  unordered_set<int> C;
  unordered_set<int>::const_iterator got;

  for (int i = 0; i < s.facts.size(); ++i) {
    deltas[s.facts[i]] = 0;
  }

  //initialize Us
  for (int i = 0; i < strips.num_operators; ++i) {
    Us[i] = strips.operators[i].pre_size;
    //immediately apply operators with 0 pre_size
    if(strips.operators[i].pre_size == 0){
      for (int j = 0; j < strips.operators[i].add_eff_size; ++j) {
        deltas[strips.operators[i].add_eff[j]] =
            min(deltas[strips.operators[i].add_eff[j]], strips.operators[i].cost);
      }
    }
  }

  int k;
  while (!facts_obtained(C, goal)){
    //get the fact that's minimal in deltas and not in C
    int min_delt_val = INT32_MAX;
    for (int i = 0; i < deltas.size(); ++i) {
      got = C.find(i);
      if(deltas[i] < min_delt_val && got == C.end()){
        k = i;
        min_delt_val = deltas[i];
      }
    }
    if(min_delt_val == INT32_MAX) {
      res.cost = min_delt_val;
      res.deltas = deltas;
      return res;
    }

    //add k to the set of facts
    C.insert(k);
    for (int i = 0; i < strips.num_operators; ++i) {
      for (int j = 0; j < strips.operators[i].pre_size; ++j) {
        if(k == strips.operators[i].pre[j] && Us[i] > 0){
         Us[i] = Us[i] - 1;
         if(Us[i] == 0){
           for (int l = 0; l < strips.operators[i].add_eff_size; ++l) {
             deltas[strips.operators[i].add_eff[l]] =
                 min(deltas[strips.operators[i].add_eff[l]],
                     (strips.operators[i].cost + deltas[k]));
           }
         }
        }
      }
    }
  }

  int max_val = -1;
  for (int i = 0; i < goal.facts.size(); ++i) {
    if(deltas[goal.facts[i]] > max_val) max_val = deltas[goal.facts[i]];
  }
  res.cost = max_val;
  res.deltas = deltas;
  return res;
}

int lm_cut_heur(strips_t &strips, node_t init, node_t goal, node_t nd){
  hmax_ret_t hmax_res = h_max_heur(strips, nd, goal);
  if(hmax_res.cost == INT32_MAX){
    return INT32_MAX;
  }
  int h_lm = 0;
  //construct the new modifiable operators
  vector<lm_op_t> lm_ops = construct_new_operators(strips, init, goal);

  int i = 1;
  while(true){
    hmax_res = h_max_heur(strips, nd, goal);
    if(hmax_res.cost == 0) break;

    set_supporters(lm_ops, hmax_res.deltas);
    unordered_set<int> N_star = get_N_star(lm_ops);
  }
  return h_lm;
}

vector<lm_op_t>construct_new_operators(strips_t &strips,node_t init,node_t goal){
  vector<lm_op_t> lm_ops;
  for (int i = 0; i < strips.num_operators; ++i) {
    lm_op_t new_op;
    new_op.cost = strips.operators[i].cost;
    for (int j = 0; j < strips.operators[i].pre_size; ++j) {
      new_op.pre_cond.push_back(strips.operators[i].pre[j]);
    }
    for (int j = 0; j < strips.operators[i].add_eff_size; ++j) {
      new_op.add_eff.push_back(strips.operators[i].add_eff[j]);
    }
    for (int j = 0; j < strips.operators[i].del_eff_size; ++j) {
      new_op.dell_eff.push_back(strips.operators[i].del_eff[j]);
    }
    lm_ops.push_back(new_op);
  }
  //add two new operators
  lm_op_t op_init, op_goal;
  op_init.cost = 0;
  op_goal.cost = 0;
  // I = num_facts, G = num_facts + 1
  op_init.pre_cond.push_back(strips.num_facts);
  op_goal.add_eff.push_back(strips.num_facts+1);
  for (int i = 0; i < init.facts.size(); ++i) {
    op_init.add_eff.push_back(init.facts[i]);
  }
  lm_ops.push_back(op_init);
  for (int i = 0; i < goal.facts.size(); ++i) {
    op_goal.pre_cond.push_back(goal.facts[i]);
  }
  lm_ops.push_back(op_goal);
  return lm_ops;
}

void set_supporters(vector<lm_op_t> &lm_ops, vector<int> deltas){
  for (int i = 0; i < lm_ops.size(); ++i) {
    int max_val = -1;
    for (int j = 0; j < lm_ops[i].pre_cond.size(); ++j) {
      if(deltas[lm_ops[i].pre_cond[j]] > max_val){
        max_val = deltas[lm_ops[i].pre_cond[j]];
        lm_ops[i].supporter = lm_ops[i].pre_cond[j];
      }
    }
  }
}

unordered_set<int> get_N_star(vector<lm_op_t> &lm_ops){
  //basically BFS
  unordered_set<int> N_star;
  //insert goal node and its supporter
  N_star.insert(lm_ops[lm_ops.size()-1].add_eff[0]);
  N_star.insert(lm_ops[lm_ops.size()-1].supporter);
  priority_queue<>
  int last_supporter lm_ops[lm_ops.size()-1].supporter;

  return N_star;
}

bool facts_obtained(unordered_set<int> C, node_t goal){
  for (int i = 0; i < goal.facts.size(); ++i) {
    if(C.find(goal.facts[i]) == C.end()) return false;
  }
  return true;
}

bool goal_reached(node_t nd, node_t goal){
  for (int i = 0; i < goal.facts.size(); ++i) {
    bool goal_fact_found = false;
    for (int j = 0; j < nd.facts.size(); ++j) {
      if (goal.facts[i] == nd.facts[j]){
        goal_fact_found = true;
        break;
      }
    }
    if (!goal_fact_found) return false;
  }

  return true;
}

bool apply_operator(node_t &nd, strips_operator_t op){
  //check for precondition
  for(int i = 0; i < op.pre_size; i++){
    bool op_found = false;
    for (int j = 0; j < nd.facts.size(); ++j) {
      if(op.pre[i] == nd.facts[j]) {
        op_found = true;
        break;
      }
    }
    if(!op_found) return false;
  }

  //apply add effects
  for(int i = 0; i < op.add_eff_size; i++){
    bool eff_found = false;
    for (int j = 0; j < nd.facts.size(); ++j) {
      if(op.add_eff[i] == nd.facts[j]) eff_found = true;
    }
    if(!eff_found) nd.facts.push_back(op.add_eff[i]);
  }

  //remove del effects
  for(int i = 0; i < op.del_eff_size; i++){
    int idx_erase = -1;
    for (int j = 0; j < nd.facts.size(); ++j) {
      if(op.del_eff[i] == nd.facts[j]){
        idx_erase = j;
        break;
      }
    }
    if(idx_erase != -1) nd.facts.erase(nd.facts.begin()+idx_erase);
  }

  sort (nd.facts.begin(), nd.facts.end());
  return true;
}

string recreate_path(node_t init, node_t res, strips_t strips){
  string output = ";; Cost: ";
  output = output + to_string(res.cost_g) + "\n";
  output = output + ";; h^max for init: ";
  output = output + to_string(init.cost_f) + "\n\n";

  for (long unsigned int i = 0; i < res.operators_used.size(); ++i) {
    string op_name(strips.operators[res.operators_used[i]].name);
    output = output + op_name + "\n";
  }
  return output;
}

int main(int argc, char *argv[]){
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
      init.facts.push_back(strips.init[i]);
    }
    sort (init.facts.begin(), init.facts.end());
    for(int i = 0; i < strips.goal_size; i++){
      goal.facts.push_back(strips.goal[i]);
    }
    sort (goal.facts.begin(), goal.facts.end());
    init.cost_f = h_max_heur(strips, init, goal);
    init.cost_g = 0;
    node_t res = a_star(strips, init, goal);

    string final_path = recreate_path(init, res, strips);
    cout << final_path;

    stripsFree(&strips);
    //fdrFree(&fdr);

    return 0;
}
