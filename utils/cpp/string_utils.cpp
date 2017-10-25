#include <iostream>
#include <vector>
#include <string>
#include <cstddef>

using namespace std;

void print_vec(vector<string> &v) {
    for (size_t n = 0; n < v.size(); n++)
        cout << "\"" << v[n] << "\"\n";
    cout << endl;
}

void strim(string& input) {
    // "  Hello  World  " -> "Hello World"
    int i=0, j=0;

    while (j < input.size()) {
        while ( j+1 < input.size() && ' ' == input[j] && ' ' == input[j+1])
            ++j;
        if (0 == i && ' ' == input[j]) ++j;
        input[i++] = input[j++];
    }
    int size_new = (' ' == input[--i]) ? i : i+1;
    input.resize(size_new);
}


// Source from: http://www.cplusplus.com/faq/sequences/strings/split/
struct split
{
    enum empties_t { empties_ok, no_empties };
};

template <typename Container>
Container& split(
    Container&                            result,
    const typename Container::value_type& s,
    const typename Container::value_type& delimiters,
    split::empties_t                      empties = split::empties_ok )
{
    result.clear();
    size_t current;
    size_t next = -1;
    do {
	if (empties == split::no_empties) {
	  next = s.find_first_not_of(delimiters, next + 1);
	  if (next == Container::value_type::npos) break;
	  next -= 1;
	}
    current = next + 1;
    next = s.find_first_of(delimiters, current);
    result.push_back(s.substr(current, next - current));
    } while (next != Container::value_type::npos);
    return result;
}

int main() {
    // test for strim
    string input = "  Hello  World  ";
    cout << input << "$" << endl;
    cout << input.size() << endl;
    strim(input);
    cout << input << "$" << endl;
    cout << input.size() << endl;

    input = "Hello World";
    cout << input << "$" << endl;
    cout << input.size() << endl;
    strim(input);
    cout << input << "$" << endl;
    cout << input.size() << endl;
    cout << endl;

    // test for split
    input = "Hello,World,";
    vector<string> split_res;
    split(split_res, input, ",,");
    print_vec(split_res);

    input = "Hello___World___"; 
    split(split_res, input, "___"); // Only valid when delimiters is a char
    print_vec(split_res);

    input = "Hello___World___"; 
    split(split_res, input, "___", split::no_empties); // Only valid when delimiters is a char
    print_vec(split_res);

    return 0;
}
