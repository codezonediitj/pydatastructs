#ifndef STRINGS_ALGORITHMS_HPP
#define STRINGS_ALGORITHMS_HPP

#include <Python.h>
#include <vector>
#include <string>
#include <unordered_map>
#include <cmath>

// Knuth-Morris-Pratt Algorithm
std::vector<int> kmp_search(const std::string& text, const std::string& query);

// Rabin-Karp Algorithm
std::vector<int> rabin_karp_search(const std::string& text, const std::string& query);

// Boyer-Moore Algorithm
std::vector<int> boyer_moore_search(const std::string& text, const std::string& query);

// Z-Function Algorithm
std::vector<int> z_function_search(const std::string& text, const std::string& query);

#endif