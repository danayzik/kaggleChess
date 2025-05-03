
SRC_DIR := bot_files/src
OUT_DIR := players
TARGET := $(OUT_DIR)/chessBot
SOURCES := $(wildcard $(SRC_DIR)/*.cpp)



all:
	g++ -std=c++17 -O2 -DNDEBUG -ffunction-sections -fdata-sections -flto -Ibot_files/src -o $(TARGET) $(SOURCES)



