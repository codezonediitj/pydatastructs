#include "algorithms.hpp"
#include <vector>
#include <string>
#include <unordered_map>
#include <cmath>

// Knuth-Morris-Pratt Algorithm
std::vector<int> kmp_search(const std::string& text, const std::string& query) {
    std::vector<int> positions;
    if (text.empty() || query.empty()) return positions;

    // Build KMP table
    std::vector<int> kmp_table(query.size() + 1, 0);
    kmp_table[0] = -1;
    int pos = 1, cnd = 0;
    while (pos < query.size()) {
        if (query[pos] == query[cnd]) {
            kmp_table[pos] = kmp_table[cnd];
        } else {
            kmp_table[pos] = cnd;
            while (cnd >= 0 && query[pos] != query[cnd]) {
                cnd = kmp_table[cnd];
            }
        }
        pos++, cnd++;
    }
    kmp_table[pos] = cnd;

    // Perform search
    int j = 0, k = 0;
    while (j < text.size()) {
        if (query[k] == text[j]) {
            j++, k++;
            if (k == query.size()) {
                positions.push_back(j - k);
                k = kmp_table[k];
            }
        } else {
            k = kmp_table[k];
            if (k < 0) {
                j++, k++;
            }
        }
    }

    return positions;
}

// Rabin-Karp Algorithm
std::vector<int> rabin_karp_search(const std::string& text, const std::string& query) {
    std::vector<int> positions;
    if (text.empty() || query.empty()) return positions;

    const int PRIME = 257;
    const int MOD = 1000000007;
    int t = text.size(), q = query.size();
    long long query_hash = 0, text_hash = 0, power = 1;

    // Precompute power
    for (int i = 0; i < q - 1; i++) {
        power = (power * PRIME) % MOD;
    }

    // Compute hash for query and first window of text
    for (int i = 0; i < q; i++) {
        query_hash = (query_hash * PRIME + query[i]) % MOD;
        text_hash = (text_hash * PRIME + text[i]) % MOD;
    }

    // Slide the window over the text
    for (int i = 0; i <= t - q; i++) {
        if (query_hash == text_hash) {
            if (text.substr(i, q) == query) {
                positions.push_back(i);
            }
        }
        if (i < t - q) {
            text_hash = (PRIME * (text_hash - text[i] * power) + text[i + q]) % MOD;
            if (text_hash < 0) text_hash += MOD;
        }
    }

    return positions;
}

// Boyer-Moore Algorithm
std::vector<int> boyer_moore_search(const std::string& text, const std::string& query) {
    std::vector<int> positions;
    if (text.empty() || query.empty()) return positions;

    // Preprocessing
    std::unordered_map<char, int> bad_match_table;
    for (int i = 0; i < query.size(); i++) {
        bad_match_table[query[i]] = i;
    }

    // Searching
    int shift = 0;
    while (shift <= text.size() - query.size()) {
        int j = query.size() - 1;
        while (j >= 0 && query[j] == text[shift + j]) {
            j--;
        }
        if (j < 0) {
            positions.push_back(shift);
            shift += (shift + query.size() < text.size()) ? query.size() - bad_match_table[text[shift + query.size()]] : 1;
        } else {
            shift += std::max(1, j - bad_match_table[text[shift + j]]);
        }
    }

    return positions;
}

// Z-Function Algorithm
std::vector<int> z_function_search(const std::string& text, const std::string& query) {
    std::vector<int> positions;
    if (text.empty() || query.empty()) return positions;

    std::string combined = query + "$" + text;
    std::vector<int> z(combined.size(), 0);
    int l = 0, r = 0;

    for (int i = 1; i < combined.size(); i++) {
        if (i <= r) {
            z[i] = std::min(r - i + 1, z[i - l]);
        }
        while (i + z[i] < combined.size() && combined[z[i]] == combined[i + z[i]]) {
            z[i]++;
        }
        if (i + z[i] - 1 > r) {
            l = i, r = i + z[i] - 1;
        }
    }

    for (int i = query.size() + 1; i < combined.size(); i++) {
        if (z[i] == query.size()) {
            positions.push_back(i - query.size() - 1);
        }
    }

    return positions;
}