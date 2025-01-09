#ifndef GAME_H
#define GAME_H

#include <array>
#include <cstdint>

// Piece definitions
constexpr int16_t PAWN = 0;
constexpr int16_t KNIGHT = 1;
constexpr int16_t BISHOP = 2;
constexpr int16_t ROOK = 3;
constexpr int16_t QUEEN = 4;
constexpr int16_t KING = 5;

// Board representation
constexpr int16_t WHITE = 0;
constexpr int16_t BLACK = 1;

constexpr int16_t WHITE_PAWN = (2 * PAWN + WHITE);
constexpr int16_t BLACK_PAWN = (2 * PAWN + BLACK);
constexpr int16_t WHITE_KNIGHT = (2 * KNIGHT + WHITE);
constexpr int16_t BLACK_KNIGHT = (2 * KNIGHT + BLACK);
constexpr int16_t WHITE_BISHOP = (2 * BISHOP + WHITE);
constexpr int16_t BLACK_BISHOP = (2 * BISHOP + BLACK);
constexpr int16_t WHITE_ROOK = (2 * ROOK + WHITE);
constexpr int16_t BLACK_ROOK = (2 * ROOK + BLACK);
constexpr int16_t WHITE_QUEEN = (2 * QUEEN + WHITE);
constexpr int16_t BLACK_QUEEN = (2 * QUEEN + BLACK);
constexpr int16_t WHITE_KING = (2 * KING + WHITE);
constexpr int16_t BLACK_KING = (2 * KING + BLACK);
constexpr int16_t EMPTY = (BLACK_KING + 1);

// Utility functions
constexpr int16_t PCOLOR(int16_t p);
constexpr int16_t FLIP(int16_t sq);


// Material and positional values
extern const std::array<int16_t, 6> mg_value;
extern const std::array<int16_t, 6> eg_value;

extern const std::array<int16_t, 64> mg_pawn_table;
extern const std::array<int16_t, 64> eg_pawn_table;
extern const std::array<int16_t, 64> mg_knight_table;
extern const std::array<int16_t, 64> eg_knight_table;
extern const std::array<int16_t, 64> mg_bishop_table;
extern const std::array<int16_t, 64> eg_bishop_table;
extern const std::array<int16_t, 64> mg_rook_table;
extern const std::array<int16_t, 64> eg_rook_table;
extern const std::array<int16_t, 64> mg_queen_table;
extern const std::array<int16_t, 64> eg_queen_table;
extern const std::array<int16_t, 64> mg_king_table;
extern const std::array<int16_t, 64> eg_king_table;

extern const std::array<const int16_t*, 6> mg_pesto_table;
extern const std::array<const int16_t*, 6> eg_pesto_table;

extern std::array<int16_t, 12> gamephaseInc;
extern std::array<std::array<int16_t, 64>, 12> mg_table;
extern std::array<std::array<int16_t, 64>, 12> eg_table;

// Function declarations
void init_tables();
int16_t eval(const std::array<int16_t, 64>& board);

#endif
