# Compiler and flags
CXX := g++
CXXFLAGS := -std=c++17 -O2 -DNDEBUG -ffunction-sections -fdata-sections -flto

# Directories
SRC_DIR := bot_files/src
INCLUDE_DIR := bot_files/include
BUILD_DIR := build
OUT_DIR := players
TARGET := $(OUT_DIR)/chessBot

# Source and object files
SOURCES := $(wildcard $(SRC_DIR)/*.cpp)
OBJECTS := $(patsubst $(SRC_DIR)/%.cpp, $(BUILD_DIR)/%.o, $(SOURCES))

# Default target
all: $(TARGET)

# Link object files into executable
$(TARGET): $(OBJECTS)
	@mkdir -p $(OUT_DIR)
	$(CXX) $(CXXFLAGS) -o $@ $^

# Compile .cpp to .o
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -I$(INCLUDE_DIR) -c $< -o $@

# Clean up
clean:
	rm -rf $(BUILD_DIR) $(TARGET)
