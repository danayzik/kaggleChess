#include <vector>
#include <map>
#include "evaluation.h"
#include "game_tables.h"

std::map<PieceType, int16_t> ATTACK_VALUES = {
        {PieceType::PAWN, 5},
        {PieceType::KNIGHT, 1},
        {PieceType::BISHOP, 1},
        {PieceType::ROOK, 2},
        {PieceType::QUEEN, 3},
        {PieceType::KING, 5}
};

std::map<PieceType, int16_t> DEFEND_VALUES = {
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

int16_t countActiveBits(uint64_t num) {
    return static_cast<int16_t >(__builtin_popcountll(num));
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



int16_t evaluate_board(const Board& board) {
    int16_t evaluation = 0;
    std::pair<GameResultReason, GameResult> gameOverCheck = board.isGameOver();
    GameResultReason resultReason = gameOverCheck.first;
    if (resultReason == GameResultReason::CHECKMATE) {
        return board.sideToMove() == Color::WHITE
               ? NEGATIVEINFINITY
               : INFINITY;
    }
    if (gameOverCheck.second == GameResult::DRAW) {
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

int16_t evaluatePieces(const chess::Board& board) {
    std::map<std::pair<PieceType, Color>, Bitboard> pieceToBitboardMap;
    chess::Color white = chess::Color::WHITE;
    chess::Color black = ~white;
    std::array<int16_t, 2> scores = {0, 0};
    std::array<int16_t, 2> mg = {0, 0};
    std::array<int16_t, 2> eg = {0, 0};
    int16_t gamePhase = 0;

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
        int colorIndex = static_cast<std::int8_t>(color);
        Square sqr = board.kingSq(color);
        int sqrIndex = sqr.index();

        int pc = static_cast<std::int8_t>(PieceType::KING) * 2 + colorIndex;
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
        int colorIndex = static_cast<int8_t>(color);
        std::vector<Square> squares = pieceColorToSquares[{PieceType::KNIGHT, color}];
        int pc = static_cast<std::int8_t>(PieceType::KNIGHT) * 2 + colorIndex;
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
        int colorIndex = static_cast<int8_t>(color);
        std::vector<Square> squares = pieceColorToSquares[{PieceType::PAWN, color}];
        int pc = static_cast<std::int8_t>(PieceType::PAWN) * 2 + colorIndex;
        for (Square sqr : squares){
            int8_t sqrIndex = sqr.index();

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
        int colorIndex = static_cast<int8_t>(color);
        for (chess::PieceType type: blockedPieces) {
            std::vector<Square> squares = pieceColorToSquares[{type, color}];
            int pc = static_cast<std::int8_t>(type) * 2 + colorIndex;
            for (Square sqr : squares){
                int8_t sqrIndex = sqr.index();
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


    int16_t eval = scores[0] - scores[1];
    int16_t mgScore = mg[0] - mg[1];
    int16_t egScore = eg[0] - eg[1];
    int16_t mgPhase = gamePhase > 24 ? 24 : gamePhase;
    int16_t egPhase = 24 - mgPhase;

    eval += (mgScore * mgPhase + egScore * egPhase) / 24;
    return eval;
}