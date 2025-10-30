#include <fstream>
#include <iostream>
#include <sstream>


enum class LevelDirection {
  increasing = 1,
  decreasing = -1,
  steady = 0,
};

enum class LevelSafety { safe = 1, unsafe = 0 };

struct LevelStatus {
    LevelDirection direction;
    LevelSafety safety;
};

LevelStatus level_status(int current, int next) {
    int level_diff = current - next;
    if(level_diff == 0) {
        return {LevelDirection::steady, LevelSafety::unsafe};
    }

    int level_diff_unsafe = abs(level_diff) > 3;
    if(level_diff < 0) {
        if(level_diff_unsafe) {
            return {LevelDirection::decreasing, LevelSafety::unsafe};
        }
        return {LevelDirection::decreasing, LevelSafety::safe};
    } else {
        if(level_diff_unsafe) {
            return {LevelDirection::increasing, LevelSafety::unsafe};
        }
        return {LevelDirection::increasing, LevelSafety::safe};
    }
}

int solve(const std::string &input_path, int max_unsafe_count = 0) {
  std::fstream file(input_path, std::ios::in);
  std::string line;
  LevelStatus status{};
  int good_lines{};
  while (std::getline(file, line)) {
    int last_number{};
    int number{};

    std::stringstream line_stream(line);
    (void)(line_stream >> last_number >> number);
    auto status = level_status(last_number, number);
    auto line_direction = status.direction;

    bool bad_line = false;

    int unsafe_count = 0;
    // edge case when direction is steady at the start we have no line direction
    while (line_direction == LevelDirection::steady &&
           unsafe_count++ <= max_unsafe_count) {
      last_number = number;
      if (!(line_stream >> number)) {
        break;
      }
      status = level_status(last_number, number);
      line_direction = status.direction;
    }

    if(unsafe_count > max_unsafe_count) {
      continue;
    }
    while (!bad_line) {
      status = level_status(last_number, number);
      if ((status.direction != line_direction ||
           status.safety == LevelSafety::unsafe) &&
          unsafe_count++ >= max_unsafe_count) {
        bad_line = true;
      }
      last_number = number;
      if (!(line_stream >> number)) {
        break;
      }
    }
    if(bad_line) {
    } else {
      good_lines++;
    }
  }
  return good_lines;
}

int main() { 
    std::cout << "Example 1: " << solve("example_input.txt", 0) << '\n';
    std::cout << "Example 2: " << solve("example_input.txt", 1) << '\n';
    std::cout << "Solution 1: " << solve("input.txt", 0) << '\n';
    std::cout << "Solution 2: " << solve("input.txt", 1) << '\n';
}
