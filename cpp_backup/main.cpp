#include "chess.hpp"
#include "game_tables.h"
#include "evaluation.h"
#include "search.h"

Board myBoard;
bool maximizeSearch;

std::vector<std::string> split(const std::string& str) {
    std::vector<std::string> parts;
    std::istringstream stream(str);
    std::string part;
    while (stream >> part) {
        parts.push_back(part);
    }
    return parts;
}

void run(){
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
        auto [eval, move] = minimax(myBoard, 3, NEGATIVEINFINITY, INFINITY, maximizeSearch, false);
        myBoard.makeMove(move);
        std::string moveUCI = uci::moveToUci(move);
        std::cout << moveUCI << std::endl;
        std::cout << eval << std::endl;
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

void test_rep(){
    Move e2f2 = uci::uciToMove(myBoard, "e2f2");
    Move f2e2 = uci::uciToMove(myBoard, "f2e2");
    Move h3c3 = uci::uciToMove(myBoard, "h3c3");
    Move c3h3 = uci::uciToMove(myBoard, "c3h3");
    myBoard.makeMove(e2f2);
    myBoard.makeMove(h3c3);
    myBoard.makeMove(f2e2);
    myBoard.makeMove(c3h3);
    myBoard.makeMove(e2f2);
    myBoard.makeMove(h3c3);
    myBoard.makeMove(f2e2);
//    myBoard.makeMove(c3h3);
    std::cout << (myBoard.isRepetition() == true) << std::endl;
}



int main() {
//    initTables();
//    Board board = Board("8/6k1/8/8/8/7r/2K5/8 b - - 0 1");
//    Board board2 = Board("8/8/5k2/8/8/7r/3K4/8 b - - 0 1");
//    std::cout << evaluate_board(board, GameResult::NONE, GameResultReason::NONE) << std::endl;
//    std::cout << evaluate_board(board2, GameResult::NONE, GameResultReason::NONE)<< std::endl;
    initTables();
    setColor();
    setupBoard();


////    evaluate_board(myBoard, GameResult::NONE, GameResultReason::NONE);
//
//
    run();
    return 0;


}

