#include <vector>
#include <map>
#include "evaluation.h"
#include "game_tables.h"

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

std::vector<PieceType> pieces = {
        PieceType::PAWN,
        PieceType::KNIGHT,
        PieceType::BISHOP,
        PieceType::ROOK,
        PieceType::QUEEN,
        PieceType::KING
};

std::pair<GameResultReason, GameResult> gameOver(Board& board)  {
    if (board.isHalfMoveDraw()) return board.getHalfMoveDrawType();
    if (board.isInsufficientMaterial()) return {GameResultReason::INSUFFICIENT_MATERIAL, GameResult::DRAW};
    if (board.isRepetition(1)) return {GameResultReason::THREEFOLD_REPETITION, GameResult::DRAW};

    Movelist movelist;
    movegen::legalmoves(movelist, board);

    if (movelist.empty()) {
        if (board.inCheck()) return {GameResultReason::CHECKMATE, GameResult::LOSE};
        return {GameResultReason::STALEMATE, GameResult::DRAW};
    }

    return {GameResultReason::NONE, GameResult::NONE};
}

int countActiveBits(uint64_t num) {
    return static_cast<int >(__builtin_popcountll(num));
}

std::vector<Square> getOccupiedSquares(Bitboard bitboard) {
    std::vector<Square> occupiedSquares;
    for (int i = 0; i < 64; ++i) {
        if (bitboard & (1ULL << i)) {
            occupiedSquares.push_back(Square(i));
        }
    }
    return occupiedSquares;
}



int evaluate_board(const Board& board, GameResult result, GameResultReason reason) {
    int evaluation = 0;
    if (reason == GameResultReason::CHECKMATE) {
        return board.sideToMove() == Color::WHITE
               ? NEGATIVEINFINITY
               : INFINITY;
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

int endgameMateEval(Square whiteKingSquare, Square blackKingSquare, int egPhase, int currEval){
    std::vector<Square> cornerSquares = {Square(0), Square(7), Square(63), Square(56)};
    int maxWhiteDistance = 0;
    int maxBlackDistance = 0;
    int egWeight = egPhase;
    int eval = 0;
    int distanceBetweenKings = Square::distance(whiteKingSquare, blackKingSquare);

    for (const auto& corner : cornerSquares) {
        maxWhiteDistance = std::min(maxWhiteDistance, Square::distance(whiteKingSquare, corner));
    }

    for (const auto& corner : cornerSquares) {
        maxBlackDistance = std::min(maxBlackDistance, Square::distance(blackKingSquare, corner));
    }
    if (currEval>=0){
        eval += (3 - maxBlackDistance)*egWeight;
        eval += (7 - distanceBetweenKings)*egWeight;
    }
    else{
        eval -= (3 - maxWhiteDistance)*egWeight;
        eval -= (7 - distanceBetweenKings)*egWeight;
    }
  


    return eval;

}

int evaluatePieces(const Board& board) {
    std::map<std::pair<PieceType, Color>, Bitboard> pieceToBitboardMap;
    chess::Color white = chess::Color::WHITE;
    chess::Color black = ~white;
    std::array<int, 2> scores = {0, 0};
    std::array<int, 2> mg = {0, 0};
    std::array<int, 2> eg = {0, 0};
    int gamePhase = 0;

    Bitboard allBits = board.occ();
    std::vector<PieceType> blockedPieces = {PieceType::BISHOP, PieceType::ROOK, PieceType::QUEEN};

    // White bits
    pieceToBitboardMap[{PieceType::PAWN, white}] = board.pieces(PieceType::PAWN, white);
    pieceToBitboardMap[{PieceType::KNIGHT, white}] = board.pieces(PieceType::KNIGHT, white);
    pieceToBitboardMap[{PieceType::BISHOP, white}] = board.pieces(PieceType::BISHOP, white);
    pieceToBitboardMap[{PieceType::ROOK, white}] = board.pieces(PieceType::ROOK, white);
    pieceToBitboardMap[{PieceType::QUEEN, white}] = board.pieces(PieceType::QUEEN, white);
    pieceToBitboardMap[{PieceType::KING, white}] = board.pieces(PieceType::KING, white);

    // Black bits
    pieceToBitboardMap[{PieceType::PAWN, black}] = board.pieces(PieceType::PAWN, black);
    pieceToBitboardMap[{PieceType::KNIGHT, black}] = board.pieces(PieceType::KNIGHT, black);
    pieceToBitboardMap[{PieceType::BISHOP, black}] = board.pieces(PieceType::BISHOP, black);
    pieceToBitboardMap[{PieceType::ROOK, black}] = board.pieces(PieceType::ROOK, black);
    pieceToBitboardMap[{PieceType::QUEEN, black}] = board.pieces(PieceType::QUEEN, black);
    pieceToBitboardMap[{PieceType::KING, black}] = board.pieces(PieceType::KING, black);


    // function mapping
    std::map<PieceType, std::function<Bitboard(Square, Bitboard)>> pieceTypeToAttackFunction = {
            {PieceType::BISHOP, attacks::bishop},
            {PieceType::ROOK, attacks::rook},
            {PieceType::QUEEN, attacks::queen}
    };

    std::map<std::pair<PieceType, Color>, std::vector<Square>> pieceColorToSquares;

    pieceColorToSquares[{PieceType::PAWN, white}] = getOccupiedSquares(pieceToBitboardMap[{PieceType::PAWN, white}]);
    pieceColorToSquares[{PieceType::KNIGHT, white}] = getOccupiedSquares(pieceToBitboardMap[{PieceType::KNIGHT, white}]);
    pieceColorToSquares[{PieceType::BISHOP, white}] = getOccupiedSquares(pieceToBitboardMap[{PieceType::BISHOP, white}]);
    pieceColorToSquares[{PieceType::ROOK, white}] = getOccupiedSquares(pieceToBitboardMap[{PieceType::ROOK, white}]);
    pieceColorToSquares[{PieceType::QUEEN, white}] = getOccupiedSquares(pieceToBitboardMap[{PieceType::QUEEN, white}]);

    pieceColorToSquares[{PieceType::PAWN, black}] = getOccupiedSquares(pieceToBitboardMap[{PieceType::PAWN, black}]);
    pieceColorToSquares[{PieceType::KNIGHT, black}] = getOccupiedSquares(pieceToBitboardMap[{PieceType::KNIGHT, black}]);
    pieceColorToSquares[{PieceType::BISHOP, black}] = getOccupiedSquares(pieceToBitboardMap[{PieceType::BISHOP, black}]);
    pieceColorToSquares[{PieceType::ROOK, black}] = getOccupiedSquares(pieceToBitboardMap[{PieceType::ROOK, black}]);
    pieceColorToSquares[{PieceType::QUEEN, black}] = getOccupiedSquares(pieceToBitboardMap[{PieceType::QUEEN, black}]);



    // King eval
    for (chess::Color color : {white, black}){
        int colorIndex = static_cast<int>(color);
        Square sqr = board.kingSq(color);
        int sqrIndex = sqr.index();
        int pc = static_cast<int>(PieceType::KING) * 2 + colorIndex;
        mg[colorIndex] += mg_table[pc][sqrIndex];
        eg[colorIndex] += eg_table[pc][sqrIndex];
        gamePhase += gamephaseInc[pc];
        Bitboard attackedSquares = attacks::king(sqr);
        for(PieceType type : pieces){
            Bitboard enemyPieceBitboard = pieceToBitboardMap[{type, ~color}];
            Bitboard friendlyPieceBitboard = pieceToBitboardMap[{type, color}];
            Bitboard attackedPieces = enemyPieceBitboard & attackedSquares;
            Bitboard defendedPieces = friendlyPieceBitboard & attackedSquares;
            scores[colorIndex] += countActiveBits(attackedPieces.getBits()) * ATTACK_VALUES[type];
            scores[colorIndex] += countActiveBits(defendedPieces.getBits()) * DEFEND_VALUES[type];
        }
    }

    // Knight eval
    for (chess::Color color : {white, black}){
        int colorIndex = static_cast<int>(color);
        std::vector<Square> squares = pieceColorToSquares[{PieceType::KNIGHT, color}];
        int pc = static_cast<int>(PieceType::KNIGHT) * 2 + colorIndex;

        for (Square sqr: squares) {
            int sqrIndex = sqr.index();
            mg[colorIndex] += mg_table[pc][sqrIndex];
            eg[colorIndex] += eg_table[pc][sqrIndex];
            gamePhase += gamephaseInc[pc];

            Bitboard attackedSquares = attacks::knight(sqr);
            for(PieceType type : pieces){
                Bitboard enemyPieceBitboard = pieceToBitboardMap[{type, ~color}];
                Bitboard friendlyPieceBitboard = pieceToBitboardMap[{type, color}];
                Bitboard attackedPieces = enemyPieceBitboard & attackedSquares;
                Bitboard defendedPieces = friendlyPieceBitboard & attackedSquares;
                scores[colorIndex] += countActiveBits(attackedPieces.getBits()) * ATTACK_VALUES[type];
                scores[colorIndex] += countActiveBits(defendedPieces.getBits()) * DEFEND_VALUES[type];
            }
        }
    }


    // Pawn eval
    Bitboard leftAttacks;
    Bitboard rightAttacks;
    for (chess::Color color : {white, black}) {
        int colorIndex = static_cast<int>(color);
        std::vector<Square> squares = pieceColorToSquares[{PieceType::PAWN, color}];
        int pc = static_cast<int>(PieceType::PAWN) * 2 + colorIndex;

        for (Square sqr : squares){
            int sqrIndex = sqr.index();
            mg[colorIndex] += mg_table[pc][sqrIndex];
            eg[colorIndex] += eg_table[pc][sqrIndex];
            gamePhase += gamephaseInc[pc];

        }
        if (color == Color::WHITE) {
            leftAttacks = attacks::pawnLeftAttacks<Color::WHITE>(pieceToBitboardMap[{PieceType::PAWN, color}]);
            rightAttacks = attacks::pawnRightAttacks<Color::WHITE>(pieceToBitboardMap[{PieceType::PAWN, color}]);
        }
        else{
            leftAttacks = attacks::pawnLeftAttacks<Color::BLACK>(pieceToBitboardMap[{PieceType::PAWN, color}]);
            rightAttacks = attacks::pawnRightAttacks<Color::BLACK>(pieceToBitboardMap[{PieceType::PAWN, color}]);
        }
        for(PieceType type : pieces){
            Bitboard enemyPieceBitboard = pieceToBitboardMap[{type, ~color}];
            Bitboard friendlyPieceBitboard = pieceToBitboardMap[{type, color}];
            Bitboard leftAttackedPieces = enemyPieceBitboard & leftAttacks;
            Bitboard rightAttackedPieces = enemyPieceBitboard & rightAttacks;
            Bitboard leftDefendedPieces = friendlyPieceBitboard & leftAttacks;
            Bitboard rightDefendedPieces = friendlyPieceBitboard & rightAttacks;
            scores[colorIndex] += countActiveBits(leftAttackedPieces.getBits()) * ATTACK_VALUES[type];
            scores[colorIndex] += countActiveBits(rightAttackedPieces.getBits()) * ATTACK_VALUES[type];
            scores[colorIndex] += countActiveBits(leftDefendedPieces.getBits()) * DEFEND_VALUES[type];
            scores[colorIndex] += countActiveBits(rightDefendedPieces.getBits()) * DEFEND_VALUES[type];
        }
    }



    // Bishop, Rook, Queen control values
    for (chess::Color color : {white, black}) {
        int colorIndex = static_cast<int>(color);
        for (chess::PieceType type: blockedPieces) {
            std::vector<Square> squares = pieceColorToSquares[{type, color}];
            int pc = static_cast<int>(type) * 2 + colorIndex;

            for (Square sqr : squares){
                int sqrIndex = sqr.index();
                mg[colorIndex] += mg_table[pc][sqrIndex];
                eg[colorIndex] += eg_table[pc][sqrIndex];
                gamePhase += gamephaseInc[pc];

                Bitboard attacks = pieceTypeToAttackFunction[type](sqr, allBits);


                for(PieceType controlled_type : pieces){
                    Bitboard enemyPieceBitboard = pieceToBitboardMap[{controlled_type, ~color}];
                    Bitboard friendlyPieceBitboard = pieceToBitboardMap[{controlled_type, color}];
                    Bitboard attackedPieces = enemyPieceBitboard & attacks;
                    Bitboard defendedPieces = friendlyPieceBitboard & attacks;
                    scores[colorIndex] += countActiveBits(attackedPieces.getBits()) * ATTACK_VALUES[controlled_type];
                    scores[colorIndex] += countActiveBits(defendedPieces.getBits()) * DEFEND_VALUES[controlled_type];

                }
            }
        }
    }

    int eval = scores[0] - scores[1];
    int mgScore = mg[0] - mg[1];
    int egScore = eg[0] - eg[1];
    int mgPhase = gamePhase > 24 ? 24 : gamePhase;
    int egPhase = 24 - mgPhase;
    eval += (mgScore * mgPhase + egScore * egPhase) / 24;
    eval += endgameMateEval(board.kingSq(white), board.kingSq(black), egPhase, eval);
    return eval;
}