#include <iostream>
#include <string>

using namespace std;

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

int main() {
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

    return 0;
}
