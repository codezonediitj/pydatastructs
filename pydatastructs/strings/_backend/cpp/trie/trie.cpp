#include "trie.hpp"

TrieNode::~TrieNode() {
    for (auto& pair : children) {
        delete pair.second;
    }
}

Trie::Trie() {
    root = new TrieNode();
}

Trie::~Trie() {
    delete root;
}

void Trie::insert(const std::string& word) {
    TrieNode* current = root;
    for (char ch : word) {
        if (current->children.find(ch) == current->children.end()) {
            current->children[ch] = new TrieNode(ch);
        }
        current = current->children[ch];
    }
    current->is_terminal = true;
}

bool Trie::search(const std::string& word) {
    TrieNode* current = root;
    for (char ch : word) {
        if (current->children.find(ch) == current->children.end()) {
            return false;
        }
        current = current->children[ch];
    }
    return current->is_terminal;
}

bool Trie::starts_with(const std::string& prefix) {
    TrieNode* current = root;
    for (char ch : prefix) {
        if (current->children.find(ch) == current->children.end()) {
            return false;
        }
        current = current->children[ch];
    }
    return true;
}

std::vector<std::string> Trie::strings_with_prefix(const std::string& prefix) {
    std::vector<std::string> result;
    TrieNode* current = root;
    for (char ch : prefix) {
        if (current->children.find(ch) == current->children.end()) {
            return result;
        }
        current = current->children[ch];
    }
    // Perform DFS to collect all strings with the given prefix
    std::vector<std::pair<TrieNode*, std::string>> stack;
    stack.push_back({current, prefix});
    while (!stack.empty()) {
        auto [node, str] = stack.back();
        stack.pop_back();
        if (node->is_terminal) {
            result.push_back(str);
        }
        for (auto& pair : node->children) {
            stack.push_back({pair.second, str + pair.first});
        }
    }
    return result;
}