#include <chrono>
#include <iostream>
#include <random>
#include <string>
#include <vector>

// std::string calc_string_operator() {}
// std::string calc_format() {}

class Strings_creator{
public:
    Strings_creator()
        : m_gen(std::random_device{}()), m_dist(m_min_ascii, m_max_ascii)
    {}

    std::vector<std::vector<std::string>> init_strings(std::size_t group_count, std::size_t string_count, std::size_t string_size)
    {
        std::vector<std::vector<std::string>> groups;
        groups.reserve(group_count);
        for(auto i = 0U; i < group_count; ++i)
        {
            std::vector<std::string> strings;
            strings.reserve(string_count);
            for (auto j = 0U; j < string_count; ++j)
            {
                strings.emplace_back(gen_string(string_size));
            }
            groups.emplace_back(strings);
        }

        return groups;
    }
private:
    std::string gen_string(std::size_t string_size)
    {
        std::string ret(string_size, '\0');
        std::generate_n(ret.begin(), string_size, [&]() {
            return static_cast<char>(m_dist(m_gen));
        });
        return ret;
    }

    const char m_min_ascii = 48;
    const char m_max_ascii = 126;

    std::mt19937 m_gen;
    std::uniform_int_distribution<int> m_dist;

};

class RaiiTimer{
public:
    RaiiTimer() : m_start_point(std::chrono::high_resolution_clock::now()) {}
    ~RaiiTimer() 
    {
        auto now = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> elapsed = now - m_start_point;
        std::cout << elapsed.count() << std::endl;
    }
private:
    std::chrono::time_point<std::chrono::high_resolution_clock> m_start_point;
};

void print_strings(const std::vector<std::vector<std::string>> &groups){
    for(const auto &group : groups)
    {
        for(const auto &string : group)
            std::cout << string << " ";

        std::cout << std::endl;
    }
}

int main() {
    RaiiTimer rt;

    Strings_creator sc;
    auto groups = sc.init_strings(100000,50,50);

    // print_strings(groups);
}
