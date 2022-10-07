#include "../_backend/cpp/utils.hpp"
#include <iostream>

template<class T>
void print(T val) {
    std::cout<<val<<std::endl;
}


int main() {
    LinearProbingMap<std::string, int> map;

    std::pair<std::string, int> pairs[] = {{"hello", 1}, {"aaa", 33}, {":D", 4}};
    std::sttring key = "hello";

    for (const auto& p: pairs) {
        map.add(p.first, p.second);
        print(map.get_to_string());
    }
    print("");

    std::string keys[] = {"hello", "aaa", ":D", "F"};
    for (const auto &k: keys) {
        try {
            print(map.get(k));
        }
        catch (const std::invalid_argument& e) {
            print("Key error");
        }
    }

    return 0;
}
