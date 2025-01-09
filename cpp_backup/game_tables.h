#ifndef GAMETABLES_H
#define GAMETABLES_H

#include <array>
#include <cstdint>

// Values
const std::array<int16_t, 6> mg_value = {82, 337, 365, 477, 1025, 0};
const std::array<int16_t, 6> eg_value = {94, 281, 297, 512, 936, 0};

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
void initTables();
constexpr int16_t PCOLOR(int16_t p);
constexpr int16_t FLIP(int16_t sq);

#endif // GAMETABLES_H
