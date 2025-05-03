# Compiler and flags
CXX := g++
CXXFLAGS := -std=c++17 -O2 -DNDEBUG -ffunction-sections -fdata-sections -flto
ifeq ($(OS),Windows_NT)
    # Detect if in PowerShell or CMD
    ifeq ($(findstring powershell,$(SHELL)),powershell)
        RM_DIR = Remove-Item -Recurse -Force
        RM_FILE = Remove-Item -Force
    else
        RM_DIR = rmdir /s /q -r
        RM_FILE = del /q
    endif
else
    RM_DIR = rm -rf
    RM_FILE = rm -f
endif
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
	@mkdir $(BUILD_DIR)
# Link object files into executable
$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $@ $^

# Compile .cpp to .o
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp
	$(CXX) $(CXXFLAGS) -I$(INCLUDE_DIR) -c $< -o $@

clean:
	$(call RM_DIR) build
	$(call RM_FILE,$(TARGET))
