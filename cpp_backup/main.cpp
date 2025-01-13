#include "chess.hpp"
#include "game_tables.h"
#include "evaluation.h"
#include "search.h"

Board myBoard;
bool maximizeSearch;


void run(int depth){
    while (true){
        std::string move_uci;
        std::getline(std::cin, move_uci);
        if (move_uci == "end") {
            break;
        }
        if (move_uci != "start") {
            Move enemyMove = uci::uciToMove(myBoard ,move_uci);
            myBoard.makeMove(enemyMove);
        }
        auto [eval, move] = minimax(myBoard, depth, NEGINF, INF, maximizeSearch);
        std::string moveUCI = uci::moveToUci(move);
        myBoard.makeMove(move);
        std::cout << moveUCI << std::endl;
        std::cout << std::flush;
    }
}

void setupBoard(){
    std::string fen;
    std::getline(std::cin, fen);
    myBoard = Board(fen);
}

void setColor(){
    std::string input;
    std::getline(std::cin, input);
    char color = input[0];
    if (color == 'w')maximizeSearch = true;
    if (color == 'b')maximizeSearch = false;
}

void testRun(){
    while (true){
        std::string move_uci;
        std::getline(std::cin, move_uci);
        if (move_uci == "end") {
            break;
        }
        if (move_uci != "start") {
            Move enemyMove = uci::uciToMove(myBoard ,move_uci);
            myBoard.makeMove(enemyMove);
        }

        auto [eval, move] = minimax(myBoard, 4, NEGINF, INF, maximizeSearch);
        myBoard.makeMove(move);
        std::string moveUCI = uci::moveToUci(move);
        std::cout << moveUCI << std::endl;
        std::cout << eval << std::endl;
        std::cout << std::flush;
    }
}
int main() {
    int r = (int)Square(63).file();
    std::cout << r << std::endl;
//    initTables();
//    setColor();
//    setupBoard();
//    run(4);
//    return 0;
}

