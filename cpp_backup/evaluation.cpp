#include <vector>
#include <map>
#include "evaluation.h"
#include "game_tables.h"


std::array<int, 2> scores;
std::array<int, 2> mg;
std::array<int, 2> eg;
int gamePhase;

std::map<PieceType, int> ATTACK_VALUES = {
        {PieceType::PAWN, 5},
        {PieceType::KNIGHT, 8},
        {PieceType::BISHOP, 8},
        {PieceType::ROOK, 10},
        {PieceType::QUEEN, 15},
        {PieceType::KING, 15}
};

std::map<PieceType, int> DEFEND_VALUES = {
        {PieceType::PAWN, 20},
        {PieceType::KNIGHT, 10},
        {PieceType::BISHOP, 10},
        {PieceType::ROOK, 5},
        {PieceType::QUEEN, 0},
        {PieceType::KING, 0}
};

std::vector<PieceType> PIECETYPES = {
        PieceType::PAWN,
        PieceType::KNIGHT,
        PieceType::BISHOP,
        PieceType::ROOK,
        PieceType::QUEEN,
        PieceType::KING
};

void initEval(){
    scores = {0, 0};
    mg = {0, 0};
    eg = {0, 0};
    gamePhase = 0;
}

void incPestoValues(int colorIndex, int pc, int sqrIndex){
    mg[colorIndex] += mg_table[pc][sqrIndex];
    eg[colorIndex] += eg_table[pc][sqrIndex];
    gamePhase += gamephaseInc[pc];
}

void addAttackDefendValues(const Board& board, Bitboard controlledSquares, Color color){
    int colorIndex = static_cast<int>(color);
    for(PieceType type : PIECETYPES){
        Bitboard enemyPieceBitboard = board.pieces(type, ~color);
        Bitboard friendlyPieceBitboard = board.pieces(type, color);
        Bitboard attackedPieces = enemyPieceBitboard & controlledSquares;
        Bitboard defendedPieces = friendlyPieceBitboard & controlledSquares;
        scores[colorIndex] += attackedPieces.count() * ATTACK_VALUES[type];
        scores[colorIndex] += defendedPieces.count() * DEFEND_VALUES[type];
    }
}

void evaluateBlockedPieces(const Board& board, Color color){
    std::vector<PieceType> blockedPieces = {PieceType::BISHOP, PieceType::ROOK, PieceType::QUEEN};
    std::map<PieceType, std::function<Bitboard(Square, Bitboard)>> pieceTypeToAttackFunction = {
            {PieceType::BISHOP, attacks::bishop},
            {PieceType::ROOK, attacks::rook},
            {PieceType::QUEEN, attacks::queen}
    };
    Bitboard occ = board.occ();
    int colorIndex = static_cast<int>(color);
    for (chess::PieceType type: blockedPieces) {
        int pc = static_cast<int>(type) * 2 + colorIndex;
        Bitboard pieceBits = board.pieces(type, color);
        while(pieceBits != 0){
            int sqrIndex = pieceBits.pop();
            incPestoValues(colorIndex, pc, sqrIndex);
            Bitboard controlledSquares = pieceTypeToAttackFunction[type](sqrIndex, occ);
            addAttackDefendValues(board, controlledSquares, color);
        }
    }

}

void evaluatePawns(const Board& board, Color color){
    Bitboard leftAttacks;
    Bitboard rightAttacks;
    Bitboard pawnBits = board.pieces(PieceType::PAWN, color);
    int colorIndex = static_cast<int>(color);
    int pc = static_cast<int>(PieceType::PAWN) * 2 + colorIndex;
    if (color == Color::WHITE) {
        leftAttacks = attacks::pawnLeftAttacks<Color::WHITE>(pawnBits);
        rightAttacks = attacks::pawnRightAttacks<Color::WHITE>(pawnBits);
    }
    else{
        leftAttacks = attacks::pawnLeftAttacks<Color::BLACK>(pawnBits);
        rightAttacks = attacks::pawnRightAttacks<Color::BLACK>(pawnBits);
    }
    addAttackDefendValues(board, leftAttacks, color);
    addAttackDefendValues(board, rightAttacks, color);
    while(pawnBits != 0){
        int sqrIndex = pawnBits.pop();
        incPestoValues(colorIndex, pc, sqrIndex);
    }
}

void evaluateKing(const Board& board, Color color){
    int colorIndex = static_cast<int>(color);
    int pc = static_cast<int>(PieceType::KING) * 2 + colorIndex;
    Square kingSquare = board.kingSq(color);
    int sqrIndex = kingSquare.index();
    Bitboard controlledSquares = attacks::king(sqrIndex);
    incPestoValues(colorIndex, pc, sqrIndex);
    addAttackDefendValues(board, controlledSquares, color);
}

void evaluateKnights(const Board& board, Color color){
    int colorIndex = static_cast<int>(color);
    Bitboard knightBits = board.pieces(PieceType::KNIGHT, color);
    int pc = static_cast<int>(PieceType::KNIGHT) * 2 + colorIndex;
    while(knightBits != 0){
        int sqrIndex = knightBits.pop();
        Bitboard controlledSquares = attacks::knight(sqrIndex);
        incPestoValues(colorIndex, pc, sqrIndex);
        addAttackDefendValues(board, controlledSquares, color);
    }
}

int evaluate_board(const Board& board, GameResult result, GameResultReason reason) {
    int evaluation = 0;
    initEval();
    if (reason == GameResultReason::CHECKMATE) {
        return board.sideToMove() == Color::WHITE
               ? NEGINF
               : INF;
    }
    if (result == GameResult::DRAW) {
        return 0;
    }
    Board::CastlingRights rights = board.castlingRights();
    if (rights.has(Color::WHITE)) {
        evaluation += castle_rights_bonus;
    }
    if (rights.has(Color::BLACK)) {
        evaluation -= castle_rights_bonus;
    }
    evaluation += evaluatePieces(board);
    return evaluation;
}

int endgameMateEval(const Board& board, int egPhase, int currEval){
    std::vector<Square> cornerSquares = {Square(0), Square(7), Square(63), Square(56)};
    std::vector<Square> centerSquares = {Square(27), Square(28), Square(35), Square(36)};
    Square whiteKingSquare = board.kingSq(Color::WHITE);
    Square blackKingSquare = board.kingSq(Color::BLACK);
    int minWhiteCornerDistance = 0;
    int minBlackCornerDistance = 0;
    int maxWhiteCenterDistance = 0;
    int maxBlackCenterDistance = 0;
    int whiteKingRank = whiteKingSquare.rank();
    int blackKingRank = blackKingSquare.rank();
    int whiteKingFile = whiteKingSquare.file();
    int blackKingFile = blackKingSquare.file();
    double egWeight = egPhase;
    int eval = 0;
    int distanceBetweenKings = abs(whiteKingFile-blackKingFile)+abs(whiteKingRank-blackKingRank);

    for (const auto& corner : cornerSquares) {
        minBlackCornerDistance = std::min(minBlackCornerDistance, Square::distance(blackKingSquare, corner));
        minWhiteCornerDistance = std::min(minWhiteCornerDistance, Square::distance(whiteKingSquare, corner));
    }

    for (const auto& center : centerSquares) {
        maxBlackCenterDistance = std::max(maxBlackCenterDistance, Square::distance(blackKingSquare, center));
        maxWhiteCenterDistance = std::max(maxWhiteCenterDistance, Square::distance(whiteKingSquare, center));

    }
    eval += (4 - maxWhiteCenterDistance)*egWeight;
    eval -= (4 - maxBlackCenterDistance)*egWeight;
    eval += (3 - minBlackCornerDistance)*egWeight;
    eval -= (3 - minWhiteCornerDistance)*egWeight;
    if (currEval>=300){
        eval += (14 - distanceBetweenKings)*egWeight;
    }
    if(currEval <= -300){
        eval -= (14 - distanceBetweenKings)*egWeight;
    }
    return eval;

}

int evaluatePieces(const Board& board) {
    chess::Color white = Color::WHITE;
    chess::Color black = ~white;
    for(Color color : {white, black}){
        evaluatePawns(board, color);
        evaluateKnights(board, color);
        evaluateBlockedPieces(board, color);
        evaluateKing(board, color);
    }
    int eval = scores[0] - scores[1];
    int mgScore = mg[0] - mg[1];
    int egScore = eg[0] - eg[1];
    int mgPhase = gamePhase > 24 ? 24 : gamePhase;
    int egPhase = 24 - mgPhase;
    eval += (mgScore * mgPhase + egScore * egPhase) / 24;
    if (egPhase>=16){
        eval += endgameMateEval(board, egPhase, eval);
    }
    return eval;
}