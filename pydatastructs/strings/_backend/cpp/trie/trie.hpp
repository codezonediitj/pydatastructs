#ifndef STRINGS_TRIE_HPP
#define STRINGS_TRIE_HPP

#include <Python.h>
#include <unordered_map>
#include <vector>
#include <string>

class TrieNode {
public:
    char character;
    bool is_terminal;
    std::unordered_map<char, TrieNode*> children;

    TrieNode(char ch = '\0') : character(ch), is_terminal(false) {}
    ~TrieNode();
};

class Trie {
public:
    TrieNode* root;

    Trie();
    ~Trie();

    void insert(const std::string& word);
    bool search(const std::string& word);
    bool starts_with(const std::string& prefix);
    std::vector<std::string> strings_with_prefix(const std::string& prefix);
};

#endif