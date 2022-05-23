//
// Created by davidrico on 11.05.22.
//
#include "evaluate.h"

int main(int argc, char** argv){
  /*vector<string> list_files = {"7-A1.txt", "7-A2.txt", "7-B.txt",
                               "7-C.txt", "7-E.txt", "15-A1.txt",
                               "15-A2.txt", "15-B.txt", "15-C.txt",
                               "15-E.txt", "25-A1.txt", "25-A2.txt",
                               "25-B.txt", "25-C.txt", "25-E.txt",
                               "51-A1.txt", "51-A2.txt", "51-B.txt",
                               "51-C.txt", "51-E.txt", "101-A1.txt",
                               "101-A2.txt", "101-B.txt", "101-C.txt",
                               "101-E.txt"};*/
  vector<string> list_files = {"51-A1.txt", "51-A2.txt", "51-B.txt",
                               "51-C.txt", "51-E.txt"};
  unsigned int num_runs = 100;

  //evaluate_ff_replan(list_files, num_runs);
  //evaluate_vi(list_files, num_runs);
  evaluate_mcts(list_files, num_runs);

  return 0;
}
