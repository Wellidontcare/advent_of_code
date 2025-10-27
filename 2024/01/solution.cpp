#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <ranges>
#include <iostream>
#include <algorithm>
#include <numeric>

template <int pos>
struct ID {
    int id;

    friend std::istream &operator>>(std::istream &s, ID &id) {
        static_assert(pos < 2);
        std::string line_str;
        std::getline(s, line_str);
        std::stringstream line(line_str);
        int discard;
        if constexpr(pos == 0) {
            line >> id.id;
            line >> discard;
        } else {
            line >> discard;
            line >> id.id;
        }
        return s;
    }
};

int solve(const std::string& input_file) {
    std::ifstream file(input_file);
    auto left = std::views::istream<ID<0>>(file) | std::views::transform([](auto id) { return id.id;})  | std::ranges::to<std::vector<int>>();
    file.clear();
    file.seekg(0);
    auto right = std::views::istream<ID<1>>(file) | std::views::transform([](auto id) { return id.id;})  | std::ranges::to<std::vector<int>>();
    std::sort(std::begin(left), std::end(left));
    std::sort(std::begin(right), std::end(right));
    std::vector<int> distances(left.size());
    std::transform(std::begin(left), std::end(left), std::begin(right), std::begin(distances), [](int a, int b) {
            return abs(a - b); });
    return std::accumulate(std::begin(distances), std::end(distances), 0);
}

int main() {
    std::cout << solve("./input.txt");
    return 0;
}
