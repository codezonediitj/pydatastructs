#include <iostream>
#include <vector>
#include <stdexcept>
#include <memory>
#include <sstream>
#include <typeinfo>

namespace pydatastructs {

    // DynamicOneDimensionalArray implementation
    class DynamicOneDimensionalArray {
    private:
        std::vector<int> arr;
        
    public:
        void append(int x) {
            arr.push_back(x);
        }

        int get_last_filled() const {
            if (arr.empty()) {
                throw std::out_of_range("Array is empty");
            }
            return arr.back();
        }

        void delete_last() {
            if (arr.empty()) {
                throw std::out_of_range("Array is empty");
            }
            arr.pop_back();
        }

        size_t size() const {
            return arr.size();
        }

        std::string to_string() const {
            std::ostringstream oss;
            for (int val : arr) {
                oss << val << " ";
            }
            return oss.str();
        }

        void set_dtype(const std::type_info& type) {
            // In the context of C++, we typically don't need to worry about dynamic types like in Python.
        }
    };

    // SinglyLinkedList Node definition
    struct Node {
        int value;
        std::shared_ptr<Node> next;

        Node(int x) : value(x), next(nullptr) {}
    };

    // SinglyLinkedList implementation
    class SinglyLinkedList {
    private:
        std::shared_ptr<Node> head;
        size_t list_size;

    public:
        SinglyLinkedList() : head(nullptr), list_size(0) {}

        void append_left(int x) {
            auto new_node = std::make_shared<Node>(x);
            new_node->next = head;
            head = new_node;
            list_size++;
        }

        int pop_left() {
            if (head == nullptr) {
                throw std::out_of_range("List is empty");
            }
            int value = head->value;
            head = head->next;
            list_size--;
            return value;
        }

        int head_value() const {
            if (head == nullptr) {
                throw std::out_of_range("List is empty");
            }
            return head->value;
        }

        size_t size() const {
            return list_size;
        }

        std::string to_string() const {
            std::ostringstream oss;
            auto current = head;
            while (current) {
                oss << current->value << " ";
                current = current->next;
            }
            return oss.str();
        }
    };
}


namespace pydatastructs {
    // Forward declaration of the SinglyLinkedList and DynamicOneDimensionalArray
    class DynamicOneDimensionalArray;
    class SinglyLinkedList;

    enum class Backend { PYTHON, CPP };

    // Abstract Stack class
    class Stack {
    public:
        virtual ~Stack() {}
        virtual void push(int x) = 0;
        virtual int pop() = 0;
        virtual bool is_empty() const = 0;
        virtual int peek() const = 0;
        virtual size_t size() const = 0;
        virtual std::string to_string() const = 0;
    };

    // ArrayStack class for stack implementation using dynamic array
    class ArrayStack : public Stack {
    private:
        std::shared_ptr<DynamicOneDimensionalArray> items;
        
    public:
        ArrayStack(std::shared_ptr<DynamicOneDimensionalArray> items) : items(items) {}

        void push(int x) override {
            items->append(x);
        }

        int pop() override {
            if (is_empty()) {
                throw std::out_of_range("Stack is empty");
            }
            int top_element = items->get_last_filled();
            items->delete_last();
            return top_element;
        }

        bool is_empty() const override {
            return items->size() == 0;
        }

        int peek() const override {
            if (is_empty()) {
                throw std::out_of_range("Stack is empty");
            }
            return items->get_last_filled();
        }

        size_t size() const override {
            return items->size();
        }

        std::string to_string() const override {
            return items->to_string();
        }
    };

    // LinkedListStack class for stack implementation using singly linked list
    class LinkedListStack : public Stack {
    private:
        std::shared_ptr<SinglyLinkedList> stack;

    public:
        LinkedListStack(std::shared_ptr<SinglyLinkedList> stack) : stack(stack) {}

        void push(int x) override {
            stack->append_left(x);
        }

        int pop() override {
            if (is_empty()) {
                throw std::out_of_range("Stack is empty");
            }
            return stack->pop_left();
        }

        bool is_empty() const override {
            return stack->size() == 0;
        }

        int peek() const override {
            return stack->head_value();
        }

        size_t size() const override {
            return stack->size();
        }

        std::string to_string() const override {
            return stack->to_string();
        }
    };

    // Stack factory function
    std::shared_ptr<Stack> create_stack(const std::string& implementation, std::shared_ptr<DynamicOneDimensionalArray> items = nullptr, Backend backend = Backend::CPP) {
        if (implementation == "array") {
            if (backend == Backend::CPP) {
                // Use C++ backend for array stack
                return std::make_shared<ArrayStack>(items);
            } else {
                // Use Python backend or default
                return std::make_shared<ArrayStack>(items);
            }
        } else if (implementation == "linked_list") {
            if (backend != Backend::PYTHON) {
                throw std::invalid_argument("Linked list stack requires Python backend.");
            }
            return std::make_shared<LinkedListStack>(std::make_shared<SinglyLinkedList>());
        } else {
            throw std::invalid_argument("Implementation not supported");
        }
    }
}
