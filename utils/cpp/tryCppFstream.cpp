#include <fstream>
#include <iostream>
#include <sstream>

using namespace std;

int main() {
    ifstream infile("./test.in");
    string line;

    while (getline(infile, line)) {
        istringstream iss(line);
        cout << "line: " << line << endl;

        string col1, col2;
        iss >> col1 >> col2;
        cout << "col1: " << col1 << ", col2: " << col2 << endl;
    }

    return 0;
}
